import { createContext, useContext, useState, ReactNode } from 'react';

interface TreeContextProps {
  selectedTree: string;
  setSelectedTree: (tree: string) => void;
}

const TreeContext = createContext<TreeContextProps | undefined>(undefined);

export const TreeProvider = ({ children }: { children: ReactNode }) => {
  const [selectedTree, setSelectedTree] = useState('BST');  // Default to Binary Search Tree

  return (
    <TreeContext.Provider value={{ selectedTree, setSelectedTree }}>
      {children}
    </TreeContext.Provider>
  );
};

export const useTree = () => {
  const context = useContext(TreeContext);
  if (!context) {
    throw new Error('useTree must be used within a TreeProvider');
  }
  return context;
};
