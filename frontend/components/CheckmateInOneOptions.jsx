import { useState } from "react";

export default function CheckmateInOneOptions({
  possible_moves,
  onAnswer,
  exerciseNumber,
  totalExercises
}) {
  const [selectedAnswer, setSelectedAnswer] = useState(null);

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
              onClick={() => setSelectedAnswer(move)}
              className={` 
                px-2 py-2
                border border-black
                rounded
                font-mono
                text-sm sm:text-base
                whitespace-normal
                break-words
                min-w-0
                w-full
                h-full
                min-h-16
                text-center
                text-black
                transition
                ${selectedAnswer === move
                    ? "bg-blue-300"
                    : "bg-wood"
                }
                disabled:cursor-default
              `}
            >
              {move.slice(0, 2) + (move.includes("*") ? "" : "->") + move.slice(2)}
            </button>
          ))}
        </div>
        <div className="flex justify-center">
          {selectedAnswer && (<button
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
          </button>)}
        </div>
      </div>
    </div>
  );
}