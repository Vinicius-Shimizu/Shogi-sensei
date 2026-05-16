import subprocess
import argparse
import cshogi
import os
import requests
import datetime
from bs4 import BeautifulSoup

def read_until(engine, keyword, verbose=False):
    while True:
        line = engine.stdout.readline()
        if not line:
            raise RuntimeError("Engine stopped")
        line = line.strip()

        if(verbose): print("[ENGINE]", line)

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

def generate_random_board():
    board = cshogi.Board()
    for move in board.legal_moves:
        temp = board.copy()
        temp.push(move)

        if temp.is_mate():
            print("mate!!")

def getGames(last_days: int):
    print(f"Looking for games from the last {last_days} days...")
    today = datetime.date.today()
    games = []

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
                game_url = url + href

                try:
                    game = requests.get(url + href, timeout=10)
                    game.raise_for_status()
                    # games.append(game)
                    # print("Game received")
                    yield game.text
                except requests.RequestException as e:
                    print("Failed to download {href}: {e}")
                    
        break

    print("Games fetched!")
    return games



def main(args):
    # eval_engine = run_engine(args.model, args.v)
    # games = getGames(10)
    # print(games[0])
    # for game in games:
    #     parsed_game = cshogi.CSA.Parser.parse_file(game)
    #     print(parsed_game)
    #     break
    for game in getGames(1):
        print(game)
        break

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