import { useState } from 'react';

export const BSTTree = () => {
  const [nNodes, setNNodes] = useState<number>(10);
  const [searchNum, setSearchNum] = useState<number | null>(null);
  const [addNodes, setAddNodes] = useState<string>('');
  const [treeImage, setTreeImage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const generateTree = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/generate_tree', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          treeType: 'BST',
          value: nNodes,
          searchNum: searchNum,
          addNodes: addNodes ? addNodes.split(',').map(Number) : null
        }),
      });

      const data = await response.json();
      setTreeImage(`data:image/png;base64,${data.image}`);
    } catch (error) {
      console.error('Error:', error);
      alert('Erro ao gerar árvore');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      <h2 className="text-2xl font-semibold text-center mb-6">Árvore Binária de Busca</h2>
      <p className='mb-6'>
        A Árvore Binária de Busca (BST) é uma estrutura de dados onde cada nó possui no máximo dois filhos...
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block mb-2">Número de Nós</label>
          <input
            type="number"
            value={nNodes}
            onChange={(e) => setNNodes(Number(e.target.value))}
            className="w-full p-2 border rounded"
            min="1"
          />
        </div>

        <div>
          <label className="block mb-2">Buscar Nó (opcional)</label>
          <input
            type="number"
            value={searchNum || ''}
            onChange={(e) => setSearchNum(e.target.value ? Number(e.target.value) : null)}
            className="w-full p-2 border rounded"
            placeholder="Número para buscar"
          />
        </div>

        <div>
          <label className="block mb-2">Adicionar Nós (opcional)</label>
          <input
            type="text"
            value={addNodes}
            onChange={(e) => setAddNodes(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Ex: 5,10,15"
          />
        </div>
      </div>

      <div className="flex justify-center mb-8">
        <button
          onClick={generateTree}
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Gerando...' : 'Gerar Árvore'}
        </button>
      </div>

      {treeImage && (
        <div className="flex justify-center border rounded-lg p-4 bg-white shadow">
          <img 
            src={treeImage} 
            alt="Árvore BST" 
            className="max-w-full h-auto" 
          />
        </div>
      )}
    </div>
  );
};