import subprocess
import argparse
import cshogi
import os


def read_until(engine, keyword, verbose=False):
    """Lê stdout até encontrar uma palavra-chave"""
    while True:
        line = engine.stdout.readline()
        if not line:
            raise RuntimeError("Engine morreu inesperadamente")
        line = line.strip()

        print("[ENGINE]", line)

        if keyword in line:
            return line


def run_engine(model, verbose=False):
    print("Using model:", model)

    engine = subprocess.Popen(
        [model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # =============================
    # 🔧 Inicialização USI
    # =============================
    engine.stdin.write("usi\n")
    engine.stdin.flush()
    read_until(engine, "usiok", verbose)

    engine.stdin.write("setoption name USI_OwnBook value false\n")
    engine.stdin.flush()

    engine.stdin.write("isready\n")
    engine.stdin.flush()
    read_until(engine, "readyok", verbose)

    return engine


def get_bestmove(engine, moves, depth=10, verbose=False):
    # monta posição USI
    moves_str = " ".join(moves)
    engine.stdin.write(f"position startpos moves {moves_str}\n")
    engine.stdin.flush()

    engine.stdin.write(f"go depth {depth}\n")
    engine.stdin.flush()

    while True:
        line = engine.stdout.readline()
        if not line:
            raise RuntimeError("Engine morreu durante busca")

        line = line.strip()

        if verbose:
            print("[ENGINE]", line)

        if line.startswith("bestmove"):
            return line.split()[1]


def main(args):
    engine = run_engine(args.model, args.v)

    # =============================
    # 🧠 Usando cshogi
    # =============================
    board = cshogi.Board()
    for move in board.legal_moves:
        print(cshogi.move_to_usi(move))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="/app/model/yaneuraou"
    )
    parser.add_argument("--v", action="store_true")
    args = parser.parse_args()
    main(args)