export default function LoginButton({ onClick }) {
    return (
        <button
            className="flex-col border-2 bg-slate-600 rounded-xl w-[50%] h-[10%] mt-8"
            onClick={onClick}
        >
            Login
        </button>
    );
}