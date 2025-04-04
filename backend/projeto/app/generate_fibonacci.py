import matplotlib.pyplot as plt
import io
import base64

def generate_fibonacci_tree(n=5):  # Adicionei o parâmetro 'n' aqui
    # Limita o valor máximo para evitar recursão excessiva
    n = min(max(1, n), 7)  # Limita entre 1 e 7
    
    # Cache para os números de Fibonacci
    fib_cache = {0: 0, 1: 1}
    
    def fib(n):
        if n not in fib_cache:
            fib_cache[n] = fib(n-1) + fib(n-2)
        return fib_cache[n]
    
    plt.figure(figsize=(10, 8))
    
    def draw(n, x, y, dx, dy):
        if n <= 1:
            plt.text(x, y, str(fib(n)), ha='center', va='center',
                   bbox=dict(facecolor='lightgreen', boxstyle='circle', pad=0.5))
            return
        
        left_x = x - dx
        right_x = x + dx
        
        plt.plot([x, left_x], [y, y-dy], 'k-', lw=1.5)
        plt.plot([x, right_x], [y, y-dy], 'k-', lw=1.5)
        
        plt.text(x, y, str(fib(n)), ha='center', va='center',
               bbox=dict(facecolor='lightgreen', boxstyle='circle', pad=0.5))
        
        draw(n-1, left_x, y-dy, dx/1.8, dy*0.9)
        draw(n-2, right_x, y-dy, dx/1.8, dy*0.9)
    
    draw(n, 0, 0, 4, 1.5)
    plt.axis('off')
    plt.title(f"Árvore de Fibonacci (F({n}))", pad=20)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    img.seek(0)
    return base64.b64encode(img.read()).decode('utf-8')