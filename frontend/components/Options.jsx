import { useState } from "react";

export default function Options({
  possible_moves,
  solution,
  onAnswer,
}) {
  const [feedback, setFeedback] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(null);

  function validateAnswer(answer) {
    const correct = answer === solution;

    setAnswered(true);

    if (correct) {
      setFeedback("ACERTOU!!!");
    } else {
      setFeedback("ERROU...");
    }

    setIsCorrect(correct);
  }

  
  return (
    <div className="flex justify-center w-70">
      <div className="flex flex-col gap-2 justify-center mt-4 w-30">
        Answers:

        {possible_moves.map((move) => (
          <button
            key={move}
            disabled={answered}
            onClick={() => validateAnswer(move)}
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
            {move}
          </button>
        ))}

        {/* {feedback && (
          <div className="mt-4 text-lg font-bold">
            {feedback}
          </div>
        )} */}

        {answered && (
          <button
            onClick={() => onAnswer(isCorrect)}
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