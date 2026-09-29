export default function SignUpButton({ onClick }) {
    return (
        <button
            className="flex-col border-2 bg-slate-600 rounded-xl w-[50%] h-[10%] mt-4"
            onClick={onClick}
        >
            Cadastrar
        </button>
    );
}