import networkx as nx
import matplotlib.pyplot as plt
import random
import io
import base64

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    if node is None:
        return 0
    return node.height

def balance_factor(node):
    if node is None:
        return 0
    return height(node.left) - height(node.right)

def update_height(node):
    if node is not None:
        node.height = 1 + max(height(node.left), height(node.right))

def rotate_right(y):
    x = y.left
    t2 = x.right

    x.right = y
    y.left = t2

    update_height(y)
    update_height(x)

    return x

def rotate_left(x):
    y = x.right
    t2 = y.left

    x.right = t2
    y.left = x

    update_height(x)
    update_height(y)

    return y

def insert(root, key):
    if root is None:
        return Node(key)

    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    update_height(root)

    balance = balance_factor(root)

    if balance > 1:
        if key < root.left.key:
            return rotate_right(root)
        else:
            root.left = rotate_left(root.left)
            return rotate_right(root)

    if balance < -1:
        if key > root.right.key:
            return rotate_left(root)
        else:
            root.right = rotate_right(root.right)
            return rotate_left(root)

    return root

def build_graph(root, graph, pos, x=0, y=0, layer=1):
    if root is not None:
        graph.add_node(root.key, pos=(x, -y))
        if root.left:
            graph.add_edge(root.key, root.left.key)
            l_x, l_y = x - 1 / 2 ** layer, y + 1
            pos = build_graph(root.left, graph, pos, l_x, l_y, layer + 1)
        if root.right:
            graph.add_edge(root.key, root.right.key)
            r_x, r_y = x + 1 / 2 ** layer, y + 1
            pos = build_graph(root.right, graph, pos, r_x, r_y, layer + 1)
    return pos


def generate_avl(n_nodes=17):
    # Criação da árvore AVL

    random.seed(42)
    root = None
    keys = random.sample(range(1, 100), n_nodes)
    for key in keys:
        root = insert(root, key)

    # Criação do grafo NetworkX
    graph = nx.DiGraph()
    pos = build_graph(root, graph, {})

    # Desenho do grafo
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightgreen', font_size=10)

    # Salvar a imagem em um buffer (BytesIO)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return base64.b64encode(img.read()).decode('utf-8')





'''def generate_avl(n_nodes=17):
    root = None
    keys = random.sample(range(1, 100), n_nodes)
    for key in keys:
        root = insert(root, key)

    graph = nx.DiGraph()
    build_graph(root, graph)
    pos = nx.get_node_attributes(graph, 'pos')

    plt.figure(figsize=(6, 4))
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightgreen', font_size=10)
    
    # Salvar a imagem em um buffer (BytesIO)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return base64.b64encode(img.read()).decode('utf-8')






import networkx as nx
import matplotlib.pyplot as plt
import random
import io
import base64

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    return 0 if node is None else node.height

def balance_factor(node):
    return 0 if node is None else height(node.left) - height(node.right)

def update_height(node):
    if node:
        node.height = 1 + max(height(node.left), height(node.right))

def rotate_right(y):
    x, t2 = y.left, y.left.right
    x.right, y.left = y, t2
    update_height(y)
    update_height(x)
    return x

def rotate_left(x):
    y, t2 = x.right, x.right.left
    y.left, x.right = x, t2
    update_height(x)
    update_height(y)
    return y

def insert(root, key):
    if root is None:
        return Node(key)

    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    update_height(root)
    balance = balance_factor(root)

    if balance > 1:
        return rotate_right(root) if key < root.left.key else rotate_right(rotate_left(root.left))
    if balance < -1:
        return rotate_left(root) if key > root.right.key else rotate_left(rotate_right(root.right))

    return root

def build_graph(root, graph, x=0, y=0, layer=1):
    if root:
        graph.add_node(root.key, pos=(x, -y))
        if root.left:
            graph.add_edge(root.key, root.left.key)
            build_graph(root.left, graph, x - 1 / 2 ** layer, y + 1, layer + 1)
        if root.right:
            graph.add_edge(root.key, root.right.key)
            build_graph(root.right, graph, x + 1 / 2 ** layer, y + 1, layer + 1)

def generate_avl(n_nodes=17):
    root = None
    keys = random.sample(range(1, 100), n_nodes)
    for key in keys:
        root = insert(root, key)

    graph = nx.DiGraph()
    build_graph(root, graph)
    pos = nx.get_node_attributes(graph, 'pos')

    plt.figure(figsize=(6, 4))
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightgreen', font_size=10)
    
    # Salvar a imagem em um buffer (BytesIO)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return base64.b64encode(img.read()).decode('utf-8')
'''