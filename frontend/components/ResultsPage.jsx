import Result from "./Result";
import { useNavigate, useLocation } from "react-router-dom";

export default function ResultsPage(){
  const navigate = useNavigate();
  const locate = useLocation();
  const result = locate.state?.result;
  if (!result) {
  return (
    <div className="flex flex-col items-center mt-6 bg-black">
      <p>Nenhum resultado disponível.</p>

      <button onClick={() => navigate("exercise-list")} className="flex-col border-2 bg-slate-600 rounded-xl w-[30%] h-[10%] mt-8">Começar uma lista</button>

    </div>
  );
}

  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full bg-black">
      <h2 className="mt-5">Resultados</h2>

      <div className="flex justify-center items-center">
        <div className="grid grid-cols-[80px_150px_200px_200px_1fr] p-4 border-2 text-lg">
          <div>Questão</div>
          <div>Módulo</div>
          <div>Resposta</div>
          <div>Resposta Esperada</div>
          <div className="mr-4">Explicação</div>
          {result.results.map((exerciseResult, index) => (
            <Result key={exerciseResult.exercise_id} index={index + 1} result={exerciseResult}></Result>
          ))}
        </div>
      </div>
      
      <button onClick={() => navigate("/exercise-list")} className="flex-col border-2 bg-slate-600 rounded-xl w-[10%] h-[10%] mt-8">Começar outra lista</button>
      <button onClick={() => navigate("/")} className="flex-col border-2 bg-slate-600 rounded-xl w-[10%] h-[10%] mt-2">Home</button>
      
    </div>
  );
}