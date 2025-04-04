import { useState } from 'react';

export const SkipLists = () => {
  const [inputValue, setInputValue] = useState('');
  const [searchValue, setSearchValue] = useState('');
  const [maxLevel, setMaxLevel] = useState(4);
  const [listImage, setListImage] = useState('');

  const handleSearch = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate_list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listType: 'skip_list',
          operation: 'search',
          search_value: parseInt(searchValue),
          max_level: maxLevel
        })
      });
      const data = await response.json();
      setListImage(data.image);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleInsert = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate_list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listType: 'skip_list',
          operation: 'insert',
          insert_values: [parseInt(inputValue)],
          max_level: maxLevel
        })
      });
      const data = await response.json();
      setListImage(data.image);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Skip Lists</h2>
      
      <div className="mb-6">
        <label className="block mb-2">Nível Máximo</label>
        <input
          type="number"
          value={maxLevel}
          onChange={(e) => setMaxLevel(parseInt(e.target.value) || 4)}
          min="1"
          max="10"
          className="w-full p-2 border rounded"
        />
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

      {listImage && (
        <div className="mt-6">
          <img 
            src={`data:image/png;base64,${listImage}`} 
            alt="Visualização da Skip List"
            className="mx-auto border rounded"
          />
        </div>
      )}
    </div>
  );
};