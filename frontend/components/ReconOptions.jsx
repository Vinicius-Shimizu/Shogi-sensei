import { useState } from "react";

export default function ReconOptions({
  position,
  possible_pieces,
  onAnswer,
  exerciseNumber,
  totalExercises
}) {
  const [answered, setAnswered] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  let PIECES_DICT = {
      "P": "Peão",
      "L": "Lança",
      "N": "Cavalo",
      "S": "General de Prata",
      "B": "Bispo",
      "R": "Torre",
      "G": "General de Ouro",
      "K": "Rei",
      "+P": "Peão Promovido",
      "+L": "Lança Promovida",
      "+N": "Cavalo Promovido",
      "+S": "General de Prata Promovido",
      "+B": "Bispo Promovido",
      "+R": "Torre Promovida",
  }
  PIECES_DICT = Object.fromEntries(
    Object.entries(PIECES_DICT).map(([key, val]) => [val, key])
  );

  // Instant O(1) lookup
  console.log(PIECES_DICT); // Output: "b"


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
        <p className="text-center">{exerciseNumber + 1}/{totalExercises} Qual é a peça na posição {position}?</p>
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
                ${selectedAnswer === null ? "bg-wood" : `${ selectedAnswer === piece ? "bg-blue-300" : "bg-wood-500" }`}
                disabled:cursor-default
                w-full
                text-black
              `}
            >
              {piece + "(" + PIECES_DICT[piece] + ")"} 
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