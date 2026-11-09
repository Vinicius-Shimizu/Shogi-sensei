import pandas as pd
import os
from pathlib import Path
import requests
import os
from dotenv import load_dotenv
import json
import ast
import matplotlib.pyplot as plt

load_dotenv()

ADMIN = os.getenv("ADMIN_USERNAME")
PWD = os.getenv("ADMIN_PASSWORD")
API_URL = os.getenv("API_URL") 

CWD = Path(os.getcwd())


def get_users_stats(df: pd.DataFrame, output_file: Path):
    users_ids = df["user_id"].unique()
    data = []
    for u in users_ids:
        response = requests.get(
            f"{API_URL}/users/{u}/status",
            auth=(ADMIN, PWD)
        )

        response = response.json()
        data.append(response)
    users_stats = pd.DataFrame(data)
    users_stats.to_csv(output_file/"users_stats.csv", index=False)
    return users_stats

def get_users_performances():
    df = pd.read_csv(CWD/"users_stats.csv")
    all_performances = {}
    for id, group in df.groupby("user_id"):
        performances = group["recent_performances"].to_list()[0]
        performances = ast.literal_eval(performances)
        all_performances[id] = performances
    
    return all_performances


def plot_performances_by_module():
    all_performances = get_users_performances()
    modules = {"recon": "Reconhecimento", 
               "movement1": "Movimento 1", 
               "movement2": "Movimento 2",
               "promotion": "Promoção", 
               "drop": "Drop", 
               "checkmate-in-one": "Xeque-mate"}
    
    user_indices = {
        user_id: index
        for index, user_id in enumerate(all_performances.keys(), start=1)
    }
    
    for module in modules:
        users = []

        for user_id, performances in all_performances.items():
            scores = [
                list(performance.values())[0]
                for performance in performances
                if module in performance
            ]

            if scores:
                users.append((user_id, scores))

        fig, axes = plt.subplots(
            2, 5,
            figsize=(16, 7),
            sharey=True
        )

        for ax, (user_id, scores) in zip(axes.flat, users):
            ax.plot(
                range(1, len(scores) + 1),
                scores,
                marker="o"
            )

            ax.set_title(f"Usuário {user_indices[user_id]}")
            ax.set_ylim(0, 1.05)
            ax.set_xlim(1, len(scores) + 1)
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.grid(alpha=0.3)

        for ax in axes.flat[len(users):]:
            ax.set_visible(False)

        fig.suptitle(f"Evolução - {modules[module]}", fontsize=15)
        fig.supxlabel("Listas resolvidas")
        fig.supylabel("Pontuação")

        plt.tight_layout()
        # plt.show()
        plt.savefig(CWD/f"results/evolucao_{modules[module]}.png")
    

def main():
    plot_performances_by_module()
    
    
    
        
        
        
    

if __name__ == "__main__":
    main()