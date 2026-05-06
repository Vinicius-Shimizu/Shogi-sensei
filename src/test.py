import subprocess
import argparse
import sys

def main(args):
    model = args.model
    print("Using model: ", model)
    # Roda a engine
    engine = subprocess.Popen(
        [model],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )

    # Inicializa USI
    engine.stdin.write("usi\n")
    engine.stdin.flush()
    # print(engine.stdout.readline())  # ID da engine etc.

    engine.stdin.write("setoption name USI_OwnBook value false\n")
    engine.stdin.flush()

    engine.stdin.write("isready\n")
    engine.stdin.flush()
    # print(engine.stdout.readline())

    # Define posição inicial
    engine.stdin.write("position startpos moves 7g7f 3c3d\n")
    engine.stdin.flush()

    engine.stdout.flush()
    # Pede a melhor jogada
    engine.stdin.write("go depth 15\n")
    engine.stdin.flush()

    while True:
        line = engine.stdout.readline()
        if line.startswith("bestmove"):
            print("Movimento sugerido:", line.replace("bestmove", ""))
            break
        elif args.v:
            print(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="./YaneuraOu_NNUE_halfkpe9_256x2_32_32-V900Git_AVX2.exe", help="Model to be used")
    parser.add_argument("--v", action="store_true", help="Verbose mode")
    args = parser.parse_args()
    main(args)