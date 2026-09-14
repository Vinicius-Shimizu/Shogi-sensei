export default function LoginButton(){
    return <button className="flex-col border-2 bg-slate-600 rounded-full w-20 h-20" onClick={() => {console.log("Login pressed")}}>
        Login
    </button>
}