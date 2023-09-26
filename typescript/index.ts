import assert from "assert";

class Node {
    right: Node | null = null;
    left: Node | null = null;
    value: number;

    constructor(value: number) {
        this.value = value;
    }
}

class BinarySearchTree {
    root: Node;

    constructor(value: number | Node) {
        if (typeof value === "number") {
            this.root = new Node(value);
        } else {
            this.root = value;
        }
    }

    insert(value: number) {
        const newNode = new Node(value);
        let node: Node | null = this.root;
        let parentNode = node;
        while (node !== null) {
            parentNode = node;
            // go to the left
            if (node.value > value) {
                node = node.left;
            }
            // go to the right
            else if (node.value < value) {
                node = node.right;
            }
        }
        if (parentNode.value > value) {
            parentNode.left = newNode;
        } else {
            parentNode.right = newNode;
        }
    }

    getNodeHeight(value: number) {
        let node: Node | null = this.root;
        let height = 0;
        while (node !== null && node.value !== value) {
            // go to the left
            if (node.value > value) {
                node = node.left;
            }
            // go to the right
            else if (node.value < value) {
                node = node.right;
            }
            height += 1;
        }
        if (node === null) {
            throw new Error();
        }
        return height;
    }

    search(value: number): BinarySearchTree | undefined {
        let node: Node | null = this.root;
        while (node !== null && node.value !== value) {
            // go to the left
            if (node.value > value) {
                node = node.left;
            } else if (node.value < value) {
                node = node.right;
            }
        }
        if (node === null) {
            throw new Error();
        }
        return new BinarySearchTree(node);
    }

    levelOrderTraversal() {
        const queue = [this.root];
        while (queue.length > 0) {
            let node = queue.shift() as Node;
            process.stdout.write(node.value + "->");
            if (node.left !== null) {
                queue.push(node.left);
            }
            if (node.right !== null) {
                queue.push(node.right);
            }
        }
    }

    max() {
        let node: Node | null = this.root;
        let _max: number | null = null;
        while (node !== null) {
            if (node.right == null) {
                _max = node.value;
            }
            node = node.right;
        }
        return _max;
    }

    min(node: Node | null = null) {
        let _node: Node | null = node === null ? this.root : node;
        let _min: number | null = null;
        while (_node !== null) {
            if (_node.left == null) {
                _min = _node.value;
            }
            _node = _node.left;
        }
        return _min;
    }

    // remove(value: number, node: Node | null = null) {
    //     const _node = node === null ? this.root : node;
    //     // go to the left
    //     if (_node.value > value) {
    //         if (_node.left === null) {
    //             throw new Error();
    //         }
    //         _node.left = this.remove(value, _node.left);
    //     }
    //     // go to the right
    //     else if (_node.value < value) {
    //         if (_node.right === null) {
    //             throw new Error();
    //         }
    //         _node.right = this.remove(value, _node.right);
    //     }
    //     // first case, where node is a leaf
    //     else if (_node.left === null && _node.right === null) {
    //         return null;
    //     }
    //     // second case, where node hasn't left
    //     else if (_node.left == null) {
    //         return _node.right;
    //     } // second case, where node hasn't right
    //     else if (_node.right == null) {
    //         return _node.left;
    //     }
    //     // third case, where node has both left and right
    //     else {
    //         const successor = this.min(_node.right);
    //         _node.value = successor;
    //         _node.right = this.remove(successor, _node.right);
    //     }
    //     return _node;
    // }
}

const binarySearchTree = new BinarySearchTree(50);

binarySearchTree.insert(30);
binarySearchTree.insert(70);
binarySearchTree.insert(40);
binarySearchTree.insert(60);
binarySearchTree.insert(20);
binarySearchTree.insert(80);

// 0 degree
assert.equal(binarySearchTree.root.value, 50);

// 1 degree
assert.equal((binarySearchTree.root.left as Node).value, 30);
assert.equal((binarySearchTree.root.right as Node).value, 70);

// 2 degree
assert.equal((binarySearchTree.root.left?.right as Node).value, 40);
assert.equal((binarySearchTree.root.left?.left as Node).value, 20);
assert.equal((binarySearchTree.root.right?.left as Node).value, 60);
assert.equal((binarySearchTree.root.right?.right as Node).value, 80);

// 0 degree
assert.equal(binarySearchTree.getNodeHeight(50), 0);

// 1 degree
assert.equal(binarySearchTree.getNodeHeight(30), 1);
assert.equal(binarySearchTree.getNodeHeight(30), 1);

// 2 degree
assert.equal(binarySearchTree.getNodeHeight(40), 2);
assert.equal(binarySearchTree.getNodeHeight(60), 2);
assert.equal(binarySearchTree.getNodeHeight(20), 2);
assert.equal(binarySearchTree.getNodeHeight(80), 2);

// inexistent node
assert.throws(() => binarySearchTree.getNodeHeight(-100), Error);

// search subtree
assert.equal(binarySearchTree.search(30) instanceof BinarySearchTree, true);

const subBinarySearchTree = binarySearchTree.search(30);

// 0 degree
assert.equal(subBinarySearchTree?.root.value, 30);

// 1 degree
assert.equal((subBinarySearchTree?.root.left as Node).value, 20);
assert.equal((subBinarySearchTree?.root.right as Node).value, 40);

// inexistent node
assert.throws(() => binarySearchTree.search(-100), Error);

// degree traversal
binarySearchTree.levelOrderTraversal();

// max value in the tree
assert.equal(binarySearchTree.max(), 80);

// min value in the tree
assert.equal(binarySearchTree.min(), 20);

function makeBst() {
    const bst = new BinarySearchTree(8);

    bst.insert(3);
    bst.insert(10);
    bst.insert(1);
    bst.insert(6);
    bst.insert(14);
    bst.insert(4);
    bst.insert(7);
    bst.insert(13);

    return bst;
}

let bst: BinarySearchTree;

// // remove leaf
// bst = makeBst();
// bst.remove(1);
// assert.equal((bst.root.left as Node).left, null);

// // remove node with one child
// bst = makeBst();
// bst.remove(10);
// assert.equal((bst.root.right as Node).value, 14);

// // remove root node
// bst = makeBst();
// bst.remove(8);
// assert.equal(bst.root.value, 10);
// assert.equal((bst.root.left as Node).value, 3);
// assert.equal((bst.root.right as Node).value, 14);

// // remove inexistent node
// bst = makeBst();
// assert.throws(() => bst.remove(-100), Error);

export default {};
