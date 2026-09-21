import Result from "./Result";

export default function ResultsPage({result, onRestart}){
    console.log(result);
    return (
      <div>
        <h2 className="mt-5">Resultados</h2>

        <div className="flex justify-center">
          <div className="grid grid-cols-[80px_150px_200px_200px_1fr] py-4 border-2 text-lg px-4">
            <div>Questão</div>
            <div>Módulo</div>
            <div>Resposta</div>
            <div>Resposta Esperada</div>
            <div>Explicação</div>
            {result.results.map((exerciseResult, index) => (
              <Result key={exerciseResult.exercise_id} index={index + 1} result={exerciseResult}></Result>
            ))}
          </div>
        </div>
        
        <button onClick={onRestart}>Começar outra lista</button>
      </div>
    );
}