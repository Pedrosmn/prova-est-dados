import { useState } from 'react';
import { Link } from 'react-router-dom';

export const NavBar = () => {
  // Estado para controlar se a sidebar está aberta ou fechada
  const [isOpen, setIsOpen] = useState(false);

  // Função para alternar o estado da sidebar
  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex">
      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full bg-blue-600 p-4 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out`}
      >
        <div className="mt-20 ">
          <Link to="/" className="text-white  font-semibold pt-20 ">Início</Link>
          <br />
          <br />
          <Link to="/arvores" className="text-white">Árvores</Link>
          <br />
          <br />
          <Link to="/hashing" className="text-white">Hashing</Link>
          <br />
          <br />
          <Link to="/list" className="text-white">Listas encadeadas</Link>
        </div>
      </div>

      {/* Botão para abrir/fechar a sidebar */}
      <button
        onClick={toggleSidebar}
        className="p-4 fixed top-4 left-4 z-50 text-white bg-blue-600 rounded-md"
      >
        {isOpen ? 'X' : '☰'}
      </button>
    </div>
  );
};