# frozen_string_literal: true

require 'minitest/autorun'

module Jekyll
  module Hooks
    def self.register(*) = nil
  end
end

require_relative '../_plugins/tabla_desplazable'

class TablaDesplazableContractTest < Minitest::Test
  NARRATIVE = <<~HTML.freeze
    <table><thead><tr><th>Pregunta</th><th>Lectura</th></tr></thead><tbody><tr><td>¿Qué ocurrió?</td><td>Una explicación narrativa deliberadamente extensa que no debe activar un contrato heredado.</td></tr></tbody></table>
  HTML

  SCROLL = <<~HTML.freeze
    <table class="table--compact table--numeric table--scroll"><thead><tr><th>Año</th><th>Valor</th></tr></thead><tbody><tr><td>2025</td><td>100</td></tr></tbody></table>
  HTML

  def test_explicit_contract_only_wraps_tables_marked_for_scroll
    output = TablaDesplazable.envolver("#{NARRATIVE}\n#{SCROLL}", 'es', 'explicit-v1')

    assert_equal 1, output.scan('class="tabla-desliza"').length
    assert_includes output, 'data-table-contract="explicit-v1"'
    assert_includes output, 'style="--table-columns: 2"'
    assert_equal 2, output.scan('scope="col"').length
    assert_includes output, 'class="table--compact table--numeric table--scroll"'
    assert_includes output, '>Año</th>'
  end

  def test_explicit_narrative_table_is_not_forced_to_an_extreme_width
    output = TablaDesplazable.envolver(NARRATIVE, 'es', 'explicit-v1')

    refute_includes output, 'tabla-desliza'
    refute_includes output, 'data-perfil="narrativa"'
  end

  def test_legacy_posts_keep_the_measured_heuristic
    output = TablaDesplazable.envolver(NARRATIVE, 'es', nil)

    assert_includes output, 'class="tabla-desliza"'
    assert_includes output, 'data-perfil="narrativa"'
  end

  def test_explicit_contract_is_idempotent_across_render_passes
    first = TablaDesplazable.envolver(SCROLL, 'es', 'explicit-v1')
    second = TablaDesplazable.envolver(first, 'es', 'explicit-v1')

    assert_equal 1, second.scan('class="tabla-desliza"').length
  end
end
