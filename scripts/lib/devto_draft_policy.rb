# frozen_string_literal: true
require 'json'
require 'openssl'
require 'base64'
require 'fileutils'

# The API has no conditional PUT: recheck immediately before writing, and stop
# on any observed race. Do not claim this eliminates the check-to-write window.
module DevtoDraftPolicy
  class Violation < StandardError; end
  FIELDS = %w[id canonical_url published body_markdown title description tag_list cover_image updated_at edited_at].freeze

  def self.select(articles, canonical)
    matches = articles.select { |a| a['canonical_url'] == canonical }
    raise Violation, "duplicate canonical: #{canonical}" if matches.length > 1
    matches.select { |a| a['published'] == false }
  end

  def self.validate!(target, current)
    raise Violation, 'missing target; creation forbidden' unless target && target['id'].is_a?(Integer) && target['id'].positive?
    raise Violation, 'published/unknown target forbidden' unless target['published'] == false
    raise Violation, 'missing rollback body' unless target['body_markdown'].is_a?(String) && !target['body_markdown'].empty?
    matches = select(current, target.fetch('canonical_url'))
    raise Violation, 'draft missing or published since inventory' unless matches.one? && matches.first['id'] == target['id']
    raise Violation, 'draft changed since inventory' unless FIELDS.all? { |key| target[key] == matches.first[key] }
    true
  end

  def self.update!(target, current:, payload:, writer:)
    validate!(target, current)
    article = payload.fetch(:article)
    raise Violation, 'unexpected canonical or publication attribute' unless article[:canonical_url] == target['canonical_url'] && !article.key?(:published)
    code, body = writer.call(target.fetch('id'), payload)
    raise Violation, "PUT failed HTTP #{code}; stop remaining writes" unless code.between?(200, 299)
    raise Violation, 'unexpected response identity/state' unless body.is_a?(Hash) && body['id'] == target['id'] && body['published'] == false
    [code, body]
  end

  # Persist only authenticated ciphertext. The API key never enters the file or
  # logs. Retain the current key until restoring/exporting any needed snapshot.
  def self.encrypt_snapshot(value, secret)
    salt = OpenSSL::Random.random_bytes(16)
    cipher = OpenSSL::Cipher.new('aes-256-gcm').encrypt
    cipher.key = OpenSSL::KDF.pbkdf2_hmac(secret, salt: salt, iterations: 250_000, length: 32, hash: 'SHA256')
    nonce = cipher.random_iv
    cipher.auth_data = '3c-devto-snapshot-v1'
    ciphertext = cipher.update(JSON.generate(value)) + cipher.final
    encoded = { 'salt' => salt, 'nonce' => nonce, 'tag' => cipher.auth_tag, 'ciphertext' => ciphertext }
      .transform_values { |value| Base64.strict_encode64(value) }
    { 'version' => 1 }.merge(encoded)
  end

  def self.decrypt_snapshot(value, secret)
    raise Violation, 'unsupported snapshot' unless value.fetch('version') == 1
    cipher = OpenSSL::Cipher.new('aes-256-gcm').decrypt
    cipher.key = OpenSSL::KDF.pbkdf2_hmac(secret, salt: Base64.strict_decode64(value.fetch('salt')), iterations: 250_000, length: 32, hash: 'SHA256')
    cipher.iv = Base64.strict_decode64(value.fetch('nonce'))
    cipher.auth_tag = Base64.strict_decode64(value.fetch('tag'))
    cipher.auth_data = '3c-devto-snapshot-v1'
    JSON.parse(cipher.update(Base64.strict_decode64(value.fetch('ciphertext'))) + cipher.final)
  end

  def self.backup!(targets, directory, secret)
    raise Violation, 'empty draft inventory' if targets.empty?
    targets.each { |target| validate!(target, targets) }
    FileUtils.mkdir_p(directory, mode: 0o700)
    File.open(File.join(directory, 'drafts-before.enc.json'), File::WRONLY | File::CREAT | File::EXCL, 0o600) do |file|
      file.write(JSON.pretty_generate(encrypt_snapshot(targets, secret)) + "\n")
    end
  end
end
