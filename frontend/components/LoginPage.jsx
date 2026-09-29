import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function LoginPage(){
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const API_URL=import.meta.env.VITE_BACKEND_API_URL;

    async function handleLogin(event){
        event.preventDefault();

        setError("");
        setLoading(true);
        try{
            const response = await fetch(
                `${API_URL}/auth/login`, 
                {
                    method: "POST",
                    headers: {
                        "Content-type": "application/x-www-form-urlencoded",
                    },
                    body: new URLSearchParams({
                        username: username,
                        password: password,
                    }), 
                }
            )
            if(!response.ok){
                setError("Usuário ou senha incorretos."); return;
            }

            const data = await response.json();
            localStorage.setItem("access_token", data.access_token);

            navigate("/");
        } catch(error){
            console.error("Unable to connect to server.", error);
            setError("Não foi possível conectar ao servidor.");
        } finally{
            setLoading(false);
        }   
    }

    return <div className="flex justify-center items-center h-screen">
        <form
            onSubmit={handleLogin}
            className="flex flex-col gap-4 w-80"
        >
            <h1 className="text-2xl">Shogi-sensei</h1>
            <input 
                type="text" 
                placeholder="Usuário" 
                value={username} 
                onChange={(event) => setUsername(event.target.value)} 
                className="border-2 rounded p-2" 
                required 
            />
            <input 
                type="password" 
                placeholder="Senha" 
                value={password} 
                onChange={(event) => setPassword(event.target.value)} 
                className="border-2 rounded p-2" 
                required 
            />
            {error && ( 
                <p className="text-red-500"> 
                    {error} 
                </p> )
            }
            <button 
                type="submit" 
                disabled={loading} 
                className="border-2 rounded p-2 bg-slate-600 text-white" 
            > 
                {loading ? "Entrando..." : "Entrar"} 
            </button>
            <button 
                type="button" 
                onClick={() => navigate("/")} 
                className="border-2 rounded p-2" 
            > 
                Voltar 
            </button>
        </form>
    </div>
}