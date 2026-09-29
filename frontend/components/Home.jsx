import BeginButton from "./BeginButton";
import ExerciseList from "./ExerciseList";
import LoginButton from "./LoginButton";
import SignUpButton from "./SignUpButton";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home(){
    const navigate = useNavigate();
    const [started, setStarted] = useState(false);
    const [user, setUser] = useState(null);
    const [checkingAuth, setCheckingAuth] = useState(true);
    const token = localStorage.getItem("access_token");
    const API_URL = import.meta.env.VITE_BACKEND_API_URL;
    useEffect(() => {
        async function checkAuth() {
            const token = localStorage.getItem("access_token");

            if (!token) {
                setCheckingAuth(false);
                return;
            }

            try {
                const response = await fetch(
                    `${API_URL}/users/me`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                if (!response.ok) {
                    localStorage.removeItem("access_token");
                    setUser(null);
                    return;
                }

                const data = await response.json();
                setUser(data);

            } catch (error) {
                console.error("Erro ao verificar autenticação:", error);
            } finally {
                setCheckingAuth(false);
            }
        }

        checkAuth();
    }, []);
    
    if(started) return <ExerciseList />;

    if(token){
        return <div className="flex flex-cols justify-center h-screen p-4">
            <div></div>
            <div className="">
                <h1>Shogi-sensei</h1>
                <BeginButton onClick={() => {console.log("Starting list"); setStarted(true);}}></BeginButton>
            </div>
        </div>
    }
    return <div className="flex flex-cols justify-center h-screen p-4">
        <div></div>
        <div className="flex flex-col justify-center items-center">
            <h1>Shogi-sensei</h1>
            <p>Boas vindas ao Shogi-sensei.</p>
            <p>Faça o login ou cadastre-se para começar.</p>
    
            <LoginButton onClick={() => navigate("/login")} />
            <SignUpButton />
        </div>
    </div>
}