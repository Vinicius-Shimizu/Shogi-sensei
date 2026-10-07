const BASE_URL=import.meta.env.BASE_URL

export default function Banner(){
    return (
        <div className="flex justify-between items-center pb-2">
            <img
                src={`${BASE_URL}pieces/pawn.svg`}
                className="w-[5vw]"
            />
            <h1 className="whitespace-nowrap">Shogi-sensei</h1>
            <img
                src={`${BASE_URL}pieces/pawn.svg`}
                className="w-[5vw]"
            />
        </div>
    )
}