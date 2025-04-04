// src/components/trees/AVLTree.tsx
import { useState } from 'react';

// Estrutura de nó da Árvore AVL
class TreeNode {
  value: number;
  left: TreeNode | null;
  right: TreeNode | null;
  height: number;

  constructor(value: number) {
    this.value = value;
    this.left = null;
    this.right = null;
    this.height = 1; // Altura inicial
  }
}

export const AVLTree = () => {
  const [root, setRoot] = useState<TreeNode | null>(null);
  const [inputValue, setInputValue] = useState('');


  // Função para obter a altura de um nó
  const getHeight = (node: TreeNode | null): number => {
    return node ? node.height : 0;
  };

  // Função para calcular o fator de balanceamento de um nó
  const getBalance = (node: TreeNode | null): number => {
    return node ? getHeight(node.left) - getHeight(node.right) : 0;
  };

  // Função para rotacionar à esquerda
  const rotateLeft = (node: TreeNode): TreeNode => {
    const newRoot = node.right!;
    node.right = newRoot.left;
    newRoot.left = node;
    node.height = Math.max(getHeight(node.left), getHeight(node.right)) + 1;
    newRoot.height = Math.max(getHeight(newRoot.left), getHeight(newRoot.right)) + 1;
    return newRoot;
  };

  // Função para rotacionar à direita
  const rotateRight = (node: TreeNode): TreeNode => {
    const newRoot = node.left!;
    node.left = newRoot.right;
    newRoot.right = node;
    node.height = Math.max(getHeight(node.left), getHeight(node.right)) + 1;
    newRoot.height = Math.max(getHeight(newRoot.left), getHeight(newRoot.right)) + 1;
    return newRoot;
  };

  // Função para rotacionar à esquerda e depois à direita
  const rotateLeftRight = (node: TreeNode): TreeNode => {
    node.left = rotateLeft(node.left!);
    return rotateRight(node);
  };

  // Função para rotacionar à direita e depois à esquerda
  const rotateRightLeft = (node: TreeNode): TreeNode => {
    node.right = rotateRight(node.right!);
    return rotateLeft(node);
  };

  // Função para inserir um nó e balancear a árvore
  const insertNode = (node: TreeNode | null, value: number): TreeNode => {
    if (!node) {
      return new TreeNode(value);
    }

    if (value < node.value) {
      node.left = insertNode(node.left, value);
    } else if (value > node.value) {
      node.right = insertNode(node.right, value);
    } else {
      return node; // Não permitir valores duplicados
    }

    node.height = Math.max(getHeight(node.left), getHeight(node.right)) + 1;

    // Balancear a árvore se necessário
    const balance = getBalance(node);

    // Caso 1: Rotação simples à direita
    if (balance > 1 && value < node.left!.value) {
      return rotateRight(node);
    }

    // Caso 2: Rotação simples à esquerda
    if (balance < -1 && value > node.right!.value) {
      return rotateLeft(node);
    }

    // Caso 3: Rotação dupla à esquerda e depois à direita
    if (balance > 1 && value > node.left!.value) {
      return rotateLeftRight(node);
    }

    // Caso 4: Rotação dupla à direita e depois à esquerda
    if (balance < -1 && value < node.right!.value) {
      return rotateRightLeft(node);
    }

    return node;
  };

  // Função para adicionar um nó à árvore AVL
  const handleAddNode = () => {
    if (inputValue) {
      const value = parseInt(inputValue);
      if (!isNaN(value)) {
        const newRoot = insertNode(root, value);
        setRoot(newRoot);
      }
    }
    setInputValue('');
  };

  // Função para renderizar a árvore (em forma simples)
  const renderTree = (node: TreeNode | null) => {
    if (!node) return null;

    return (
      <div className="flex flex-col items-center space-y-4">
        <div className="bg-green-500 text-white p-4 rounded-full">
          <span className="text-lg">{node.value}</span>
        </div>
        <div className="flex space-x-12">
          <div>{renderTree(node.left)}</div>
          <div>{renderTree(node.right)}</div>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h2 className="text-2xl font-semibold text-center mb-6">Árvore AVL</h2>
      <p className='mb-20'> A Árvore AVL é uma variação da árvore binária de busca que se mantém balanceada. Em uma árvore AVL, a diferença entre as alturas das subárvores esquerda e direita de qualquer nó não pode ser maior que 1. Essa restrição garante que a árvore permaneça balanceada, o que ajuda a evitar a degradação do desempenho nas operações de busca, inserção e remoção. Como resultado, a árvore AVL garante que essas operações sejam realizadas em O(log n), mesmo no pior caso, proporcionando maior eficiência em comparação com uma árvore binária de busca não balanceada.</p>
      {/* Input e botão para adicionar um nó */}
      <div className="flex justify-center space-x-4 mb-8">
        <input
          type="number"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Digite um valor"
          className="px-4 py-2 border border-gray-300 rounded-lg"
        />
        <button
          onClick={handleAddNode}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Adicionar Nó
        </button>
      </div>

      {/* Exibir a árvore */}
      <div className="flex justify-center">
        {renderTree(root)}
      </div>
    </div>
  );
};
