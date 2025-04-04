import { HashingEncadeado } from "../components/hashs/HashingEncadeado";
import { HashingPerfeito } from "../components/hashs/HashingPerfeito";
import { HashingSondagem } from "../components/hashs/HashingSondagem";
import { HashingUniversal } from "../components/hashs/HashingUniversal";
import { useHash } from "../contexts/HashContext";

export default function Hashing() {
  const { selectedHash, setSelectedHash } = useHash();

  return (
    <div className="flex flex-col items-center">
      <h1 className="text-3xl font-bold my-4">Escolha um Tipo de Hash</h1>
      <div className="flex space-x-4">
   
        <button onClick={() => setSelectedHash('HashingEncadeado')} className="btn">
          Hashing Encadeado
        </button>
        <button onClick={() => setSelectedHash('HashingPerfeito')} className="btn">
          Hashing Perfeito
        </button>
        <button onClick={() => setSelectedHash('HashingSondagem')} className="btn">
          Hashing Sondagem
        </button>
        <button onClick={() => setSelectedHash('HashingUniversal')} className="btn">
          Hashing Universal
        </button>
      </div>

      <div className="mt-8">
        {selectedHash === 'HashingEncadeado' && <HashingEncadeado />}
        {selectedHash === 'HashingPerfeito' && <HashingPerfeito />}
        {selectedHash === 'HashingSondagem' && <HashingSondagem />}
        {selectedHash === 'HashingUniversal' && <HashingUniversal />}
      </div>
    </div>
  );
}