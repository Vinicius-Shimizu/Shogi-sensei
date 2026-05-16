import subprocess
import argparse
# import cshogi
from cshogi import CSA
import os
import requests
import datetime
from bs4 import BeautifulSoup
from pprint import pprint


class ExerciseGenerator():
    def __init__(self, model: str, verbose=False, games_period = 7):
        self.verbose = verbose
        self.engine = self.start_yaneuraou_engine(model)
        self.exercises = None
        # self.games = []
        # for game in self.get_games(games_period):
        #     print(game)
        #     # game = CSA.Parser.parse_csa_str(game)
        #     break

    def start_yaneuraou_engine(self, model: str):
        print("Using model:", model)

        engine = subprocess.Popen(
            [model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        engine.stdin.write("usi\n")
        engine.stdin.flush()
        self.read_until(engine, "usiok")

        engine.stdin.write("setoption name USI_OwnBook value false\n")
        engine.stdin.flush()

        engine.stdin.write("isready\n")
        engine.stdin.flush()
        self.read_until(engine, "readyok")

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


    def get_games(self, last_days = 7):
        print(f"Looking for games from the last {last_days} days...")
        today = datetime.date.today()

        for d in range(last_days, -1, -1):
            date = str(today - datetime.timedelta(days=d)).replace("-", "/")
            url = f"http://wdoor.c.u-tokyo.ac.jp/shogi/x/{date}/"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to access {url}: {e}")
                continue

            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a"):
                href = a.get("href")
                if href and href.endswith(".csa"):
                    try:
                        game = requests.get(url + href, timeout=10)
                        game.raise_for_status()
                        yield game.text
                    except requests.RequestException as e:
                        print("Failed to download {href}: {e}")
                        



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

    # def generate_random_board():
    #     board = cshogi.Board()
    #     for move in board.legal_moves:
    #         temp = board.copy()
    #         temp.push(move)

    #         if temp.is_mate():
    #             print("mate!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="/app/model/yaneuraou"
    )
    parser.add_argument("--v", action="store_true")
    args = parser.parse_args()
    generator = ExerciseGenerator(args.model)
    csa_parser = CSA.Parser()
    for game in generator.get_games():
        game_info = csa_parser.parse_str(game)
        pprint(game_info[0].moves)     
        break
