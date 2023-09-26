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

    def level_order_traversal(self):
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

    def min(self, node: Node | None = None):
        _node = self.root if node is None else node
        _min = None
        while _node is not None:
            if _node.left is None:
                _min = _node.value
            _node = _node.left
        return _min

    def remove(self, value: int):
        parent_node = self.root
        parent_direction = ""
        queue = [self.root]
        while len(queue) > 0:
            node = queue.pop(0)
            if node is None:
                raise ValueError()
            # go to the left
            if node.value > value:
                parent_node = node
                queue.append(node.left)
                parent_direction = "left"
            # go to the right
            elif node.value < value:
                parent_node = node
                queue.append(node.right)
                parent_direction = "right"
            # first case where node is a leaf
            elif node.right is None and node.left is None:
                if parent_direction == "left":
                    parent_node.left = None
                else:
                    parent_node.right = None
            # second case where node has only one child
            elif node.left is None:
                if parent_direction == "left":
                    parent_node.left = node.right
                else:
                    parent_node.right = node.right
            # second case where node has only one child
            elif node.right is None:
                if parent_direction == "left":
                    parent_node.left = node.left
                else:
                    parent_node.right = node.left
            # third case where node has both children
            else:
                successor = self.min(node.right)
                node.value = successor
                value = successor
                queue.append(node.right)


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
    binary_search_tree.level_order_traversal()

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

    # remove leaf
    bst = make_bst()
    bst.remove(1)
    assert bst.root.left.left is None

    # remove node with one child
    bst = make_bst()
    bst.remove(10)
    assert bst.root.right.value == 14

    # remove root node
    bst = make_bst()
    bst.remove(8)
    assert bst.root.value == 10
    assert bst.root.left.value == 3
    assert bst.root.right.value == 14

    # remove inexistent node
    bst = make_bst()
    try:
        bst.remove(-100)
        raise AssertionError
    except Exception as e:
        assert isinstance(e, ValueError)
