require "test/unit"
# FIXME: Remove this hardcoded path
require_relative "../build/generated/Tree"

class TestTree < Test::Unit::TestCase
  def test_subtree_handle_keeps_tree_alive
    t = Tree.new(1)
    st = t.left_subtree()
    x = st.data()
    t = nil
    ObjectSpace.garbage_collect
    assert_equal(x, st.data())
  end

  def test_tree_set_data
    t = Tree.new(0)
    t.set_data(77)
    assert_equal(77, t.data())
  end
end

