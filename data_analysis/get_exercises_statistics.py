import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd

limit = 100
offset = 0

all_stats = []
load_dotenv()

ADMIN = os.getenv("ADMIN_USERNAME")
PWD = os.getenv("ADMIN_PASSWORD")
API_URL = os.getenv("API_URL") 
with tqdm(desc="Coletando estatísticas", unit=" registros") as pbar:
    while True:
        response = requests.get(
            f"{API_URL}/exercises/statistics",
            params={
                "limit": limit,
                "offset": offset
            },
            auth=(ADMIN, PWD)
        )

        response.raise_for_status()

        result = response.json()

        all_stats.extend(result["data"])

        if pbar.total is None:
            pbar.total = result["total"]

        pbar.update(len(result["data"]))

        if not result["has_more"]:
            break

        offset += len(result["data"])

print(f"\nTotal de registros coletados: {len(all_stats)}")
df = pd.DataFrame(all_stats)
df.to_csv("users_answers.csv", index=False)
