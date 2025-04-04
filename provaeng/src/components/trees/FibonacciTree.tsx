import { useState } from 'react';

// Estrutura de nó da Árvore de Fibonacci
class FibonacciTreeNode {
  value: number;
  left: FibonacciTreeNode | null;
  right: FibonacciTreeNode | null;

  constructor(value: number) {
    this.value = value;
    this.left = null;
    this.right = null;
  }
}

export const FibonacciTree = () => {
  const [root, setRoot] = useState<FibonacciTreeNode | null>(null);
  const [inputValue, setInputValue] = useState('');

  // Função para gerar o número de Fibonacci
  const fibonacci = (n: number): number => {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
  };

  // Função para inserir um valor na árvore de Fibonacci
  const insertNode = (root: FibonacciTreeNode | null, value: number): FibonacciTreeNode => {
    if (!root) {
      return new FibonacciTreeNode(value);
    }

    if (value < root.value) {
      root.left = insertNode(root.left, value);
    } else if (value > root.value) {
      root.right = insertNode(root.right, value);
    }

    return root;
  };

  // Função para adicionar o valor à árvore
  const handleAddNode = () => {
    if (inputValue) {
      const value = parseInt(inputValue);
      if (!isNaN(value)) {
        const newValue = fibonacci(value);
        const newRoot = insertNode(root, newValue);
        setRoot(newRoot);
      }
    }
    setInputValue('');
  };

  // Função para renderizar a árvore (em forma simples)
  const renderTree = (node: FibonacciTreeNode | null) => {
    if (!node) return null;

    return (
      <div className="flex flex-col items-center space-y-4">
        <div className="bg-blue-500 text-white p-4 rounded-full">
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
      <h2 className="text-2xl font-semibold text-center mb-6">Árvore de Fibonacci</h2>
      <p className='mb-20'> A Árvore de Fibonacci é uma estrutura de dados baseada na sequência de Fibonacci e é usada para representar uma estrutura de heap, conhecida como "Fibonacci heap". Essa árvore permite operações eficientes como a inserção de elementos, a remoção do mínimo e a união de árvores, todas com complexidade amortizada O(1). O principal benefício dessa árvore é a eficiência nas operações de união e remoção, que são mais rápidas em comparação com outras implementações de heap.</p>
      {/* Input e botão para adicionar um nó */}
      <div className="flex justify-center space-x-4 mb-8">
        <input
          type="number"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Digite um índice de Fibonacci"
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
