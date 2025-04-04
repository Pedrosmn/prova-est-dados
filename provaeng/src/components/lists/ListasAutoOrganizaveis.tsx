import { useState, useEffect } from 'react';

export const ListasAutoOrganizadas = () => {
  const [inputValue, setInputValue] = useState('');
  const [searchValue, setSearchValue] = useState('');
  const [listSize, setListSize] = useState(10);
  const [listType, setListType] = useState('move_to_front');
  const [listImages, setListImages] = useState<string[]>([]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [listDescription, setListDescription] = useState('');

  const goToPrevStep = (): void => {
    setCurrentImageIndex((prevIndex) => 
      (prevIndex - 1 + listImages.length) % listImages.length
    );
    setIsPlaying(false);
  };
  
  const goToNextStep = (): void => {
    setCurrentImageIndex((prevIndex) => 
      (prevIndex + 1) % listImages.length
    );
    setIsPlaying(false);
  };
  
  const togglePlayPause = (): void => {
    setIsPlaying((prev) => !prev);
  };

  // Efeito para controlar a animação
  useEffect(() => {
    let interval: number;
    
    if (isPlaying && listImages.length > 0) {
      interval = window.setInterval(() => {
        setCurrentImageIndex(prev => (prev + 1) % listImages.length);
      }, 1000);
    }
    
    return () => window.clearInterval(interval);
  }, [isPlaying, listImages]);

  const handleSearch = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate_list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listType,
          operation: 'search',
          value: parseInt(searchValue),
          size: listSize
        })
      });
  
      if (!response.ok) {
        throw new Error(`Erro HTTP! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      if (data?.images?.length > 0) {
        setListImages(data.images);
        setCurrentImageIndex(0);
        setIsPlaying(true);
        setListDescription(data.list || 'Busca realizada');
      } else if (data?.image) {
        setListImages([data.image]);
        setIsPlaying(false);
        setListDescription(data.list || 'Lista visualizada');
      } else {
        throw new Error('Resposta inválida do servidor');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
      console.error('Error:', error);
      alert(`Erro ao buscar valor: ${errorMessage}`);
      setListImages([]);
    }
  };
  
  const handleInsert = async () => {
    try {
      const numericValue = parseInt(inputValue);
      if (isNaN(numericValue)) {
        throw new Error("Por favor, insira um número válido");
      }
  
      const response = await fetch('http://localhost:5000/generate_list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listType,
          operation: 'insert',
          items: [numericValue],
          size: listSize
        })
      });
  
      const data = await response.json();
  
      if (!response.ok || data.error) {
        throw new Error(data.error || "Erro no servidor");
      }
  
      if (!data.image) {
        // Se não veio image, tenta usar a primeira de images (se existir)
        const imageToUse = data.image || data.images?.[0];
        if (!imageToUse) {
          throw new Error("Nenhuma imagem foi retornada");
        }
        setListImages([imageToUse]);
      } else {
        setListImages([data.image]);
      }
  
      setListDescription(data.list || `Valor ${numericValue} inserido`);
      setInputValue('');
  
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Erro desconhecido";
      console.error("Erro na inserção:", error);
      alert(`Falha ao inserir: ${errorMessage}`);
      setListImages([]);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Listas Auto-Organizáveis</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block mb-2">Tipo de Lista</label>
          <select
            value={listType}
            onChange={(e) => setListType(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="move_to_front">Move-to-Front</option>
            <option value="transpose">Transpose</option>
          </select>
        </div>
        
        <div>
          <label className="block mb-2">Tamanho da Lista</label>
          <input
            type="number"
            value={listSize}
            onChange={(e) => setListSize(parseInt(e.target.value) || 10)}
            className="w-full p-2 border rounded"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block mb-2">Valor para Inserir</label>
          <input
            type="number"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="w-full p-2 border rounded"
          />
          <button
            onClick={handleInsert}
            className="mt-2 w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Inserir Valor
          </button>
        </div>
        
        <div>
          <label className="block mb-2">Valor para Buscar</label>
          <input
            type="number"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            className="w-full p-2 border rounded"
          />
          <button
            onClick={handleSearch}
            className="mt-2 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Buscar Valor
          </button>
        </div>
      </div>

      {listImages.length > 0 && (
        <div className="mt-6">
          <div className="flex justify-center mb-4">
            <img 
              src={`data:image/png;base64,${listImages[currentImageIndex]}`} 
              alt="Visualização da Lista"
              className="max-w-full h-auto border rounded"
            />
          </div>
          
          {/* Controles de animação */}
          <div className="flex justify-center space-x-4 mt-4">
            <button
                onClick={() => goToPrevStep()}
                className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
            >
                Anterior
            </button>
            
            <button
                onClick={() => togglePlayPause()}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-purple-700"
            >
                {isPlaying ? 'Pausar' : 'Reproduzir'}
            </button>
            
            <button
                onClick={() => goToNextStep()}
                className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
            >
                Próximo
            </button>
            </div>
          
          {/* Descrição */}
          <div className="mt-4 p-4 bg-gray-100 rounded-lg">
            <p>{listDescription}</p>
          </div>
        </div>
      )}
    </div>
  );
};