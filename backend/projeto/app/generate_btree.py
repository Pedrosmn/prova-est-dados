import matplotlib.pyplot as plt
import io
import base64
import random

def generate_b_tree(n_nodes=10, add_num=None, search_num=None, t=2):
    class BTreeNode:
        def __init__(self, leaf=False):
            self.keys = []
            self.children = []
            self.leaf = leaf

    class BTree:
        def __init__(self, t):
            self.root = BTreeNode(leaf=True)
            self.t = t  # Grau mínimo da árvore

        def insert(self, key):
            root = self.root
            if len(root.keys) == (2 * self.t) - 1:
                new_root = BTreeNode()
                self.root = new_root
                new_root.children.append(root)
                self._split_child(new_root, 0)
                self._insert_non_full(new_root, key)
            else:
                self._insert_non_full(root, key)

        def _insert_non_full(self, node, key):
            i = len(node.keys) - 1
            if node.leaf:
                node.keys.append(None)
                while i >= 0 and key < node.keys[i]:
                    node.keys[i + 1] = node.keys[i]
                    i -= 1
                node.keys[i + 1] = key
            else:
                while i >= 0 and key < node.keys[i]:
                    i -= 1
                i += 1
                if len(node.children[i].keys) == (2 * self.t) - 1:
                    self._split_child(node, i)
                    if key > node.keys[i]:
                        i += 1
                self._insert_non_full(node.children[i], key)

        def _split_child(self, parent, index):
            t = self.t
            child = parent.children[index]
            new_node = BTreeNode(leaf=child.leaf)

            parent.keys.insert(index, child.keys[t - 1])
            parent.children.insert(index + 1, new_node)

            new_node.keys = child.keys[t:(2 * t - 1)]
            child.keys = child.keys[0:(t - 1)]

            if not child.leaf:
                new_node.children = child.children[t:(2 * t)]
                child.children = child.children[0:t]

        def search(self, key, node=None):
            """Implementação do método de busca"""
            if node is None:
                node = self.root
            
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            
            if i < len(node.keys) and key == node.keys[i]:
                return (node, i)  # Retorna o nó e o índice da chave
            elif node.leaf:
                return None
            else:
                return self.search(key, node.children[i])

        def visualize(self, search_key=None):
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.set_aspect('equal')
            ax.axis('off')

            if not self.root.keys:
                return ""

            # Verifica se a chave de busca existe
            found_node = None
            found_index = -1
            if search_key is not None:
                search_result = self.search(search_key)
                if search_result is not None:
                    found_node, found_index = search_result

            # Calcula as posições dos nós
            positions = {}
            levels = {}
            self._calculate_positions(self.root, 0, 0, positions, levels)

            # Desenha as conexões
            for node in positions:
                if not node.leaf:
                    x, y = positions[node]
                    for i, child in enumerate(node.children):
                        if child in positions:
                            cx, cy = positions[child]
                            plt.plot([x, cx], [y - 0.1, cy + 0.1], 'k-', lw=1)

            # Desenha os nós
            for node in positions:
                x, y = positions[node]
                is_found_node = (node == found_node)
                self._draw_node(ax, node, x, y, is_found_node, found_index)

            plt.tight_layout()
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            return base64.b64encode(img.read()).decode('utf-8')

        def _calculate_positions(self, node, x, level, positions, levels, spacing=2.0):
            if node is None:
                return x

            # Calcula a posição dos filhos
            child_x = x
            child_positions = []
            if not node.leaf:
                for child in node.children:
                    child_x = self._calculate_positions(child, child_x, level + 1, positions, levels, spacing)
                    child_positions.append(child_x)

            # Posição atual do nó
            if child_positions:
                node_x = (child_positions[0] + child_positions[-1]) / 2
            else:
                node_x = x

            positions[node] = (node_x, -level)
            levels[node] = level

            return child_x + 1 if node.leaf else child_x

        def _draw_node(self, ax, node, x, y, is_found_node=False, found_index=-1):
            num_keys = len(node.keys)
            width = num_keys * 0.5
            height = 0.4

            facecolor = 'lightgreen' if is_found_node else 'lightyellow'
            rect = plt.Rectangle((x - width/2, y - height/2), width, height,
                               facecolor=facecolor, edgecolor='black', lw=1)
            ax.add_patch(rect)

            for i, key in enumerate(node.keys):
                key_x = x - width/2 + 0.25 + i * 0.5
                if is_found_node and i == found_index:
                    ax.text(key_x, y, str(key), ha='center', va='center',
                          fontsize=10, weight='bold', bbox=dict(facecolor='yellow', alpha=0.7))
                else:
                    ax.text(key_x, y, str(key), ha='center', va='center', fontsize=10)

    btree = BTree(t=t)
    random.seed(42)
    keys = random.sample(range(1, 100), min(n_nodes, 99))
    for key in keys:
        btree.insert(key)

    # Adiciona nós extras se especificado
    if add_num:
        if isinstance(add_num, list):
            for num in add_num:
                btree.insert(num)
        else:
            btree.insert(add_num)

    return btree.visualize(search_key=search_num)