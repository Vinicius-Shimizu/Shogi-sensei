import Hand from "./Hand";
import { Board } from "./Board";
import { useEffect, useState } from 'react'
import Options from "./Options";


export default function Exercise(){
  const [exercise, setExercise] = useState(null)
  const [whiteHand, setWhiteHand] = useState(null)
  const [blackHand, setBlackHand] = useState(null)
  const [possible_moves, setPossibleMoves] = useState([])
  const [solution, setSolution] = useState(null)
  useEffect(() => {
    async function fetchExercise() {
      const response = await fetch(
        "http://localhost:8000/exercises/checkmate_in_one"
      )

      let data = await response.json()
      console.log(data)
      data = data.response[0]
      let solution = data["solution"]
      let hands = data["hands"]
      let moves = data["options"]
      
      console.log(hands)
      console.log(moves)
      setExercise(data)
      setWhiteHand(hands.gote)
      setBlackHand(hands.sente)
      setPossibleMoves(moves)
      setSolution(solution)
    }

    fetchExercise()
  }, [])
  if (!exercise) {
    return <div>Carregando...</div>
  }
  return (
    <div className="flex justify-center">
        <div className="flex-col justify-center border-2 p-5">
            <Hand pieces={whiteHand}></Hand>
            <Board
                sfen={exercise["sfen"]}
            />
            <Hand pieces={blackHand}></Hand>
        </div>
        <Options possible_moves={possible_moves} solution={solution}/>
    </div>
  )
}