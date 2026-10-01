import { useState } from "react"
import ExercisePreview from "./ExercisePreview";

export default function Result({index, result}){
    const [showExplanation, setShowExplanation] = useState(false);
    const exercise_types = {
        "recon": "Reconhecimento", 
        "movement1": "Movimento 1", 
        "movement2": "Movimento 2", 
        "drop": "Drop", 
        "promotion": "Promoção", 
        "checkmate-in-one": "Chequemate"
    };

    const resultColor = result.is_correct ? "bg-green-500 text-black" : "bg-red-600 text-black";
    const cellClass = `${resultColor} flex items-center justify-center text-center p-2`;

    return(
    <>
        <div className={cellClass}>{index}</div>
        <div className={cellClass}>{exercise_types[result.exercise_type]}</div>
        <div className={cellClass}>{result.answer}</div>
        <div className={cellClass}>{result.solution.split(":")[0]}</div>
        <div className={cellClass}>
            {!result.is_correct && (
                <button onClick={() => setShowExplanation(true)} className="underline mr-4">
                    Ver explicação
                </button>
            )}
            {result.is_correct && (
                <p>-</p>
            )}
        </div>

        {showExplanation && (
            <div className="fixed inset-0 z-50 flex items-center justify-center">
                <div className="bg-gray-800 p-6 rounded-lg w-[80vw] md:w-[30vw] max-h-[80vh] md:max-h-[80vh] overflow-y-auto">
                    <h3 className="text-xl font-bold mb-4">
                        Explicação
                    </h3>

                    <ExercisePreview result={result} />

                    <p className="mt-6 mb-6">
                        {result.explanation}
                    </p>

                    <button
                        onClick={() => setShowExplanation(false)}
                    >
                        Fechar
                    </button>
                </div>
            </div>
        )}
    </>
    );
}