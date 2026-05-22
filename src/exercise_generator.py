import subprocess
import argparse
# import cshogi
from cshogi import CSA
import os
import requests
import datetime
from bs4 import BeautifulSoup
from pprint import pprint
import psycopg
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
from src.database.connection import engine
from src.database.models.raw_game import RawGame

class ExerciseGenerator():
    def __init__(self, model: str, verbose=False, games_period = 7):
        self.verbose = verbose
        self.db = psycopg.connect(
            host="database",
            port=5432,
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        self.csa_parser = CSA.Parser()
        # self.engine = self.start_yaneuraou_engine(model)
        # self.exercises = None


    def start_yaneuraou_engine(self, model: str):
        print("Using model:", model)

        engine = subprocess.Popen(
            [model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd="/app/model"
        )

        engine.stdin.write("usi\n")
        engine.stdin.flush()
        self.read_until(engine, "usiok")
        print("Engine ok")
        engine.stdin.write("setoption name EvalDir value /app/model/eval\n")
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


    def get_games(self, last_days = 0):
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

            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a"):
                href = a.get("href")
                if href and href.endswith(".csa"):
                    try:
                        game = requests.get(url + href, timeout=10)
                        game.raise_for_status()
                        yield game.text
                    except requests.RequestException as e:
                        print(f"Failed to download {href}: {e}")
                        

    def insert_games(self):
        print("Parsing games...")
        games = []
        for game in self.get_games():
            if not game:
                print("Error")
            parsed_game = self.csa_parser.parse_str(game)[0]
            games.append({
                "game_comment": parsed_game.comment,
                "endgame": parsed_game.endgame,
                "sfen": parsed_game.sfen,
                "win": parsed_game.win,
                "moves": parsed_game.moves,
                "players": parsed_game.names,
                "moves_comments": parsed_game.comments,
                "ratings": parsed_game.ratings,
                "scores": parsed_game.scores,
                "times": parsed_game.times,
                "var_info": parsed_game.var_info,
            })
        print(f"Inserting {len(games)} games...")

        with Session(engine) as session:
            session.execute(
                insert(RawGame),
                games
            )
            session.commit()
        print("games inserted!")

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
        default="/app/yaneuraou"
    )
    parser.add_argument("--v", action="store_true")
    args = parser.parse_args()
    generator = ExerciseGenerator(args.model)
    print("Generator created")
    generator.insert_games()
    # csa_parser = CSA.Parser()
    # cur = generator.db.cursor()
    # for game in generator.get_games():
    #     # game_info = csa_parser.parse_str(game)
    #     break
    #     # pprint(type(game_info[0].comment))     
    #     # pprint(type(game_info[0].comments))     
    #     # pprint(type(game_info[0].endgame))     
    #     # pprint(type(game_info[0].moves))     
    #     # pprint(type(game_info[0].names))     
    #     # pprint(type(game_info[0].ratings))     
    #     # pprint(type(game_info[0].scores))     
    #     # pprint(type(game_info[0].sfen))     
    #     # pprint(type(game_info[0].times))     
    #     # pprint(type(game_info[0].var_info))     
    #     # pprint(type(game_info[0].win))     
    #     # break

