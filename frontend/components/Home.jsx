import BeginButton from "./BeginButton";
import LoginButton from "./LoginButton";
import SignUpButton from "./SignUpButton";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home(){
    const navigate = useNavigate();
    const [authenticated, setAuthenticated] = useState(false);
    const token = localStorage.getItem("access_token");
    const API_URL = import.meta.env.VITE_BACKEND_API_URL;
    useEffect(() => {
        async function checkAuth() {
            const token = localStorage.getItem("access_token");

            if (!token) {
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
                    setAuthenticated(false);
                    return;
                }
                
                setAuthenticated(true);

            } catch (error) {
                console.error("Erro ao verificar autenticação:", error);
            }
        }

        checkAuth();
    }, [API_URL]);
    

    if(authenticated){
        return <div className="flex flex-cols justify-center min-h-screen w-full bg-black">
            <div></div>
            <div className="flex flex-col justify-center items-center">
                <h1>Shogi-sensei</h1>
                <BeginButton onClick={() => {console.log("Starting list"); navigate("/exercise-list");}}></BeginButton>
                <button className="flex-col border-2 bg-slate-600 rounded-xl w-[50%] h-[10%] mt-4" onClick={() => {localStorage.removeItem("access_token"); setAuthenticated(false);}}>
                    Logout
                </button>
            </div>
        </div>
    }
    return <div className="flex flex-cols justify-center min-h-screen w-full bg-black">
        <div></div>
        <div className="flex flex-col justify-center items-center">
            <h1>Shogi-sensei</h1>
            <p>Boas vindas ao Shogi-sensei.</p>
            <p>Faça o login ou cadastre-se para começar.</p>
    
            <LoginButton onClick={() => navigate("/login")} />
            <SignUpButton onClick={() => navigate("/signup")}/>
        </div>
    </div>
}