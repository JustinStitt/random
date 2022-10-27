from random import randint, choices, choice


class Node:
    def __init__(self, r=0, c=0, s=0, val=None):
        self.val = val
        self.children = []
        self.r = r
        self.c = c
        self.s = s

    def __repr__(self):
        return f"Node(val={self.val}, s={self.s}, r={self.r}, c={self.c}, children=\033[31m{self.children})\033[39m"


def gridPrint(lst):
    for x in lst:
        for y in x:
            print(y if y != 0 else "░", end="")
        print()


def divide(img: list[list[int]]):
    assert len(img) > 0 and "Empty Image"
    rows = len(img)
    cols = len(img[0])
    assert rows == cols and "Non-square Size"
    # kick off main division with 4 divisions
    node = Node(0, 0, rows)
    divideRecur(node, img)
    return node


def divideRecur(node: Node, img: list[list[int]]):
    r = node.r
    c = node.c
    s = node.s
    # base case
    if s == 1:
        node.val = img[r][c]
        return

    new_size = s // 2
    # make 4 new nodes and divide those
    # 00, 01, 10, 11
    for b in range(4):
        newr = r + new_size if (b & 2) else r
        newc = c + new_size if (b & 1) else c
        node.children.append(Node(newr, newc, new_size))
        divideRecur(node.children[-1], img)

    # some child has no value (can't merge)
    if None in [n.val for n in node.children]:
        return
    # if all children have the same value, parent takes the value and destroys
    # its children (merge)
    if (
        node.children[0].val
        == node.children[1].val
        == node.children[2].val
        == node.children[3].val
    ):
        node.val = node.children[0].val
        node.children = []


def printNode(node: Node):
    for child in node.children:
        print(child)
    print()


def makeGrid(root: Node, grid):
    if not root:
        return
    if root.val:
        grid[root.r][root.c] = root.val
    for child in root.children:
        makeGrid(child, grid)


def makeRandomTestCase(s):
    opts = "AB"
    lst = [choices(opts, k=s) for _ in range(s)]
    # make some blocks
    blocks = 8
    max_size = s // 2
    while blocks > 0:
        randr = randint(0, s)
        randc = randint(0, s)
        rands = randint(0, max_size)
        randv = choice(opts)
        blocks -= 1
        rb = min(randr + rands, s)
        cb = min(randr + randc, s)
        for nr in range(randr, rb):
            for nc in range(randc, cb):
                lst[nr][nc] = randv

    return lst


lst = makeRandomTestCase(32)
# lst = ["AAAD", "AAGH", "ZJPP", "MNPP"]
gridPrint(lst)
root = divide(lst)
print("-" * 25)
grid = [[0] * root.s for _ in range(root.s)]
makeGrid(root, grid)
gridPrint(grid)
