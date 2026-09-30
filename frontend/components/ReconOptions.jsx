import { useState } from "react";

export default function ReconOptions({
  position,
  possible_moves,
  onAnswer,
  exerciseNumber,
  totalExercises
}) {
  const [answered, setAnswered] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  function selectAnswer(answer) {
    setSelectedAnswer(answer);
    setAnswered(true);
    console.log(answer);
  }

  function handleNext() {
    onAnswer(selectedAnswer);
  }
  
  const isLastExercise = exerciseNumber + 1 === totalExercises;
  
  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-2 justify-center mt-4 w-[30vw]">
        {exerciseNumber + 1}/{totalExercises} Qual é a peça na posição {position}?
        <div className="grid grid-cols-2 gap-2">
          {possible_moves.map((move) => (
            <button
              key={move}
              disabled={answered}
              onClick={() => selectAnswer(move)}
              className={` 
                px-3 py-2 
                border border-black 
                rounded 
                font-mono 
                transition 
                ${ selectedAnswer === move ? "bg-blue-300" : "bg-amber-100" } 
                disabled:cursor-default
                w-full
              `}
            >
              {move}
            </button>
          ))}
        </div>
        <div className="flex justify-center">
          {answered && (
            <button
              onClick={handleNext}
              className="
                mt-2
                px-3 py-1
                bg-green-200
                border border-black
                rounded
                w-[10vw]
              "
            >
              {isLastExercise ? "Finalizar lista" : "Próximo exercício"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}