import matplotlib.pyplot as plt
import numpy as np
import time
import random
import io
import base64

class SelfOrganizingList:
    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

    def is_empty(self):
        return len(self.items) == 0

    def insert(self, item):
        self.items.insert(0, item)

    def search(self, item):
        raise NotImplementedError("Subclasses should implement this!")

    def visualize(self, title=""):
        fig = plt.figure(figsize=(10, 2))
        plt.title(title)

        for i, val in enumerate(self.items):
            plt.barh(0, 1, left=i, height=0.6, color='skyblue', alpha=0.7)
            plt.text(i + 0.5, 0, str(val), ha='center', va='center')

        plt.xlim(0, len(self.items))
        plt.ylim(-1, 1)
        plt.axis('off')
        
        # Convert plot to base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

class MoveToFrontList(SelfOrganizingList):
    def search(self, item):
        images = []
        
        for i in range(len(self.items)):
            if self.items[i] == item:
                # Visualize before moving
                images.append(self.visualize(f"Found {item} at position {i}"))
                
                # Move to front
                self.items.pop(i)
                self.items.insert(0, item)
                
                # Visualize after moving
                images.append(self.visualize(f"Moved {item} to front"))
                
                return True, images

        return False, [self.visualize(f"{item} not found")]

class TransposeList(SelfOrganizingList):
    def search(self, item):
        images = []
        
        for i in range(len(self.items)):
            if self.items[i] == item:
                if i > 0:  # Not already at the front
                    # Visualize before swapping
                    images.append(self.visualize(f"Found {item} at position {i}"))
                    
                    # Swap with previous element
                    self.items[i], self.items[i-1] = self.items[i-1], self.items[i]
                    
                    # Visualize after swapping
                    images.append(self.visualize(f"Transposed {item} with previous element"))
                else:
                    images.append(self.visualize(f"{item} already at front position"))
                
                return True, images

        return False, [self.visualize(f"{item} not found")]

class SkipNode:
    def __init__(self, value=None, level=0):
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=4, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = SkipNode(None, max_level)
        self.level = 0

    def random_level(self):
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def insert(self, value):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.value != value:
            new_level = self.random_level()

            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level

            new_node = SkipNode(value, new_level)

            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def search(self, value):
        current = self.header
        path = []
        search_steps = []
        images = []

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                path.append((i, current.value if current.value is not None else "H"))
                current = current.forward[i]
                search_steps.append((list(path), f"Searching {value} at level {i}"))
                images.append(self._visualize_search_step(path, value, f"Searching {value} at level {i}"))

            path.append((i, current.value if current.value is not None else "H"))
            search_steps.append((list(path), f"Checking pointer at level {i}"))
            images.append(self._visualize_search_step(path, value, f"Checking pointer at level {i}"))

        current = current.forward[0]
        found = current and current.value == value
        path.append((0, current.value if found else "X"))
        images.append(self._visualize_search_step(path, value, 
                f"Value {value} {'found!' if found else 'not found!'}", True))

        return found, images

    def visualize(self, title="Skip List"):
        img = self._generate_skip_list_image(title)
        return img

    def _generate_skip_list_image(self, title="Skip List"):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        nodes = {}
        max_width = 0
        current = self.header.forward[0]
        x_pos = 0

        while current:
            nodes[current.value] = x_pos
            max_width = max(max_width, x_pos)
            x_pos += 1
            current = current.forward[0]

        for level in range(self.level, -1, -1):
            current = self.header
            y = level + 1
            prev_x = -0.5

            ax.text(-0.5, y, "H", ha='center', va='center',
                   bbox=dict(facecolor='skyblue', boxstyle='circle'))

            while current.forward[level]:
                current = current.forward[level]
                x = nodes[current.value]

                ax.plot([prev_x + 0.5, x], [y, y], 'b-', linewidth=1)
                ax.text(x, y, str(current.value), ha='center', va='center',
                       bbox=dict(facecolor='lightgreen', boxstyle='circle'))
                prev_x = x

            ax.plot([prev_x + 0.5, max_width + 0.5], [y, y], 'b-', linewidth=1)

        for value, x in nodes.items():
            node = self.header
            while node.forward[0] and node.forward[0].value != value:
                node = node.forward[0]
            node = node.forward[0]

            top_level = len(node.forward) - 1
            ax.plot([x, x], [1, top_level + 1], 'b--', alpha=0.3)

        ax.set_xlim(-1, max_width + 1)
        ax.set_ylim(0, self.level + 2)
        ax.set_title(title)
        ax.axis('off')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    def _visualize_search_step(self, path, value, description, final=False):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        nodes = {}
        max_width = 0
        current = self.header.forward[0]
        x_pos = 0

        while current:
            nodes[current.value] = x_pos
            max_width = max(max_width, x_pos)
            x_pos += 1
            current = current.forward[0]

        for level in range(self.level, -1, -1):
            current = self.header
            y = level + 1
            prev_x = -0.5

            header_color = 'red' if (level, "H") in path else 'skyblue'
            ax.text(-0.5, y, "H", ha='center', va='center',
                  bbox=dict(facecolor=header_color, boxstyle='circle'))

            while current.forward[level]:
                current = current.forward[level]
                x = nodes[current.value]

                node_in_path = (level, current.value) in path
                line_color = 'r-' if node_in_path else 'b-'
                node_color = 'red' if node_in_path else 'lightgreen'

                ax.plot([prev_x + 0.5, x], [y, y], line_color,
                      linewidth=2 if node_in_path else 1)
                ax.text(x, y, str(current.value), ha='center', va='center',
                    bbox=dict(facecolor=node_color, boxstyle='circle'))
                prev_x = x

            ax.plot([prev_x + 0.5, max_width + 0.5], [y, y], 'b-', linewidth=1)

        for val, x in nodes.items():
            node = self.header
            while node.forward[0] and node.forward[0].value != val:
                node = node.forward[0]
            node = node.forward[0]

            top_level = len(node.forward) - 1
            line_style = 'r--' if any((l, val) in path for l in range(top_level+1)) else 'b--'
            ax.plot([x, x], [1, top_level + 1], line_style, alpha=0.5)

        ax.text(max_width/2, -0.5, description, ha='center', va='center',
              fontsize=12, color='green' if 'found!' in description else 'red',
              bbox=dict(facecolor='white', alpha=0.8))

        ax.set_xlim(-1, max_width + 1)
        ax.set_ylim(-1, self.level + 2)
        ax.set_title(f"Searching for: {value}")
        ax.axis('off')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

def auto_list_operation(list_type, operation, value=None, items=None, size=10):
    print(f"Operação: {operation}")
    print(f"Tipo: {list_type}")
    print(f"Items: {items}")
    print(f"Valor: {value}")
    try:
        if list_type == "move_to_front":
            lst = MoveToFrontList()
        elif list_type == "transpose":
            lst = TransposeList()
        else:
            return {"error": "Tipo de lista inválido"}, 400

        # Inicializa a lista
        if items:
            for item in reversed(items):
                lst.insert(item)
        else:
            for i in range(size, 0, -1):
                lst.insert(i)

        if operation == "search" and value is not None:
            success, images = lst.search(value)
            if not images:  # Se não gerou imagens, gera pelo menos uma
                images = [lst.visualize(f"Resultado da busca por {value}")]
            return {
                "success": success,
                "images": images,
                "list": str(lst.items)
            }
        else:
            image = lst.visualize(f"Lista {list_type}")
            return {
                "image": image,
                "list": str(lst.items)
            }

    except Exception as e:
        return {"error": str(e)}, 500
    
def skip_list_operation(operation, search_value=None, insert_values=None, max_level=4):
    skip_list = SkipList(max_level=max_level)
    
    default_values = [3, 6, 7, 9, 12, 19, 17, 21, 25]
    for value in default_values:
        skip_list.insert(value)
    
    if insert_values:
        if isinstance(insert_values, list):
            for value in insert_values:
                skip_list.insert(value)
        else:
            skip_list.insert(insert_values)
    
    if operation == "search" and search_value is not None:
        found, images = skip_list.search(search_value)
        return {
            "found": found,
            "images": images,
            "list": "Skip list visualization"
        }
    elif operation == "visualize":
        return {
            "image": skip_list.visualize("Skip List"),
            "list": "Skip list visualization"
        }
    elif operation == "insert":
        return {
            "image": skip_list.visualize("Skip List After Insertion"),
            "list": "Skip list visualization"
        }
    else:
        return {"error": "Invalid operation"}, 400