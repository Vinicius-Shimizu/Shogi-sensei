export default function SignUpButton({ onClick }) {
    return (
        <button
            className="flex flex-col justify-center border-2 bg-wood rounded-xl w-[50%] h-[10%] mt-4 text-black"
            onClick={onClick}
        >
            Cadastrar
        </button>
    );
}