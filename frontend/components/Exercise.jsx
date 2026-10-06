import Hand from "./Hand";
import Board  from "./Board";
import BoardWithMovement from "./BoardWithMovement";
import CheckmateInOneOptions from "./CheckmateInOneOptions";
import ReconOptions from "./ReconOptions";
import MovementOptions from "./MovementOptions";
import CheckmateBoard from "./CheckmateBoard";
import PromotionOptions from "./PromotionOptions";

export default function Exercise({
  exercise,
  onAnswer,
  exerciseNumber,
  totalExercises,
}) {
  switch(exercise.type){
    case "recon":
      return (
        <div className="flex flex-col justify-center items-center">
          <Board sfen={exercise.sfen}/>
    
          <ReconOptions
            position={exercise.solution.split(":")[1]}
            possible_pieces={exercise.options}
            onAnswer={onAnswer}
            exerciseNumber={exerciseNumber}
            totalExercises={totalExercises}
          />
        </div>
      );

    case "movement1":
      return (
        <div className="flex flex-col justify-center items-center">
          <BoardWithMovement sfen={exercise.sfen} moves={exercise.solution.split(":")[1]}/>
    
          <MovementOptions
            possible_pieces={exercise.options}
            onAnswer={onAnswer}
            exerciseNumber={exerciseNumber}
            totalExercises={totalExercises}
          />
        </div>
      );

    case "movement2":
      return (
        <div className="flex flex-col justify-center items-center">
          <BoardWithMovement sfen={exercise.sfen} moves={exercise.solution.split(":")[1]}/>
    
          <MovementOptions
            possible_pieces={exercise.options}
            onAnswer={onAnswer}
            exerciseNumber={exerciseNumber}
            totalExercises={totalExercises}
          />
        </div>
      );

    case "promotion":
      return (
        <div className="flex flex-col justify-center items-center">
          <Board sfen={exercise.sfen}/>
    
          <PromotionOptions
            possible_moves={exercise.options}
            onAnswer={onAnswer}
            exerciseNumber={exerciseNumber}
            totalExercises={totalExercises}
          />
        </div>
      );

    case "checkmate-in-one":
      return (
        <div className="flex flex-col justify-center items-center">
          <div className="flex-col justify-center">
            <Hand pieces={exercise.hands.gote} side={"gote"} />
            <CheckmateBoard sfen={exercise.sfen}/>
            <Hand pieces={exercise.hands.sente} side={"sente"}/>
          </div>
    
          <CheckmateInOneOptions
            possible_moves={exercise.options}
            onAnswer={onAnswer}
            exerciseNumber={exerciseNumber}
            totalExercises={totalExercises}
          />
        </div>
      );
    
  }

}