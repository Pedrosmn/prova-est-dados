
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.js'
import { HashProvider } from "./contexts/HashContext";
import { ListProvider } from './contexts/ListsContext.js';

createRoot(document.getElementById('root')!).render(
  <ListProvider>
  <HashProvider>
    <App />
    </HashProvider>
    </ListProvider>,
)