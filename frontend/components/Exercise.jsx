import Hand from "./Hand";
import { Board } from "./Board";
import Options from "./Options";

export default function Exercise({
  exercise,
  onAnswer,
  exerciseNumber,
  totalExercises,
}) {
  return (
    <div className="flex justify-center items-center">
      <div className="flex-col justify-center border-2 p-5">
        <Hand pieces={exercise.hands.gote} />

        <Board sfen={exercise.sfen} />

        <Hand pieces={exercise.hands.sente} />
      </div>

      <div className="flex flex-col">
        <div className="font-semibold mb-4">
          {exerciseNumber + 1}/{totalExercises}
        </div>

        <Options
          possible_moves={exercise.options}
          onAnswer={onAnswer}
        />
      </div>
    </div>
  );
}