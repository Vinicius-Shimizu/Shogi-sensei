function validateAnswer(answer, solution){
    console.log(answer === solution)
}

export default function Options({ possible_moves, onSelect, solution }) {
    return (
        <div className="flex justify-center w-70">
            <div className="flex flex-col gap-2 justify-center mt-4">
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
            </div>
        </div>
    );
}