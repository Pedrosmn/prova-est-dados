import { useState } from 'react';

export const HashingPerfeito = () => {
        const [hashingImage, setHashingImage] = useState<string | null>(null);
        const [loading, setLoading] = useState<boolean>(false);
    
        const generateHashing = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/generate_hashing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                hashingType: 'Perfeito'
            }),
            });
    
            if (!response.ok) {
            throw new Error('Erro ao gerar hashing');
            }
    
            const data = await response.json();
            setHashingImage(`data:image/png;base64,${data.image}`);
            
        } catch (error) {
            console.error('Erro:', error);
            alert('Falha ao gerar visualização do hashing');
        } finally {
            setLoading(false);
        }
        };
    
    return(
        <div className="max-w-4xl mx-auto py-8">
          <h2 className="text-2xl font-semibold text-center mb-6">Hashing Perfeito</h2>
          <p className='mb-20'>O hashing perfeito é uma técnica que busca eliminar colisões completamente, garantindo que cada chave tenha um endereço único na tabela hash. Isso é alcançado através de um processo de pré-computação que utiliza funções hash específicas, criando uma estrutura onde as colisões nunca ocorrem. Apesar de ser extremamente eficiente em termos de busca (O(1)), sua construção pode ser complexa e demorada, especialmente quando o conjunto de chaves é dinâmico.


    
            </p>
            <div className="flex justify-center mb-8">
        <button
          onClick={generateHashing}
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Gerando...' : 'Gerar Hashing'}
        </button>
      </div>

      {hashingImage && (
        <div className="mt-6 flex justify-center border rounded-lg p-4 bg-white shadow">
          <img 
            src={hashingImage} 
            alt="Visualização do Hashing Duplo" 
            className="max-w-full h-auto" 
          />
        </div>
      )}
    </div>
  );
};