import Hand from "./Hand";
import { Board } from "./Board";
import { useEffect, useState } from 'react'
import Options from "./Options";


export default function Exercise(){
  const [exercise, setExercise] = useState(null)
  useEffect(() => {
    async function fetchExercise() {
      const response = await fetch(
        "http://localhost:8000/exercises/checkmate_in_one"
      )

      let data = await response.json()
      console.log(data)
      data = data.response[0]
      
      setExercise(data)
    }

    fetchExercise()
  }, [])
  if (!exercise) {
    return <div>Carregando...</div>
  }
  return (
    <div className="flex justify-center">
        <div className="flex-col justify-center border-2 p-5">
            <Hand pieces={exercise["hands"].gote}></Hand>
            <Board
                sfen={exercise["sfen"]}
            />
            <Hand pieces={exercise["hands"].sente}></Hand>
        </div>
        <Options possible_moves={exercise["options"]} solution={exercise["solution"]}/>
    </div>
  )
}