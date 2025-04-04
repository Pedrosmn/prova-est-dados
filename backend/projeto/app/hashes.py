import numpy as np
import random
import matplotlib.pyplot as plt
import io
import base64
from flask import jsonify

def generate_hashing_image(hashing_type):
    plt.switch_backend('Agg')  # Importante para evitar problemas com matplotlib em threads
    
    if hashing_type == "Perfeito":
        return hashing_perfeito_program()
    elif hashing_type == "Universal":
        return hashing_universal_program()
    elif hashing_type == "Encadeado":
        return hashing_encadeado_program()
    elif hashing_type == "Sondagem":
        return hashing_sondagem_program()
    elif hashing_type == "Duplo":
        return hashing_duplo_program()
    else:
        raise ValueError("Tipo de hashing não suportado")

def hashing_perfeito_program():
    def hashing_perfeito(chaves):
        hash_map = {1: 0, 10: 1, 20: 2, 30: 3, 40: 4}  # Mapeamento manual
        tabela = [None] * len(chaves)
        for chave in chaves:
            tabela[hash_map[chave]] = chave
        return tabela

    # Dados
    chaves = [1, 10, 20, 30, 40]
    tabela_perfeita = hashing_perfeito(chaves)

    # Plotagem
    plt.figure(figsize=(10, 5))
    indices = range(len(tabela_perfeita))
    valores = [1 if chave is not None else 0 for chave in tabela_perfeita]
    
    plt.bar(indices, valores, color='skyblue')
    plt.xlabel('Índice da Tabela Hash')
    plt.ylabel('Ocupação (1 = Chave Presente)')
    plt.title("Tabela Hash Perfeita")
    plt.xticks(indices)
    plt.yticks([0, 1])
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, chave in enumerate(tabela_perfeita):
        if chave is not None:
            plt.text(i, 0.5, str(chave), ha='center', va='center', fontweight='bold')

    return plot_to_base64()

def hashing_universal_program():
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def next_prime(n):
        while True:
            n += 1
            if is_prime(n):
                return n

    def universal_hash(k, a, b, p, m):
        return ((a * k + b) % p) % m

    def generate_perfect_hash(chaves):
        p = next_prime(max(chaves))
        m = len(chaves)
        
        for _ in range(1000):
            a = random.randint(1, p-1)
            b = random.randint(0, p-1)
            hash_table = [None] * m
            collision = False

            for k in chaves:
                index = universal_hash(k, a, b, p, m)
                if hash_table[index] is not None:
                    collision = True
                    break
                hash_table[index] = k

            if not collision:
                return hash_table
        raise ValueError("Não foi possível gerar um hash perfeito")

    # Dados
    chaves = [1, 10, 20, 30, 40, 99, 123]
    tabela_perfeita = generate_perfect_hash(chaves)

    # Plotagem
    plt.figure(figsize=(10, 5))
    indices = range(len(tabela_perfeita))
    ocupacao = [1 if chave is not None else 0 for chave in tabela_perfeita]
    
    plt.bar(indices, ocupacao, color='lightgreen')
    plt.xlabel('Índice da Tabela Hash')
    plt.ylabel('Ocupação (1 = Chave Presente)')
    plt.title("Tabela Hash Universal")
    plt.xticks(indices)
    plt.yticks([0, 1])
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, chave in enumerate(tabela_perfeita):
        if chave is not None:
            plt.text(i, 0.5, str(chave), ha='center', va='center', fontweight='bold')

    return plot_to_base64()

def hashing_encadeado_program():
    class No:
        def __init__(self, chave, valor):
            self.chave = chave
            self.valor = valor
            self.proximo = None

    class TabelaHashEncadeamento:
        def __init__(self, tamanho):
            self.tamanho = tamanho
            self.tabela = [None] * tamanho

        def hash(self, chave):
            return chave % self.tamanho

        def inserir(self, chave, valor):
            indice = self.hash(chave)
            no = No(chave, valor)

            if self.tabela[indice] is None:
                self.tabela[indice] = no
            else:
                atual = self.tabela[indice]
                while atual.proximo is not None:
                    atual = atual.proximo
                atual.proximo = no

    # Criação e população da tabela
    tabela = TabelaHashEncadeamento(tamanho=3)
    tabela.inserir(10, "A")
    tabela.inserir(20, "B")
    tabela.inserir(15, "C")
    tabela.inserir(30, "D")

    # Plotagem
    plt.figure(figsize=(10, 5))
    indices = range(tabela.tamanho)
    colisoes = [0] * tabela.tamanho

    for i in indices:
        atual = tabela.tabela[i]
        contador = 0
        while atual is not None:
            contador += 1
            atual = atual.proximo
        colisoes[i] = contador

    bars = plt.bar(indices, colisoes, color='skyblue')
    plt.xlabel('Índice')
    plt.ylabel('Número de Colisões')
    plt.title("Hashing com Encadeamento")
    plt.xticks(indices)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')

    return plot_to_base64()

def hashing_sondagem_program():
    class TabelaHashSondagemLinear:
        def __init__(self, tamanho):
            self.tamanho = tamanho
            self.tabela = [None] * tamanho

        def hash(self, chave):
            return chave % self.tamanho

        def inserir(self, chave, valor):
            indice = self.hash(chave)
            for i in range(self.tamanho):
                novo_indice = (indice + i) % self.tamanho
                if self.tabela[novo_indice] is None or self.tabela[novo_indice] == "DELETADO":
                    self.tabela[novo_indice] = (chave, valor)
                    return
            raise Exception("Tabela cheia!")

    # Criação e população da tabela
    tabela = TabelaHashSondagemLinear(tamanho=7)
    tabela.inserir(10, "João")
    tabela.inserir(20, "Maria")
    tabela.inserir(15, "Carlos")
    tabela.inserir(30, "Ana")

    # Plotagem
    plt.figure(figsize=(10, 6))
    indices = np.arange(tabela.tamanho)
    valores = []
    cores = []

    for entrada in tabela.tabela:
        if entrada is None:
            valores.append(0)
            cores.append('white')
        elif entrada == "DELETADO":
            valores.append(1)
            cores.append('red')
        else:
            valores.append(2)
            cores.append('lightgreen')

    plt.bar(indices, valores, color=cores, edgecolor='black')
    plt.xlabel('Índice da Tabela')
    plt.ylabel('Estado')
    plt.title("Hashing com Sondagem Linear")
    plt.yticks([0, 1, 2], ["Vazio", "DELETADO", "Ocupado"])
    plt.xticks(indices)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, entrada in enumerate(tabela.tabela):
        if entrada not in [None, "DELETADO"]:
            plt.text(i, 1.5, f"{entrada[0]}: {entrada[1]}", ha='center', fontweight='bold')

    return plot_to_base64()

def hashing_duplo_program():
    class TabelaHashDuploHash:
        def __init__(self, tamanho):
            self.tamanho = tamanho
            self.tabela = [None] * tamanho
            self.primo = self._encontrar_primo_menor(tamanho - 1)

        def _encontrar_primo_menor(self, n):
            if n <= 1:
                return 2
            for num in range(n, 1, -1):
                if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
                    return num
            return 2

        def h1(self, chave):
            return chave % self.tamanho

        def h2(self, chave):
            return self.primo - (chave % self.primo)

        def inserir(self, chave, valor):
            indice = self.h1(chave)
            passo = self.h2(chave)

            for i in range(self.tamanho):
                novo_indice = (indice + i * passo) % self.tamanho
                if self.tabela[novo_indice] is None or self.tabela[novo_indice] == "DELETADO":
                    self.tabela[novo_indice] = (chave, valor)
                    return
            raise Exception("Tabela cheia!")

    # Criação e população da tabela
    tabela = TabelaHashDuploHash(tamanho=7)
    tabela.inserir(10, "João")
    tabela.inserir(20, "Maria")
    tabela.inserir(15, "Carlos")
    tabela.inserir(30, "Ana")

    # Plotagem
    plt.figure(figsize=(12, 6))
    indices = np.arange(tabela.tamanho)
    estados = []
    cores = []

    for entrada in tabela.tabela:
        if entrada is None:
            estados.append(0)
            cores.append('white')
        elif entrada == "DELETADO":
            estados.append(1)
            cores.append('red')
        else:
            estados.append(2)
            cores.append('lightgreen')

    plt.bar(indices, estados, color=cores, edgecolor='black', width=0.8)
    plt.xlabel('Índice da Tabela')
    plt.ylabel('Estado')
    plt.title("Hashing Duplo")
    plt.yticks([0, 1, 2], ["Vazio", "DELETADO", "Ocupado"])
    plt.xticks(indices)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, entrada in enumerate(tabela.tabela):
        if entrada not in [None, "DELETADO"]:
            plt.text(i, 1.5, f"{entrada[0]}: {entrada[1]}", ha='center', fontweight='bold')

    for i in range(1, tabela.tamanho):
        if tabela.tabela[i] not in [None, "DELETADO"]:
            h1 = tabela.h1(tabela.tabela[i][0])
            if h1 != i:
                plt.text(i, 2.2, "⚡", ha='center', fontsize=14, color='orange')

    return plot_to_base64()

def plot_to_base64():
    """Função auxiliar para converter plot para base64"""
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.read()).decode('utf-8')