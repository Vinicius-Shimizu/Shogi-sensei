import { useState } from "react";

export default function DropOptions({
  possible_drops,
  onAnswer,
  exerciseNumber,
  totalExercises
}) {
  const [answered, setAnswered] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  let PIECES_DICT = {
      "P": "o Peão",
      "L": "a Lança",
      "N": "o Cavalo",
      "S": "o General de Prata",
      "B": "o Bispo",
      "R": "a Torre",
      "G": "o General de Ouro",
      "+P": "o Peão Promovido",
      "+L": "a Lança Promovida",
      "+N": "o Cavalo Promovido",
      "+S": "o General de Prata Promovido",
      "+B": "o Bispo Promovido",
      "+R": "a Torre Promovida",
  }

  function selectAnswer(answer) {
    setSelectedAnswer(answer);
    setAnswered(true);
  }

  function handleNext() {
    onAnswer(selectedAnswer);
  }
  const isLastExercise = exerciseNumber + 1 === totalExercises;
  const piece = PIECES_DICT[possible_drops[0][0]]
  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-2 items-center justify-center mt-4 w-[60vw] md:w-[30vw]">
        <p className="text-center">{exerciseNumber + 1}/{totalExercises} Qual é a casa do tabuleiro na qual você pode corretamente posicionar {piece} da sua mão?</p>
        <div className="grid grid-cols-2 gap-2">
          {possible_drops.map((drop) => (
            <button
              key={drop}
              disabled={answered}
              onClick={() => selectAnswer(drop)}
              className={` 
                px-3 py-2 
                border border-black 
                rounded-lg 
                font-mono 
                transition 
                ${selectedAnswer === null ? "bg-wood" : `${ selectedAnswer === drop ? "bg-blue-300" : "bg-wood-500" }`}
                disabled:cursor-default
                w-full
                text-black
              `}
            >
              {drop}
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