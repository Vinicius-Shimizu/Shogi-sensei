import subprocess
import argparse
import cshogi
from cshogi import CSA
import requests
import datetime
from bs4 import BeautifulSoup
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
import random

PIECES_TYPES = [
    "P",
    "L",
    "N",
    "S",
    "B",
    "R",
    "G",
    "K",
    "+P",
    "+L",
    "+N",
    "+S",
    "+B",
    "+R",
]

PIECES_DICT = {
    "P": "Peão",
    "L": "Lança",
    "N": "Cavalo",
    "S": "General de Prata",
    "B": "Bispo",
    "R": "Torre",
    "G": "General de Ouro",
    "K": "Rei",
    "+P": "Peão Promovido",
    "+L": "Lança Promovida",
    "+N": "Cavalo Promovido",
    "+S": "General de Prata Promovido",
    "+B": "Bispo promovido",
    "+R": "Torre Promovida",
}

class ExerciseGenerator():
    def __init__(self, verbose=False, games_period = 7):
        self.verbose = verbose
        self.csa_parser = CSA.Parser()
        self.session = requests.Session()
    
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
                    
    def parse_game(self, game):
        parsed_game = self.csa_parser.parse_str(game)[0]

        return {
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
                "processed": False
            }

    def get_positions_from_board(self, board: cshogi.Board, use_both_sides=True):
        positions = []
        for i in range(9):
            for j in range(9):
                piece_type = board.piece_type(j*9 + i)
                if piece_type == 0: continue
                piece = cshogi.PIECES[board.piece(j*9 + i)]
                if piece in [cshogi.NONE, cshogi.NOTUSE]: continue
                if not use_both_sides and str(piece).startswith("W"):
                    continue
                
                positions.append((f"{j + 1}{chr(ord('a') + i)}", PIECES_TYPES[piece_type - 1]))
        return positions

    def checkmate_in_one(self, games):
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


        def get_piece_used(board: cshogi.Board, move: int):
            usi = cshogi.move_to_usi(move)
            if "*" in usi:
                return usi[0]
            
            origin = cshogi.move_from(move)
            piece = board.piece(origin)
            return PIECES_TYPES[cshogi.piece_to_piece_type(piece) - 1]

        exercises = []
        if not games:
            return exercises
        for game in games:
            board = cshogi.Board()
            seen_positions = set()

            for _, move in enumerate(game.moves):
                mate_move = board.mate_move_in_1ply()
                if mate_move:
                    test_board = board.copy()
                    test_board.push(mate_move)
                    if not test_board.is_check(): 
                        board.push(move)
                        continue

                    sfen = board.sfen()
                    if sfen.split(" ")[1] == "w": 
                        board.push(move)
                        continue

                    if sfen not in seen_positions:
                        seen_positions.add(sfen)
                        solution = cshogi.move_to_usi(mate_move)
                        try:
                            print("sending sfen: ", sfen, " with solution: ", solution)
                            response = self.session.get(
                                "http://engine:8080/checkmate_in_one_answers",
                                params={
                                    "sfen": sfen,
                                    "solution": solution,
                                    "n": 4,
                                    "depth": 1
                                },
                                timeout=120
                            )
                            
                            response.raise_for_status()
                            options = response.json()
                            print(options)
                        except requests.RequestException as e:
                            print(f"Failed to generate alternatives: {e}")
                            continue
                        
                        if len(options) < 4: continue

                        exercise = {
                            "sfen": sfen,
                            "hands": parse_hands(sfen.split(" ")[2]),
                            "solution": solution,
                            "options": options,
                            "pieces_used": [get_piece_used(board, mate_move)],
                            "type": "checkmate-in-one"
                        }

                        exercises.append(exercise)

                board.push(move)

        return exercises

    def recon(self, games):
        exercises = []
        if not games:
            return exercises
        
        for game in games:
            board = cshogi.Board()

            for move in game.moves:
                board.push(move)
                sfen = board.sfen()
                positions = self.get_positions_from_board(board)
                square_usi, piece = random.choice(positions)
                solution = PIECES_DICT[piece]
                    
                possible_options = [
                    piece
                    for piece in PIECES_DICT.values()
                    if piece != solution
                ]

                options = random.sample(
                    possible_options,
                    3
                )

                options.append(solution)
                random.shuffle(options)

                exercise = {
                    "sfen": sfen,
                    "hands": {
                        "sente": {},
                        "gote": {},
                    },
                    "solution": f"{solution}:{square_usi}",
                    "options": options,
                    "pieces_used": [piece],
                    "type": "recon"
                }
           
                exercises.append(exercise)

        return exercises

    def movement1(self):
        def get_options(piece: str):
            if piece in ("+B", "+R") or not piece.startswith("+"):
                options = [PIECES_DICT[p] for p in [p for p in PIECES_TYPES if p != piece]]
            else: 
                options = [PIECES_DICT[p] for p in [p for p in PIECES_TYPES if p not in ("+P", "+L", "+N", "+S", "G")]]
            options = random.sample(options, 3)
            options.append(PIECES_DICT[piece])
            random.shuffle(options)
            return options
        
        exercises = []
        for p in PIECES_TYPES:
            sfen = f"9/9/9/9/4{p}4/9/9/9/9 b"
            board = cshogi.Board(sfen)
            moves = [m for m in [cshogi.move_to_usi(m) for m in board.pseudo_legal_moves] if "+" not in m]
            options = get_options(p)
            exercise = {
                "sfen": sfen,
                "hands": {
                    "sente": {},
                    "gote": {},
                },
                "solution": f"{PIECES_DICT[p]}:{moves}",
                "options": options,
                "pieces_used": [p],
                "type": "movement1"
            }
            exercises.append(exercise)
        return exercises

    def movement2(self, games):
        def swap_piece(new_piece, square_usi, board):
            sfen = board.sfen().split(" ")
            positions = sfen[0].split("/")

            column = int(square_usi[0]) - 1
            row = ord(square_usi[1]) - 97

            expanded = []

            for char in positions[row]:
                if char.isdigit():
                    expanded.extend(["."] * int(char))
                else:
                    expanded.append(char)

            expanded[column] = new_piece

            compressed = []
            empty = 0

            for square in expanded:
                if square == ".":
                    empty += 1
                else:
                    if empty:
                        compressed.append(str(empty))
                        empty = 0
                    compressed.append(square)

            if empty:
                compressed.append(str(empty))

            positions[row] = "".join(compressed)
            sfen[0] = "/".join(positions)

            return " ".join(sfen)

        def moves_from_piece(square_usi, board):
            moves = [m for m in [cshogi.move_to_usi(m) for m in board.pseudo_legal_moves] if "+" not in m]
            return [m for m in moves if m.startswith(square_usi)]
        
        def get_options(piece, square_usi, board):
            solution_moves = [m for m in [cshogi.move_to_usi(m) for m in board.pseudo_legal_moves] if "+" not in m]
            solution_moves = [m for m in solution_moves if m.startswith(square_usi)]
            solution_moves = set(solution_moves)

            pieces_moves = {}
            for p in PIECES_TYPES:
                if p == piece: 
                    continue
                test_sfen = swap_piece(p, square_usi, board)
                try:
                    test_board = cshogi.Board(test_sfen)
                except:
                    continue
                moves = set(moves_from_piece(square_usi, test_board))
                if moves == solution_moves: continue
                pieces_moves[p] = moves

            options = []
            seen_moves = set()

            for p, moves in pieces_moves.items():
                moves_key = frozenset(moves)
                if moves_key in seen_moves: continue

                seen_moves.add(moves_key)
                options.append(PIECES_DICT[p])

            options = random.sample(options, min(3, len(options)))
            options.append(PIECES_DICT[piece])
            random.shuffle(options)
            return options

        exercises = []
        for game in games:
            board = cshogi.Board()
            for move in game.moves:
                board.push(move)
                sfen = board.sfen()
                if sfen.split(" ")[1] == "w": continue
                positions = self.get_positions_from_board(board, use_both_sides=False)
                square_usi, piece = random.choice(positions)
                solution = PIECES_DICT[piece]
                moves = [m for m in [cshogi.move_to_usi(m) for m in board.pseudo_legal_moves] if "+" not in m]
                moves = [m for m in moves if m.startswith(square_usi)]
                if len(moves) == 0: continue
                options = get_options(piece, square_usi, board)
                if len(options) < 4: continue

                exercise = {
                    "sfen": sfen,
                    "hands": {
                        "sente": {},
                        "gote": {},
                    },
                    "solution": f"{solution}:{moves}",
                    "options": options,
                    "pieces_used": [piece],
                    "type": "movement2"
                }
                exercises.append(exercise)

        return exercises



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

    