# frozen_string_literal: true
require 'minitest/autorun'
require_relative '../_plugins/math_keyboard'

class MathKeyboardTest < Minitest::Test
  def test_only_display_wrapper_changes_and_remains_idempotent
    inner = '<span class="katex"><math><mi>x</mi></math></span>'
    original = '<span class="katex-display">' + inner + '</span>'
    refute_includes original, 'tabindex="0"'
    decorated = MathKeyboard.decorate(original, 'es')
    assert_includes decorated, 'tabindex="0"'
    assert_includes decorated, 'Fórmula matemática'
    assert_includes decorated, inner
    assert_equal decorated, MathKeyboard.decorate(decorated, 'es')
    assert_equal inner, MathKeyboard.decorate(inner, 'es')
    assert_includes MathKeyboard.decorate(original, 'en'), 'Mathematical formula'
  end
end
