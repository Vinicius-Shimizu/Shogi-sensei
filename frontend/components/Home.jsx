import BeginButton from "./BeginButton";
import LoginButton from "./LoginButton";
import SignUpButton from "./SignUpButton";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Banner from "./Banner";

export default function Home(){
    const navigate = useNavigate();
    const [authenticated, setAuthenticated] = useState(false);

    const API_URL = import.meta.env.VITE_BACKEND_API_URL;
    const BASE_URL = import.meta.env.BASE_URL;

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
            <div className="flex flex-col justify-center items-center">
                {/* <div className="flex flex-col justify-between items-center">
                    <img
                        src={`${BASE_URL}pieces/pawn.svg`}
                        className="w-[5vw]"
                    />
                    <h1 className="whitespace-nowrap translate-y-4">Shogi-sensei</h1>
                    <img
                        src={`${BASE_URL}pieces/pawn.svg`}
                        className="w-[5vw]"
                    />
                </div> */}
                <Banner></Banner>
                <BeginButton onClick={() => {console.log("Starting list"); navigate("/exercise-list");}}></BeginButton>
                <button className="flex flex-col justify-center border-2 bg-wood text-black rounded-xl w-[50%] h-[10%] mt-4" onClick={() => {
                    localStorage.removeItem("current_exercise");
                    localStorage.removeItem("access_token");
                    localStorage.removeItem("user_answers");
                    localStorage.removeItem("exercise_list"); 
                    setAuthenticated(false); 
                }}>
                    Logout
                </button>
            </div>
        </div>
    }
    return <div className="flex flex-cols justify-center min-h-screen w-full bg-black">
        <div className="flex flex-col justify-center items-center">
            {/* <div className="flex justify-between items-center">
                <img
                    src={`${BASE_URL}pieces/pawn.svg`}
                    className="w-[5vw]"
                />
                <h1 className="whitespace-nowrap translate-y-4">Shogi-sensei</h1>
                <img
                    src={`${BASE_URL}pieces/pawn.svg`}
                    className="w-[5vw]"
                />
            </div> */}
            <Banner />
            <p>Boas vindas ao Shogi-sensei.</p>
            <p>Faça o login ou cadastre-se para começar.</p>
    
            <LoginButton onClick={() => navigate("/login")} />
            <SignUpButton onClick={() => navigate("/signup")}/>
        </div>
    </div>
}