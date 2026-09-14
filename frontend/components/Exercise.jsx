import Hand from "./Hand";
import Board  from "./Board";
import BoardWithMovement from "./BoardWithMovement";
import CheckmateInOneOptions from "./CheckmateInOneOptions";
import ReconOptions from "./ReconOptions";
import MovementOptions from "./MovementOptions";

export default function Exercise({
  exercise,
  onAnswer,
  exerciseNumber,
  totalExercises,
}) {
  switch(exercise.type){
    case "recon":
      return (
        <div className="flex justify-center items-center">
          <div className="flex-col justify-center border-2 p-5">
            <Board sfen={exercise.sfen}/>
          </div>
    
          <div className="flex flex-col">
            <div className="font-semibold mb-4">
              {exerciseNumber + 1}/{totalExercises}
            </div>
            <ReconOptions
              position={exercise.solution.split(":")[1]}
              possible_moves={exercise.options}
              onAnswer={onAnswer}
            />
          </div>
        </div>
      );

    case "movement":
      return (
        <div className="flex justify-center items-center">
          <div className="flex-col justify-center border-2 p-5">
            <BoardWithMovement sfen={exercise.sfen} moves={exercise.solution.split(":")[1]}/>
          </div>
    
          <div className="flex flex-col">
            <div className="font-semibold mb-4">
              {exerciseNumber + 1}/{totalExercises}
            </div>
            <MovementOptions
              possible_pieces={exercise.options}
              onAnswer={onAnswer}
            />
          </div>
        </div>
      );

    case "checkmate-in-one":
      return (
        <div className="flex justify-center items-center">
          <div className="flex-col justify-center border-2 p-5">
            <Hand pieces={exercise.hands.gote} />
    
            <Board sfen={exercise.sfen}/>
    
            <Hand pieces={exercise.hands.sente} />
          </div>
    
          <div className="flex flex-col">
            <div className="font-semibold mb-4">
              {exerciseNumber + 1}/{totalExercises}
            </div>
            <CheckmateInOneOptions
              possible_moves={exercise.options}
              onAnswer={onAnswer}
            />
          </div>
        </div>
      );
    
  }

}