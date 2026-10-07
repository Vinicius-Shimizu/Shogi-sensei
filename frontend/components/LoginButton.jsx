export default function LoginButton({ onClick }) {
    return (
        <button
            className="flex flex-col justify-center border-2 bg-wood text-black rounded-xl w-[50%] h-[10%] mt-8 pt-2"
            onClick={onClick}
        >
            Login
        </button>
    );
}