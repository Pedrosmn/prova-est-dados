export const fetchAlgorithms = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/algorithms");
      if (!response.ok) {
        throw new Error("Erro ao buscar os algoritmos");
      }
      return await response.json();
    } catch (error) {
      console.error(error);
      return [];
    }
  };
  