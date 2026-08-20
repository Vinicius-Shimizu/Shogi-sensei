import subprocess
import random
import threading

class Engine():
    def __init__(self, model: str):
        self.verbose = False
        self.lock = threading.Lock()
        self.engine = self.start_yaneuraou_engine(model)

    def start_yaneuraou_engine(self, model: str):
        engine = subprocess.Popen(
            [model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd="/app/"
        )

        engine.stdin.write("usi\n")
        engine.stdin.flush()
        self.read_until(engine, "usiok")
        print("Engine ok")
        engine.stdin.write("setoption name EvalDir value /app/eval\n")
        engine.stdin.flush()
        engine.stdin.write("setoption name USI_Hash value 32\n")
        engine.stdin.flush()

        engine.stdin.write("setoption name Threads value 8\n")
        engine.stdin.flush()
        engine.stdin.write("setoption name USI_OwnBook value false\n")
        engine.stdin.flush()
        engine.stdin.write("isready\n")
        engine.stdin.flush()
        self.read_until(engine, "readyok")
        print("Engine ready!")

        return engine

    def read_until(self, engine, keyword):
        while True:
            line = engine.stdout.readline()
            if not line:
                raise RuntimeError("Engine stopped")
            line = line.strip()

            if(self.verbose): print("[ENGINE]", line)

            if keyword in line:
                return line
    
    def close(self):
        if self.engine:
            self.engine.stdin.write("quit\n")
            self.engine.stdin.flush()
            self.engine.wait(timeout=5)
    
    def _get_alternatives(self, sfen: str, solution: str, n: int, depth: int):
        self.engine.stdin.write("usinewgame\n")
        self.engine.stdin.write("setoption name MultiPV value 10\n")
        self.engine.stdin.write(f"position sfen {sfen}\n")
        self.engine.stdin.write(f"go depth {depth}\n")
        self.engine.stdin.flush()

        moves = {}

        while True:
            line = self.engine.stdout.readline().strip()

            if line.startswith("info") and "multipv" in line and " pv " in line:
                parts = line.split()

                multipv_index = parts.index("multipv") + 1
                pv_index = parts.index("pv") + 1

                multipv = int(parts[multipv_index])
                move = parts[pv_index]

                moves[multipv] = move

            elif line.startswith("bestmove"):
                break

        candidates = list(moves.values())

        candidates = [
            move for move in candidates
            if move != solution
        ]

        options = candidates[:n - 1]
        options.append(solution)

        random.shuffle(options)

        return options

    def get_alternatives(self, sfen: str, solution: str, n: int, depth: int):
        with self.lock:
            return self._get_alternatives(sfen, solution, n, depth)