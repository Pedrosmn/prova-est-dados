import { useState } from "react";

export const Trees = () => {
  const [selectedTree, setSelectedTree] = useState<string>("BST");
  const [treeImage, setTreeImage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  
  // Parâmetros para todas as árvores
  const [nNodes, setNNodes] = useState<number>(5); // Para BST, AVL e Fibonacci
  const [degree, setDegree] = useState<number>(2); // Para BTree
  const [searchNum, setSearchNum] = useState<number | null>(null); // Para BST e BTree
  const [addNodes, setAddNodes] = useState<string>(""); // Para BST e BTree

  const generateTree = async () => {
    setLoading(true);
    try {
      const requestBody: any = { treeType: selectedTree };

      switch(selectedTree) {
        case "BST":
          requestBody.value = nNodes;
          requestBody.searchNum = searchNum;
          requestBody.addNodes = addNodes ? addNodes.split(',').map(Number) : null;
          break;
          
        case "AVL":
          requestBody.value = nNodes;
          break;
          
        case "BTree":
          requestBody.degree = degree;
          requestBody.searchNum = searchNum;
          requestBody.addNum = addNodes ? addNodes.split(',').map(Number) : null;
          break;
          
        case "Fibonacci":
          requestBody.value = Math.min(7, Math.max(1, nNodes));
          break;
      }

      const response = await fetch("http://127.0.0.1:5000/generate_tree", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error("Erro ao gerar a árvore");
      }

      const data = await response.json();
      setTreeImage(`data:image/png;base64,${data.image}`);
      
    } catch (error) {
      console.error("Erro detalhado:", error);
      alert(`Erro: ${error instanceof Error ? error.message : "Erro desconhecido"}`);
    } finally {
      setLoading(false);
    }
  };

  const renderInputs = () => {
    switch(selectedTree) {
      case "BST":
        return (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="flex flex-col items-center">
              <label className="mb-2">Número de Nós</label>
              <input
                type="number"
                value={nNodes}
                onChange={(e) => setNNodes(Number(e.target.value))}
                className="border border-gray-300 rounded px-4 py-2 w-32 text-center"
                min="1"
              />
            </div>
            <div className="flex flex-col items-center">
              <label className="mb-2">Buscar Nó (opcional)</label>
              <input
                type="number"
                value={searchNum || ''}
                onChange={(e) => setSearchNum(e.target.value ? Number(e.target.value) : null)}
                className="border border-gray-300 rounded px-4 py-2 w-32 text-center"
                placeholder="Número"
              />
            </div>
            <div className="flex flex-col items-center">
              <label className="mb-2">Adicionar Nós (opcional)</label>
              <input
                type="text"
                value={addNodes}
                onChange={(e) => setAddNodes(e.target.value)}
                className="border border-gray-300 rounded px-4 py-2 w-64 text-center"
                placeholder="Ex: 5,10,15"
              />
            </div>
          </div>
        );
        
      case "AVL":
        return (
          <div className="flex justify-center mb-6">
            <div className="flex flex-col items-center">
              <label className="mb-2">Número de Nós</label>
              <input
                type="number"
                value={nNodes}
                onChange={(e) => setNNodes(Number(e.target.value))}
                className="border border-gray-300 rounded px-4 py-2 w-32 text-center"
                min="1"
              />
            </div>
          </div>
        );
        
      case "BTree":
        return (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="flex flex-col items-center">
              <label className="mb-2">Grau da Árvore (t)</label>
              <input
                type="number"
                value={degree}
                onChange={(e) => setDegree(Number(e.target.value))}
                className="border border-gray-300 rounded px-4 py-2 w-32 text-center"
                min="2"
              />
            </div>
            <div className="flex flex-col items-center">
              <label className="mb-2">Buscar Nó (opcional)</label>
              <input
                type="number"
                value={searchNum || ''}
                onChange={(e) => setSearchNum(e.target.value ? Number(e.target.value) : null)}
                className="border border-gray-300 rounded px-4 py-2 w-32 text-center"
                placeholder="Número"
              />
            </div>
            <div className="flex flex-col items-center">
              <label className="mb-2">Adicionar Nós (opcional)</label>
              <input
                type="text"
                value={addNodes}
                onChange={(e) => setAddNodes(e.target.value)}
                className="border border-gray-300 rounded px-4 py-2 w-64 text-center"
                placeholder="Ex: 5,10,15"
              />
            </div>
          </div>
        );
        
      case "Fibonacci":
        return (
          <div className="flex justify-center mb-6">
            <div className="flex flex-col items-center">
              <label className="mb-2">Número Fibonacci (1-7)</label>
              <input
                type="number"
                value={nNodes}
                onChange={(e) => setNNodes(Math.min(7, Math.max(1, Number(e.target.value))))}
                className="border border-gray-300 rounded px-4 py-2 w-32 text-center"
                min="1"
                max="7"
              />
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-semibold text-center mb-6">
        Escolha um Tipo de Árvore
      </h1>

      {/* Botões para selecionar o tipo de árvore */}
      <div className="flex justify-center space-x-4 mb-6">
        {["BST", "AVL", "Fibonacci", "BTree"].map((tree) => (
          <button
            key={tree}
            onClick={() => setSelectedTree(tree)}
            className={`px-6 py-2 rounded-lg text-white transition ${
              selectedTree === tree ? "bg-gray-700" : "bg-blue-500 hover:bg-blue-600"
            }`}
          >
            {tree}
          </button>
        ))}
      </div>

      {/* Renderiza os inputs específicos para cada árvore */}
      {renderInputs()}

      <div className="flex justify-center mb-8">
        <button
          onClick={generateTree}
          className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 disabled:bg-gray-400"
          disabled={loading}
        >
          {loading ? "Gerando..." : "Gerar Árvore"}
        </button>
      </div>

      {/* Exibição da árvore gerada */}
      {treeImage && (
        <div className="mt-6 flex justify-center">
          <img
            src={treeImage}
            alt={`Árvore ${selectedTree}`}
            className="border border-gray-400 rounded-lg shadow-lg max-w-full"
          />
        </div>
      )}
    </div>
  );
};