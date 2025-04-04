import { createContext, useContext, useState, ReactNode } from "react";

interface HashContextProps {
  selectedHash: string;
  setSelectedHash: (hash: string) => void;
}

const HashContext = createContext<HashContextProps | undefined>(undefined);

export const HashProvider = ({ children }: { children: ReactNode }) => {
  const [selectedHash, setSelectedHash] = useState("HashingDuplo");

  return (
    <HashContext.Provider value={{ selectedHash, setSelectedHash }}>
      {children}
    </HashContext.Provider>
  );
};

export const useHash = () => {
  const context = useContext(HashContext);
  if (!context) {
    throw new Error("useHash must be used within a HashProvider");
  }
  return context;
};