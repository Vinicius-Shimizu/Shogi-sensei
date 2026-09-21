import { useState } from "react"
import ExercisePreview from "./ExercisePreview";

export default function Result({index, result}){
    const [showExplanation, setShowExplanation] = useState(false);
    const exercise_types = {"recon": "reconhecimento", "movement2": "Movimento 2"};
    
    return(
    <>
        <div>{index}</div>
        <div>{exercise_types[result.exercise_type]}</div>
        <div>{result.answer}</div>
        <div>{result.solution.split(":")[0]}</div>

        <div>
            {!result.is_correct && (
                <button onClick={() => setShowExplanation(true)}>
                    Ver explicação
                </button>
            )}
            {result.is_correct && (
                <p>-</p>
            )}
        </div>

        {showExplanation && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
                <div className="bg-white p-6 rounded-lg max-w-2xl w-full">
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