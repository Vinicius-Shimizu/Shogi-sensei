import { useState } from "react";

export default function MovementOptions({
  possible_pieces,
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
      <div className="flex flex-col gap-2 justify-center mt-4 w-[60vw] md:w-[30vw]">
        {exerciseNumber + 1}/{totalExercises} Qual peça pode se mover para as casas destacadas?
        <div className="grid grid-cols-2 gap-2">
          {possible_pieces.map((piece) => (
            <button
              key={piece}
              disabled={answered}
              onClick={() => selectAnswer(piece)}
              className={` 
                px-3 py-2 
                border border-black 
                rounded 
                font-mono 
                transition 
                  ${ selectedAnswer === piece ? "bg-blue-300" : "bg-amber-100" } 
                  disabled:cursor-default
                  w-full
              `}
            >
              {piece}
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
                w-[20vw]
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