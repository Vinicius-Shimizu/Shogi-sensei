import subprocess
import argparse
import cshogi
from cshogi import CSA
import requests
import datetime
from bs4 import BeautifulSoup
from pprint import pprint
from src.database.repositories.raw_games import RawGameRepository
from src.database.repositories.exercise import ExerciseRepository
from concurrent.futures import ThreadPoolExecutor
import random

class ExerciseGenerator():
    def __init__(self, model: str, verbose=False, games_period = 7):
        self.verbose = verbose
        self.csa_parser = CSA.Parser()

        # self.engine = self.start_yaneuraou_engine(model)
        
        self.raw_games_repo = RawGameRepository()
        self.exercises_repo = ExerciseRepository()
        self.session = requests.Session()

    # def start_yaneuraou_engine(self, model: str):
    #     print("Using model:", model)

    #     engine = subprocess.Popen(
    #         [model],
    #         stdin=subprocess.PIPE,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT,
    #         text=True,
    #         bufsize=1,
    #         cwd="/app/model"
    #     )

    #     engine.stdin.write("usi\n")
    #     engine.stdin.flush()
    #     self.read_until(engine, "usiok")
    #     print("Engine ok")
    #     engine.stdin.write("setoption name EvalDir value /app/model/eval\n")
    #     engine.stdin.flush()
    #     engine.stdin.write("setoption name USI_Hash value 32\n")
    #     engine.stdin.flush()

    #     engine.stdin.write("setoption name Threads value 8\n")
    #     engine.stdin.flush()
    #     engine.stdin.write("setoption name USI_OwnBook value false\n")
    #     engine.stdin.flush()
    #     engine.stdin.write("isready\n")
    #     engine.stdin.flush()
    #     self.read_until(engine, "readyok")
    #     print("Engine ready!")
    #     return engine


    # def read_until(self, engine, keyword):
    #     while True:
    #         line = engine.stdout.readline()
    #         if not line:
    #             raise RuntimeError("Engine stopped")
    #         line = line.strip()

    #         if(self.verbose): print("[ENGINE]", line)

    #         if keyword in line:
    #             return line

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


    # def get_best_moves(self, sfen: str, multipv=4, depth=8):
    #     engine = self.engine
    #     engine.stdin.write(f"setoption name MultiPV value {multipv}\n")
    #     engine.stdin.write("isready\n")
    #     engine.stdin.flush()
    #     self.read_until(engine, "readyok")
    #     print("Engine ready!")

    #     engine.stdin.write("usinewgame\n")
    #     engine.stdin.write(f"position sfen {sfen}\n")
    #     engine.stdin.write(f"go depth {depth}\n")
    #     engine.stdin.flush()

    #     moves = {}

    #     while True:
    #         line = engine.stdout.readline().strip()

    #         if self.verbose:
    #             print("[ENGINE]", line)

    #         if line.startswith("info") and " multipv " in line and " pv " in line:
    #             tokens = line.split()

    #             pv = int(tokens[tokens.index("multipv") + 1])
    #             move = tokens[tokens.index("pv") + 1]

    #             moves[pv] = move

    #         elif line.startswith("bestmove"):
    #             break

    #     return [moves[i] for i in sorted(moves)]


    def checkmate_in_one(self):
        def parse_hands(hand_string):
            if hand_string == "-":
                return {
                    "sente": {},
                    "gote": {},
                }

            result = {
                "sente": {},
                "gote": {},
            }

            i = 0

            while i < len(hand_string):
                count = ""

                while i < len(hand_string) and hand_string[i].isdigit():
                    count += hand_string[i]
                    i += 1

                piece = hand_string[i]
                qty = int(count) if count else 1

                target = "sente" if piece.isupper() else "gote"
                piece = piece.upper()

                result[target][piece] = result[target].get(piece, 0) + qty

                i += 1

            return result


        def generate_options(legal_moves, solution, n=4):
            moves = [m for m in legal_moves if m != solution]
            options = random.sample(moves, min(n-1, len(moves)))
            options.append(solution)
            random.shuffle(options)
            return options
        

        exercises = []
        while len(exercises) == 0:
            game = self.raw_games_repo.get_random()
            board = cshogi.Board()

            seen_positions = set()

            for ply, move in enumerate(game.moves):
                mate_move = board.mate_move_in_1ply()
                if mate_move:
                    test_board = board.copy()
                    test_board.push(mate_move)
                    if not test_board.is_check(): continue
                    sfen = board.sfen()
                    if sfen.split(" ")[1] == "w": continue
                    if sfen not in seen_positions:
                        seen_positions.add(sfen)
                        solution = cshogi.move_to_usi(mate_move)
                        legal_moves = [cshogi.move_to_usi(move) for move in board.legal_moves]
                        # options = self.get_best_moves(sfen)

                        # if len(options) < 3: continue
                        # options = random.sample(options, min(3, len(options)))
                        # options.append(solution)
                        # random.shuffle(options)
                        exercise = {
                            "sfen": sfen,
                            "hands": parse_hands(sfen.split(" ")[2]),
                            "solution": solution,
                            "options": generate_options(legal_moves, solution),
                            "pieces_used": solution[0],
                            "type": "checkmate-in-one"
                        }

                        exercises.append(exercise)

                board.push(move)
        self.exercises_repo.bulk_insert(exercises)



def print_board(sfen: str):
    board_part = sfen.split()[0]

    print("   9  8  7  6  5  4  3  2  1")

    for rank, row in enumerate(board_part.split("/"), start=1):
        cells = []
        i = 0

        while i < len(row):
            c = row[i]

            if c.isdigit():
                cells.extend([" . "] * int(c))
                i += 1

            elif c == "+":
                cells.append(f"+{row[i+1]:<2}")
                i += 2

            else:
                cells.append(f" {c} ")
                i += 1

        print(f"{chr(rank + 96)} " + "".join(cells))

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
    # generator.insert_games()
    exercises = generator.checkmate_in_one()
    # print(cshogi.move_to_usi(exercises[0]["solution"]))
    for exercise in exercises:
        print("\n=========================================\n")
        sfen = exercise["sfen"]
        board = cshogi.Board(sfen)
        pieces_in_hand = board.pieces_in_hand
        turn = board.turn
        pieces_in_hand_model = """\n  sente(black), gote(white)\n  [P, L, N, S, G, B, R]"""
        print(f"Pieces in hand: \n  Model: {pieces_in_hand_model} \n{exercise['sfen'].split(' ')[2]} {pieces_in_hand}"
        )

        
        print(f"Turn: {'WHITE' if turn else 'BLACK'}")
        print(f"Legal moves: {len([cshogi.move_to_usi(move) for move in board.legal_moves])}")
        print_board(sfen)
        print("\n\n")
        solution = cshogi.move_to_usi(exercise["solution"])
        print(f"Solution: {solution}")
        board.push(exercise["solution"])
        print_board(board.sfen())
        print(f"New legal moves: {len([cshogi.move_to_usi(move) for move in board.legal_moves])}")
        print("\n=========================================\n")

    