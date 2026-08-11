import Hand from "./Hand";
import { Board } from "./Board";
import { useEffect, useState } from 'react'
import Options from "./Options";


export default function Exercise({exercise, onAnswer}){
  return (
    <div className="flex justify-center">
        <div className="flex-col justify-center border-2 p-5">
            <Hand pieces={exercise.hands.gote}></Hand>
            
            <Board
                sfen={exercise.sfen}
            />
            
            <Hand pieces={exercise.hands.sente}></Hand>
        </div>
        <Options 
            possible_moves={exercise.options} 
            solution={exercise.solution}
            onAnswer={onAnswer}
        />
    </div>
  )
}