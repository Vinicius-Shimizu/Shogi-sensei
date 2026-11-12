import pandas as pd
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import json
import ast
import matplotlib.pyplot as plt
import textwrap

load_dotenv()

ADMIN = os.getenv("ADMIN_USERNAME")
PWD = os.getenv("ADMIN_PASSWORD")
API_URL = os.getenv("API_URL") 

CWD = Path(os.getcwd())


# Users statistics analysis
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

            ax.set_title(f"Participante {user_indices[user_id]}")
            ax.set_ylim(0, 1.05)
            ax.set_xlim(1, len(scores) + 1)
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.grid(alpha=0.3)

        for ax in axes.flat[len(users):]:
            ax.set_visible(False)

        fig.suptitle(f"Taxa de acerto - {modules[module]}", fontsize=15)
        fig.supxlabel("Listas resolvidas")
        fig.supylabel("Pontuação")

        plt.tight_layout()
        # plt.show()
        plt.savefig(CWD/f"results/desempenho_{modules[module].lower()}.png")
    
def get_modules_probs():
    df = pd.read_csv(CWD/"users_stats.csv")
    all_probs = {}
    for id, group in df.groupby("user_id"):
        probs = group["modules_probs"].to_list()[0]
        probs = ast.literal_eval(probs)
        all_probs[id] = probs
    
    return all_probs

def plot_modules_probs_by_user():
    all_probs = get_modules_probs()

    modules = {"recon": "Reconhecimento", 
               "movement1": "Movimento 1", 
               "movement2": "Movimento 2",
               "promotion": "Promoção", 
               "drop": "Drop", 
               "checkmate-in-one": "Xeque-mate"}
    
    user_indices = {
        user_id: index
        for index, user_id in enumerate(all_probs.keys(), start=1)
    }
    
    for module in modules:
        users = []

        for user_id, probs in all_probs.items():
            scores = [
                prob[module]
                for prob in probs
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

            ax.set_title(f"Participante {user_indices[user_id]}")
            ax.set_ylim(0, 1.05)
            ax.set_xlim(1, len(scores) + 1)
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.grid(alpha=0.3)

        for ax in axes.flat[len(users):]:
            ax.set_visible(False)

        fig.suptitle(f"Distribuição de probabilidade - {modules[module]}", fontsize=15)
        fig.supxlabel("Listas resolvidas")
        fig.supylabel("Probabilidade")

        plt.tight_layout()

        plt.savefig(CWD/f"results/probs_{modules[module].lower()}.png")

def plot_users_response_time():
    df = pd.read_csv(CWD / "users_answers.csv")

    modules = {
        "recon": "Reconhecimento",
        "movement1": "Movimento 1",
        "movement2": "Movimento 2",
        "promotion": "Promoção",
        "drop": "Drop",
        "checkmate-in-one": "Xeque-mate"
    }

    df["response_time_seconds"] = df["response_time_ms"] / 1000
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Ordena cronologicamente por participante
    df = df.sort_values(["user_id", "created_at", "id"])

    # Identifica as listas com base no created_at
    df["list_number"] = (
        df.groupby("user_id")["created_at"]
        .transform(lambda x: pd.factorize(x)[0] + 1)
    )

    # Calcula a média por participante, lista e módulo
    grouped = (
        df.groupby(["user_id", "list_number", "module"])
        ["response_time_seconds"]
        .mean()
        .reset_index()
    )

    user_ids = sorted(df["user_id"].unique())

    user_indices = {
        user_id: index
        for index, user_id in enumerate(user_ids, start=1)
    }

    for module, module_name in modules.items():
        module_df = grouped[grouped["module"] == module]

        fig, axes = plt.subplots(
            2, 5,
            figsize=(16, 7),
            sharey=True
        )


        for ax, user_id in zip(axes.flat, user_ids):
            user_df = module_df[
                module_df["user_id"] == user_id
            ].sort_values("list_number")

            if not user_df.empty:
                ax.plot(
                    user_df["list_number"],
                    user_df["response_time_seconds"],
                    marker="o"
                )

            ax.set_title(f"Participante {user_indices[user_id]}")
            
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            ax.set_yscale("log")
            ax.grid(alpha=0.3)

        for ax in axes.flat[len(user_ids):]:
            ax.set_visible(False)

        fig.suptitle(
            f"Tempo médio de resposta por lista - {module_name}",
            fontsize=15
        )
        fig.supxlabel("Listas resolvidas")
        fig.supylabel("Tempo médio de resposta (segundos)")

        plt.tight_layout()
        plt.savefig(CWD / f"results/response_time_{module}")
        plt.close(fig)

def plot_piece_accuracy():
    df = pd.read_csv(CWD / "users_answers.csv")

    modules = {
        "recon": "Reconhecimento",
        "movement1": "Movimento 1",
        "movement2": "Movimento 2",
        "promotion": "Promoção",
        "drop": "Drop",
        "checkmate-in-one": "Xeque-mate"
    }

    df["pieces_used"] = df["pieces_used"].apply(ast.literal_eval)
    df = df.explode("pieces_used")
    df = df.rename(columns={"pieces_used": "Peça"})

    df["is_correct"] = (
        df["is_correct"].astype(str).str.lower() == "true"
    )

    # Calcula a taxa de acerto
    accuracy = df.pivot_table(
        index="Peça",
        columns="module",
        values="is_correct",
        aggfunc="mean"
    )

    # Calcula a quantidade de questões
    counts = df.pivot_table(
        index="Peça",
        columns="module",
        values="is_correct",
        aggfunc="count"
    )

    # Garante a presença de todos os módulos
    accuracy = accuracy.reindex(columns=modules.keys())
    counts = counts.reindex(columns=modules.keys())

    # Calcula os valores totais por peça
    accuracy["total"] = df.groupby("Peça")["is_correct"].mean()
    counts["total"] = df.groupby("Peça")["is_correct"].count()

    # Combina porcentagem e quantidade
    table = accuracy.copy()

    for col in table.columns:
        table[col] = [
            f"{rate * 100:.1f}\\% ({int(count)})"
            if pd.notna(rate) and pd.notna(count)
            else "—"
            for rate, count in zip(accuracy[col], counts[col])
        ]

    table = table.rename(columns=modules)
    table = table.rename(columns={
        "total": "Total",
        "Reconhecimento": r"\makecell{Reconhe-\\cimento}"
    })

    table = table.reset_index()

    latex_table = table.to_latex(
        index=False,
        escape=False,
        column_format=(
            ">{\\centering\\arraybackslash}m{1.2cm} "
            + " ".join(
                [">{\\centering\\arraybackslash}m{1.7cm}"] * 7
            )
        ),
    )

    lines = latex_table.splitlines()

    data_indices = [
        i for i, line in enumerate(lines)
        if "&" in line and not line.lstrip().startswith("Peça")
    ]

    for i in data_indices[:-1]:
        lines[i] += r" \midrule"

    latex_table = "\n".join(lines)

    latex_table = (
        "\\resizebox{\\textwidth}{!}{%\n"
        + latex_table
        + "\n}"
    )

    with open(
        CWD / "results/piece_accuracy.tex",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(latex_table)

# Questionaire analysis

def plot_interface_eval():
    df = pd.read_csv(CWD/"users_evaluation.csv")
    col = df.columns[0]
    answers = df[col].dropna().astype(int)

    counts = answers.value_counts().sort_index()

    plt.figure(figsize=(8, 8))

    plt.pie(
        counts.values,
        labels=[f"Nota {n}" for n in counts.index],
        autopct=lambda p: f"{p:.1f}%\n({round(p * len(answers) / 100)} respostas)",
        startangle=90
    )

    plt.title(textwrap.fill(col, width=40))
    plt.tight_layout()

    plt.savefig(CWD/"results/interface_eval.png")

def plot_hardest_module():
    df = pd.read_csv(CWD / "users_evaluation.csv")
    cols = df.columns[2:4]
    df = df.rename(columns={cols[0]: "module", cols[1]: "reason"})

    module_order = [
        "Reconhecimento",
        "Movimento 1",
        "Movimento 2",
        "Promoção",
        "Drop",
        "Xeque-mate"
    ]

    counts = (
        df["module"]
        .dropna()
        .value_counts()
        .reindex(module_order, fill_value=0)
    )

    reasons = (
        df.dropna(subset=["module", "reason"])
        .groupby("module")["reason"]
        .apply(
            lambda x: r"\begin{itemize}" +
            "".join(r"\item " + reason for reason in x.unique()) +
            r"\end{itemize}"
        )
        .reindex(module_order)
    )

    table = pd.DataFrame({
        "Módulo": module_order,
        "Quantidade de participantes": counts.values,
        "Motivos": reasons.fillna("—").values
    })

    # Módulos sem respostas
    table.loc[
        table["Quantidade de participantes"] == 0,
        "Motivos"
    ] = "—"

    table = table.to_latex(
        index=False,
        escape=False,
        column_format=">{\\centering\\arraybackslash}m{3cm} "
                    ">{\\centering\\arraybackslash}m{3cm} "
                    ">{\\centering\\arraybackslash}m{8cm}",
    )
    lines = table.splitlines()

    data_indices = [
        i for i, line in enumerate(lines)
        if "&" in line and not line.lstrip().startswith("Módulo")
    ]

    for i in data_indices[:-1]:
        lines[i] += r"\midrule"

    table = "\n".join(lines)

    with open(CWD / "results/hardest_module.tex", "w", encoding="utf-8") as f:
        f.write(table)

def plot_explanation_clarity_eval():
    df = pd.read_csv(CWD/"users_evaluation.csv")
    col = df.columns[7]

    answers = df[col].dropna().astype(int)

    counts = answers.value_counts().sort_index()

    plt.figure(figsize=(8, 8))

    plt.pie(
        counts.values,
        labels=[f"Nota {n}" for n in counts.index],
        autopct=lambda p: f"{p:.1f}%\n({round(p * len(answers) / 100)} respostas)",
        startangle=90
    )

    plt.title(textwrap.fill(col, width=40))
    plt.tight_layout()

    plt.savefig(CWD/"results/explanation_clarity_eval.png")

def plot_explanation_contribution_eval():
    df = pd.read_csv(CWD/"users_evaluation.csv")
    col = df.columns[8]

    answers = df[col].dropna().astype(int)

    counts = answers.value_counts().sort_index()

    plt.figure(figsize=(8, 8))

    plt.pie(
        counts.values,
        labels=[f"Nota {n}" for n in counts.index],
        autopct=lambda p: f"{p:.1f}%\n({round(p * len(answers) / 100)} respostas)",
        startangle=90
    )

    plt.title(textwrap.fill(col, width=40))
    plt.tight_layout()

    plt.savefig(CWD/"results/explanation_contribution_eval.png")

def main():
    # plot_performances_by_module()
    # plot_modules_probs_by_user()
    # plot_users_response_time()
    plot_piece_accuracy()
    # plot_interface_eval()
    # plot_hardest_module()
    # plot_explanation_clarity_eval()
    # plot_explanation_contribution_eval()
    
    
        
        
        
    

if __name__ == "__main__":
    main()