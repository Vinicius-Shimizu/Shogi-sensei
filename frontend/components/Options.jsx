import { useState } from "react";


export default function Options({ possible_moves, solution }) {
    const [feedback, setFeedback] = useState(null);
    
    function validateAnswer(answer, solution){
        console.log(answer === solution)
        if (answer === solution) setFeedback("ACERTOU!!!");
        else setFeedback("ERROU...");
    }
    
    
    return (
        <div className="flex justify-center w-70">
            <div className="flex flex-col gap-2 justify-center mt-4 w-30">
                Answers:
                {possible_moves.map((move) => (
                    <button
                        key={move}
                        onClick={() => validateAnswer(move, solution)}
                        className="
                            px-3 py-1
                            bg-amber-100
                            border border-black
                            rounded
                            hover:bg-amber-200
                            font-mono
                        "
                    >
                        {move}
                    </button>
                ))}
                {feedback && (
                    <div className="mt-4 text-lg font-bold">
                        {feedback}
                    </div>
                )}
            </div>
        </div>
    );
}