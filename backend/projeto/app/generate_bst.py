import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import random

def generate_binary_tree(n_nodes=10, search_num=None, add_nodes=None):
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    class BST:
        def __init__(self):
            self.root = None

        def insert(self, keys):
            """Aceita um único valor ou uma lista de valores"""
            if isinstance(keys, (list, tuple)):
                for key in keys:
                    self._insert_single(key)
            else:
                self._insert_single(keys)

        def _insert_single(self, key):
            if self.root is None:
                self.root = Node(key)
            else:
                self._insert_recursive(self.root, key)

        def _insert_recursive(self, node, key):
            if key < node.key:
                if node.left is None:
                    node.left = Node(key)
                else:
                    self._insert_recursive(node.left, key)
            elif key > node.key:
                if node.right is None:
                    node.right = Node(key)
                else:
                    self._insert_recursive(node.right, key)

        def search(self, key):
            return self._search_recursive(self.root, key)

        def _search_recursive(self, node, key):
            if node is None or node.key == key:
                return node
            if key < node.key:
                return self._search_recursive(node.left, key)
            return self._search_recursive(node.right, key)

        def visualize(self, highlight_key=None):
            G = nx.DiGraph()
            queue = [self.root]
            color_map = []
            
            while queue:
                node = queue.pop(0)
                if node is None:
                    continue
                
                G.add_node(node.key)
                if highlight_key is not None and node.key == highlight_key:
                    color_map.append('limegreen')
                else:
                    color_map.append('skyblue')
                
                if node.left:
                    G.add_edge(node.key, node.left.key)
                    queue.append(node.left)
                if node.right:
                    G.add_edge(node.key, node.right.key)
                    queue.append(node.right)

            # Tentar layouts hierárquicos diferentes
            try:
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            except:
                try:
                    pos = nx.graphviz_layout(G, prog='dot')
                except:
                    # Fallback para layout hierárquico se graphviz não estiver disponível
                    pos = {}
                    if G.nodes():
                        root = self.root.key
                        pos[root] = (0, 0)
                        self._compute_positions(G, root, pos, x=0, y=0, level_height=1)

            plt.figure(figsize=(10, 6))
            nx.draw(G, pos, with_labels=True, node_size=1000, 
                   node_color=color_map, font_size=10, arrows=True)
            plt.title("Binary Search Tree" + 
                     (f" (Node {highlight_key} found)" if highlight_key else ""))
            
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
            plt.close()
            img.seek(0)
            return base64.b64encode(img.read()).decode('utf-8')

        def _compute_positions(self, G, node, pos, x, y, level_height, level_width=1.0):
            """Calcula posições hierárquicas manualmente"""
            children = list(G.successors(node))
            if not children:
                return
            
            # Divide o espaço horizontal entre os filhos
            n_children = len(children)
            width_per_child = level_width / n_children
            next_x = x - level_width/2 + width_per_child/2
            
            for child in children:
                pos[child] = (next_x, y - level_height)
                self._compute_positions(G, child, pos, next_x, y - level_height, 
                                      level_height, width_per_child)
                next_x += width_per_child

    bst = BST()
    random.seed(42)
    values = random.sample(range(1, 100), min(n_nodes, 99))
    bst.insert(values)

    if add_nodes:
        bst.insert(add_nodes)

    highlight = None
    if search_num is not None:
        found_node = bst.search(search_num)
        if found_node:
            highlight = search_num

    return bst.visualize(highlight_key=highlight)

'''import networkx as nx
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
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

# Construção da árvore
root = None
keys = [50, 30, 20, 40, 70, 60, 80]
for key in keys:
    root = insert(root, key)

# Criação do grafo NetworkX
graph = nx.DiGraph()
pos = build_graph(root, graph, {})

# Desenho do grafo
pos = nx.get_node_attributes(graph, 'pos')
nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightgreen', font_size=10)






def generate_binary_tree():
    n=1'''
'''teste'''



'''import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

def build_graph(root, graph, x=0, y=0, layer=1):
    if root is not None:
        graph.add_node(root.key, pos=(x, -y))
        if root.left:
            graph.add_edge(root.key, root.left.key)
            build_graph(root.left, graph, x - 1 / 2 ** layer, y + 1, layer + 1)
        if root.right:
            graph.add_edge(root.key, root.right.key)
            build_graph(root.right, graph, x + 1 / 2 ** layer, y + 1, layer + 1)

def generate_binary_tree():
    # Construção da árvore
    root = None
    keys = [50, 30, 20, 40, 70, 60, 80]  # Valores fixos para teste
    for key in keys:
        root = insert(root, key)

    # Criar grafo
    graph = nx.DiGraph()
    build_graph(root, graph)
    pos = nx.get_node_attributes(graph, 'pos')

    # Criar figura
    plt.figure(figsize=(6, 4))
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightgreen', font_size=10)

    # Salvar a imagem em um buffer (BytesIO)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return base64.b64encode(img.read()).decode('utf-8')'''