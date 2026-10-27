# frozen_string_literal: true

require 'minitest/autorun'

module Jekyll
  module Hooks
    def self.register(*) = nil
  end
end

require_relative '../_plugins/tabla_desplazable'
require_relative '../_plugins/tablas_numericas'

class TablasNumericasContractTest < Minitest::Test
  def test_recognizes_english_and_spanish_intervals_as_numeric
    assert TablasNumericas.cifra?('[−0.77, 2.03]')
    assert TablasNumericas.cifra?('[88.5%, 91.5%]')
    assert TablasNumericas.cifra?('[−0,77; 2,03] pp')
  end

  def test_marks_interval_columns_and_header
    html = <<~HTML
      <table><thead><tr><th>Resultado</th><th>Intervalo</th></tr></thead><tbody>
      <tr><td>A</td><td>[−0.77, 2.03]</td></tr>
      <tr><td>B</td><td>[88.5%, 91.5%]</td></tr>
      </tbody></table>
    HTML

    output = TablasNumericas.marcar(html)

    assert_equal 3, output.scan(/class="num"/).length
    assert_includes output, '<th class="num">Intervalo</th>'
  end

  def test_does_not_treat_narrative_brackets_as_numeric
    refute TablasNumericas.cifra?('[resultado, lectura]')
  end
end
