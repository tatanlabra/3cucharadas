# frozen_string_literal: true
require 'minitest/autorun'
require 'tmpdir'
require_relative '../scripts/lib/devto_draft_policy'

class DevtoDraftPolicyTest < Minitest::Test
  def setup
    @draft = { 'id' => 42, 'canonical_url' => 'https://3cucharadas.cl/en/example/', 'published' => false, 'body_markdown' => 'original' }
    @payload = { article: { canonical_url: @draft['canonical_url'], body_markdown: 'replacement' } }
    @writes = []
    @writer = ->(id, body) { @writes << [id, body]; [200, @draft] }
  end

  def write(target = @draft, current = [@draft], writer = @writer)
    DevtoDraftPolicy.update!(target, current: current, payload: @payload, writer: writer)
  end

  def test_forbidden_targets_red_then_valid_recovery
    [nil, @draft.merge('published' => true), @draft.merge('body_markdown' => nil)].each do |target|
      assert_raises(DevtoDraftPolicy::Violation) { write(target) }
    end
    [[], [@draft.merge('published' => true)], [@draft, @draft.merge('id' => 43)], [@draft.merge('body_markdown' => 'concurrent edit')]].each do |current|
      assert_raises(DevtoDraftPolicy::Violation) { write(@draft, current) }
    end
    assert_empty @writes
    assert_equal 200, write.first
    assert_equal 1, @writes.length
  end

  def test_rate_limit_is_failure_not_success
    assert_raises(DevtoDraftPolicy::Violation) { write(@draft, [@draft], ->(*) { [429, {}] }) }
    assert_equal 200, write.first
  end

  def test_publication_attribute_and_wrong_response_are_rejected
    @payload[:article][:published] = true
    assert_raises(DevtoDraftPolicy::Violation) { write }
    assert_empty @writes
    @payload[:article].delete(:published)
    assert_raises(DevtoDraftPolicy::Violation) { write(@draft, [@draft], ->(*) { [200, @draft.merge('published' => true)] }) }
  end

  def test_encrypted_custody_round_trip_and_tamper_rejection
    Dir.mktmpdir do |dir|
      assert_raises(DevtoDraftPolicy::Violation) { DevtoDraftPolicy.backup!([], dir, 'test-key') }
      DevtoDraftPolicy.backup!([@draft], dir, 'test-key')
      path = File.join(dir, 'drafts-before.enc.json')
      snapshot = JSON.parse(File.read(path))
      assert_equal [@draft], DevtoDraftPolicy.decrypt_snapshot(snapshot, 'test-key')
      assert_equal 0o600, File.stat(path).mode & 0o777
      assert_raises(OpenSSL::Cipher::CipherError) { DevtoDraftPolicy.decrypt_snapshot(snapshot, 'wrong-key') }
      snapshot['tag'] = Base64.strict_encode64('x' * 16)
      assert_raises(OpenSSL::Cipher::CipherError) { DevtoDraftPolicy.decrypt_snapshot(snapshot, 'test-key') }
      assert_raises(Errno::EEXIST) { DevtoDraftPolicy.backup!([@draft], dir, 'test-key') }
    end
  end
end
