import BeginButton from "./BeginButton";
import ExerciseList from "./ExerciseList";
import LoginButton from "./LoginButton";
import { useState } from "react";

export default function Home(){
    const [started, setStarted] = useState(false);
    if(started) return <ExerciseList />;

    return <div className="flex flex-col h-screen items-center p-4">
        <div className="flex justify-center">
            <h1>Shogi-sensei</h1>
            <LoginButton></LoginButton>
        </div>
        <div className="flex flex-col">
            <BeginButton onClick={() => {console.log("Starting list"); setStarted(true);}}></BeginButton>

        </div>
    </div>
}