import subprocess
import argparse
import cshogi
from cshogi import CSA
import requests
import datetime
from bs4 import BeautifulSoup
from pprint import pprint
from src.database.repositories.raw_games import RawGameRepository
from concurrent.futures import ThreadPoolExecutor

class ExerciseGenerator():
    def __init__(self, model: str, verbose=False, games_period = 7):
        self.verbose = verbose
        self.csa_parser = CSA.Parser()

        self.engine = self.start_yaneuraou_engine(model)
        
        self.raw_games_repo = RawGameRepository()
        self.session = requests.Session()

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

    def download_csa(self, url: str):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status
            return response.text
        except Exception as e:
            print("Failed download csa error: ", e)
            return None

    def get_games(self, last_days = 0):
        today = datetime.date.today()

        for d in range(last_days, -1, -1):
            date = str(today - datetime.timedelta(days=d)).replace("-", "/")
            print(f"Looking for games from {date}...")
            url = f"http://wdoor.c.u-tokyo.ac.jp/shogi/x/{date}/"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to access {url}: {e}")
                continue

            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            urls = []
            for a in soup.find_all("a"):
                href = a.get("href")
                if href and href.endswith(".csa"):
                    urls.append(url + href)
            print(len(urls))
            with ThreadPoolExecutor(max_workers=20) as executor:
                for game in executor.map(self.download_csa, urls):
                    if game: yield game
                # try:
                #     game = self.session.get(url + href, timeout=10)
                #     game.raise_for_status()
                #     yield game.text
                # except requests.RequestException as e:
                #     print(f"Failed to download {href}: {e}")
                    

    def insert_games(self):
        print("Parsing games...")
        games = []
        for game in self.get_games():
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
        if len(games) == 0:
            print("No games found")
            return
        print(f"Inserting {len(games)} games...")
        self.raw_games_repo.bulk_insert(games)
        print("games inserted!")


    def checkmate_in_one(self):
        game = self.raw_games_repo.get_by_id(1)

        board = cshogi.Board()

        exercises = []
        seen_positions = set()

        for ply, move in enumerate(game.moves):
            mate_move = board.mate_move_in_1ply()

            if mate_move:
                sfen = board.sfen()

                if sfen not in seen_positions:
                    seen_positions.add(sfen)

                    exercise = {
                        "sfen": sfen,
                        "solution": cshogi.move_to_usi(mate_move),
                        "ply": ply,
                        "game_id": game.game_id,
                    }

                    exercises.append(exercise)

            board.push(move)

        return exercises



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="/yaneuraou/yaneuraou"
    )
    parser.add_argument("--v", action="store_true")
    args = parser.parse_args()

    generator = ExerciseGenerator(args.model)
    generator.insert_games()
    # exercises = generator.checkmate_in_one()
    # print(exercises)
    # print("Generator created")
    # generator.insert_games()