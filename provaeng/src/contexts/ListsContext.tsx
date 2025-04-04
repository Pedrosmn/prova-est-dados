import { createContext, useContext, useState, ReactNode } from 'react';

interface ListContextProps {
  selectedList: string;
  setSelectedList: (list: string) => void;
}

const ListContext = createContext<ListContextProps | undefined>(undefined);

export const ListProvider = ({ children }: { children: ReactNode }) => {
  const [selectedList, setSelectedList] = useState('ListaAutoOrganizaveis');

  return (
    <ListContext.Provider value={{ selectedList, setSelectedList }}>
      {children}
    </ListContext.Provider>
  );
};

export const useList = () => {
  const context = useContext(ListContext);
  if (!context) {
    throw new Error('useList must be used within a ListProvider');
  }
  return context;
};