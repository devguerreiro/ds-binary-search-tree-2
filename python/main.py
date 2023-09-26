from typing import TypeVar


TNode = TypeVar("TNode", bound="Node")


class Node:
    right: TNode | None = None
    left: TNode | None = None
    value: int

    def __init__(self, value: int):
        self.value = value


class BinarySearchTree:
    root: Node

    def __init__(self, value: int | None = None, node: Node | None = None):
        if node is not None:
            self.root = node
        elif value is not None:
            self.root = Node(value)

    def insert(self, value: int):
        new_node = Node(value)
        node = self.root
        parent_node = node
        while node is not None:
            parent_node = node
            # go to the left
            if node.value > value:
                node = node.left
            # go to the right
            elif node.value < value:
                node = node.right
        if parent_node.value > value:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

    def get_node_height(self, value: int):
        node = self.root
        height = 0
        while node is not None and node.value != value:
            # go to the left
            if node.value > value:
                node = node.left
            # go to the right
            elif node.value < value:
                node = node.right
            height += 1
        if node is None:
            raise ValueError()
        return height

    def search(self, value: int, node: Node | None = None):
        node = self.root
        while node is not None and node.value != value:
            # go to the left
            if node.value > value:
                node = node.left
            # go to the right
            elif node.value < value:
                node = node.right
        if node is None:
            raise ValueError()
        return BinarySearchTree(node=node)

    def degree_traversal(self):
        queue = [self.root]
        while len(queue) > 0:
            node = queue.pop(0)
            print(node.value, end="->")
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

    def max(self):
        node = self.root
        _max = None
        while node is not None:
            if node.right is None:
                _max = node.value
            node = node.right
        return _max

    def min(self):
        node = self.root
        _min = None
        while node is not None:
            if node.left is None:
                _min = node.value
            node = node.left
        return _min

    def remove(
        self,
        value: int,
        node: Node | None = None,
    ):
        _node = self.root if node is None else node
        # go to the left
        if _node.value > value:
            if _node.left is None:
                raise ValueError()
            _node.left = self.remove(value, _node.left)
        # go to the right
        elif _node.value < value:
            if _node.right is None:
                raise ValueError()
            _node.right = self.remove(value, _node.right)
        # first case, where node is a leaf
        elif _node.left is None and _node.right is None:
            return None
        # second case, where node hasn't left
        elif _node.left is None:
            return _node.right
        # second case, where node hasn't right
        elif _node.right is None:
            return _node.left
        # third case, where node has both left and right
        else:
            successor = self.min(_node.right)
            _node.value = successor
            _node.right = self.remove(successor, _node.right)
        return _node


if __name__ == "__main__":
    binary_search_tree = BinarySearchTree(50)

    binary_search_tree.insert(30)
    binary_search_tree.insert(70)
    binary_search_tree.insert(40)
    binary_search_tree.insert(60)
    binary_search_tree.insert(20)
    binary_search_tree.insert(80)

    # 0 degree
    assert binary_search_tree.root.value == 50

    # 1 degree
    assert binary_search_tree.root.left.value == 30
    assert binary_search_tree.root.right.value == 70

    # 2 degree
    assert binary_search_tree.root.left.right.value == 40
    assert binary_search_tree.root.left.left.value == 20
    assert binary_search_tree.root.right.left.value == 60
    assert binary_search_tree.root.right.right.value == 80

    # 0 degree
    assert binary_search_tree.get_node_height(50) == 0

    # 1 degree
    assert binary_search_tree.get_node_height(30) == 1
    assert binary_search_tree.get_node_height(70) == 1

    # 2 degree
    assert binary_search_tree.get_node_height(40) == 2
    assert binary_search_tree.get_node_height(60) == 2
    assert binary_search_tree.get_node_height(20) == 2
    assert binary_search_tree.get_node_height(80) == 2

    # inexistent node
    try:
        binary_search_tree.get_node_height(-100)
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, ValueError)

    # search subtree
    assert isinstance(binary_search_tree.search(30), BinarySearchTree)

    sub_binary_search_tree = binary_search_tree.search(30)

    # 0 degree
    assert sub_binary_search_tree.root.value == 30

    # 1 degree
    assert sub_binary_search_tree.root.left.value == 20
    assert sub_binary_search_tree.root.right.value == 40

    # inexistent node
    try:
        binary_search_tree.search(-100)
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, ValueError)

    # degree traversal
    binary_search_tree.degree_traversal()

    # max value in the three
    assert binary_search_tree.max() == 80

    # min value in the three
    assert binary_search_tree.min() == 20

    def make_bst():
        bst = BinarySearchTree(8)

        bst.insert(3)
        bst.insert(10)
        bst.insert(1)
        bst.insert(6)
        bst.insert(14)
        bst.insert(4)
        bst.insert(7)
        bst.insert(13)

        return bst

    # # remove leaf
    # bst = make_bst()
    # bst.remove(1)
    # assert bst.root.left.left is None

    # # remove node with one child
    # bst = make_bst()
    # bst.remove(10)
    # assert bst.root.right.value == 14

    # # remove root node
    # bst = make_bst()
    # bst.remove(8)
    # assert bst.root.value == 10
    # assert bst.root.left.value == 3
    # assert bst.root.right.value == 14

    # # remove inexistent node
    # bst = make_bst()
    # try:
    #     bst.remove(-100)
    #     raise AssertionError
    # except Exception as e:
    #     assert isinstance(e, ValueError)
