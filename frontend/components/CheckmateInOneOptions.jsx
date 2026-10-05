import { useState } from "react";

export default function CheckmateInOneOptions({
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
  }

  function handleNext() {
    onAnswer(selectedAnswer);
  }
  const isLastExercise = exerciseNumber + 1 === totalExercises;

  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-2 items-center justify-center mt-4 w-[60vw] md:w-[30vw]">
        <p className="text-center">{exerciseNumber + 1}/{totalExercises} Qual movimento abaixo leva ao chequemate?</p>
        <div className="grid grid-cols-2 gap-2">
          {possible_moves.map((move) => (
            <button
              key={move}
              disabled={answered}
              onClick={() => selectAnswer(move)}
              className={` 
                px-3 py-2 
                border border-black 
                rounded-lg 
                font-mono 
                transition 
                ${selectedAnswer === null ? "bg-wood" : `${ selectedAnswer === move ? "bg-blue-300" : "bg-wood-500" }`}
                disabled:cursor-default
                w-full
                text-black
              `}
            >
              {move.slice(0, 2) + (move.includes("*") ? "" : "->") + move.slice(2)}
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
              border border-black
              rounded-lg
              bg-wood
              text-black
              w-full
              whitespace-nowrap
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