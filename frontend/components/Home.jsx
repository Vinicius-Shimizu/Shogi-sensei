import BeginButton from "./BeginButton";
import ExerciseList from "./ExerciseList";
import LoginButton from "./LoginButton";
import { useState } from "react";

export default function Home(){
    const [started, setStarted] = useState(false);
    if(started) return <ExerciseList />;

    return <div className="grid grid-cols-3 h-screen p-4">
        <div></div>
        <div className="">
            <h1>Shogi-sensei</h1>
            <BeginButton onClick={() => {console.log("Starting list"); setStarted(true);}}></BeginButton>
        </div>
        <div className="justify-center">
            <LoginButton></LoginButton>
        </div>
    </div>
}