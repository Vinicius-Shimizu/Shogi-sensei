import { useState } from "react";

export default function MovementOptions({
  possible_pieces,
  onAnswer,
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

  return (
    <div className="flex justify-center w-70">
      <div className="flex flex-col gap-2 justify-center mt-4 w-30">
        Qual peça pode se mover para as casas destacadas?
        
        {possible_pieces.map((piece) => (
          <button
            key={piece}
            disabled={answered}
            onClick={() => selectAnswer(piece)}
            className="
              px-3 py-1
              bg-amber-100
              border border-black
              rounded
              hover:bg-amber-200
              font-mono
              disabled:opacity-50
            "
          >
            {piece}
          </button>
        ))}

        {answered && (
          <button
            onClick={handleNext}
            className="
              mt-2
              px-3 py-1
              bg-green-200
              border border-black
              rounded
            "
          >
            Próximo exercício
          </button>
        )}
      </div>
    </div>
  );
}