import Result from "./Result";
import { useNavigate, useLocation } from "react-router-dom";

export default function ResultsPage(){
  const navigate = useNavigate();
  const locate = useLocation();
  const result = locate.state?.result;
  if (!result) {
  return (
    <div className="flex flex-col items-center mt-6 min-h-screen w-full bg-black">
      <p>Nenhum resultado disponível.</p>

      <button onClick={() => navigate("exercise-list")} className="flex-col border-2 bg-slate-600 rounded-xl w-[80vw] md:w-[30vw] mt-8">Começar uma lista</button>

    </div>
  );
}

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-black">
      <h2 className="mt-5">Resultados</h2>

      <div className="w-[95vw] md:w-[80vw] overflow-x-auto border-2 mt-4">
        <div className="grid grid-cols-[50px_1fr_1fr_1fr_1.5fr] p-4 text-lg">
          <div className="flex items-center justify-center p-2">
            Questão
          </div>

          <div className="flex items-center justify-center p-2">
            Módulo
          </div>

          <div className="flex items-center justify-center p-2">
            Resposta
          </div>

          <div className="flex items-center justify-center p-2">
            Resposta Esperada
          </div>

          <div className="flex items-center justify-center p-2">
            Explicação
          </div>
          {result.results.map((exerciseResult, index) => (
            <Result key={exerciseResult.exercise_id} index={index + 1} result={exerciseResult}></Result>
          ))}
        </div>
      </div>
      
      <button onClick={() => navigate("/exercise-list")} className="border-2 bg-slate-600 rounded-xl w-[80vw] md:w-[30vw] mt-8 py-2">Começar outra lista</button>
      <button onClick={() => navigate("/")} className="border-2 bg-slate-600 rounded-xl w-[80vw] md:w-[30vw] mt-2 py-2">Home</button>
      
    </div>
  );
}