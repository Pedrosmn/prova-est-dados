import { useState } from 'react';
import { ListasAutoOrganizadas } from '../components/lists/ListasAutoOrganizaveis';
import { SkipLists } from '../components/lists/SkipLists';

export default function Listas() {
  const [selectedList, setSelectedList] = useState<'auto' | 'skip'>('auto');

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold my-4">Visualizador de Estruturas de Dados</h1>
      
      <div className="flex space-x-4 mb-8">
        <button 
          onClick={() => setSelectedList('auto')} 
          className={`px-4 py-2 rounded-lg ${
            selectedList === 'auto' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-200 hover:bg-gray-300'
          }`}
        >
          Listas Auto-Organizáveis
        </button>
      </div>

      <div className="w-full max-w-4xl">
        {selectedList === 'auto' && <ListasAutoOrganizadas />}
        {selectedList === 'skip' && <SkipLists />}
      </div>
    </div>
  );
}