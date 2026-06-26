import Hand from "./Hand";
import { Board } from "./Board";
import { useEffect, useState } from 'react'
import Options from "./Options";


function parseHands(handString) {
    if (!handString || handString === "-") {
        return { sente: {}, gote: {} };
    }

    const result = {
        sente: {},
        gote: {},
    };

    let i = 0;

    while (i < handString.length) {
        let count = "";

        while (!isNaN(handString[i])) {
            count += handString[i];
            i++;
        }

        const piece = handString[i];
        const qty = count ? Number(count) : 1;

        const isSente = piece === piece.toUpperCase();

        const key = piece.toUpperCase();

        if (isSente) {
            result.sente[key] = (result.sente[key] || 0) + qty;
        } else {
            result.gote[key] = (result.gote[key] || 0) + qty;
        }

        i++;
    }

    return result;
}

function getPossibleAnswers(arr, n, solution) {
    const filtered = arr.filter(x => x !== solution);
    const shuffled = [...filtered];

    let i = shuffled.length;
    const min = Math.max(0, i - n);

    while (i-- > min) {
        const index = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[index]] = [shuffled[index], shuffled[i]];
    }

    const ans = shuffled.slice(min);
    ans.push(solution);

    return ans.sort(() => Math.random() - 0.5);
}

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
      data = data.response[0]
      console.log(data)
      let solution = data["solution"]
      let hands = data["sfen"].split(" ")[2]
      hands = parseHands(hands)
      let moves = getPossibleAnswers(data["options"], 3, solution)
      
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