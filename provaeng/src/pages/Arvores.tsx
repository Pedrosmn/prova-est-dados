import { useTree } from '../contexts/TreeContext';
import { AVLTree } from '../components/trees/AVLTree';
import { BSTTree } from '../components/trees/BSTTree';
import { BTree } from '../components/trees/BTree';
import { FibonacciTree } from '../components/trees/FibonacciTree';

export default function Arvores() {
  const { selectedTree, setSelectedTree } = useTree();

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold my-4">Escolha um Tipo de Árvore</h1>
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        <button 
          onClick={() => setSelectedTree('BST')} 
          className={`px-4 py-2 rounded-lg ${selectedTree === 'BST' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
        >
          Árvore Binária de Busca
        </button>
        <button 
          onClick={() => setSelectedTree('AVL')} 
          className={`px-4 py-2 rounded-lg ${selectedTree === 'AVL' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
        >
          Árvore AVL
        </button>
        <button 
          onClick={() => setSelectedTree('BTree')} 
          className={`px-4 py-2 rounded-lg ${selectedTree === 'BTree' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
        >
          Árvore B
        </button>
        <button 
          onClick={() => setSelectedTree('Fibonacci')} 
          className={`px-4 py-2 rounded-lg ${selectedTree === 'Fibonacci' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
        >
          Árvore de Fibonacci
        </button>
      </div>

      <div className="w-full max-w-4xl">
        {selectedTree === 'BST' && <BSTTree />}
        {selectedTree === 'AVL' && <AVLTree />}
        {selectedTree === 'BTree' && <BTree />}
        {selectedTree === 'Fibonacci' && <FibonacciTree />}
      </div>
    </div>
  );
}