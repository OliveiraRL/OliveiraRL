import os
import requests
import random

USERNAME = "OliveiraRL"
TOKEN = os.getenv("PAT_GITHUB")
OUTPUT = "christmas-lights.svg"

if not TOKEN:
    raise RuntimeError("PAT_GITHUB não encontrado")

query = f"""
{{
  user(login: "{USERNAME}") {{
    contributionsCollection {{
      contributionCalendar {{
        weeks {{
          contributionDays {{
            contributionCount
          }}
        }}
      }}
    }}
  }}
}}
"""

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

data = response.json()

if "errors" in data:
    raise RuntimeError(data["errors"])

weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

colors = ["#ff0000", "#00ff00", "#ffd700", "#ffffff"]
off = "#1a1a1a"

size = 12
gap = 3

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="140">',
    '<rect width="100%" height="100%" fill="#0a0a0a"/>'
]

x = 10
for week in weeks:
    y = 10
    for day in week["contributionDays"]:
        if day["contributionCount"] > 0:
            color = random.choice(colors)
        else:
            color = off

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>'
        )
        y += size + gap
    x += size + gap

svg.append("</svg>")

with open(OUTPUT, "w") as f:
    f.write("\n".join(svg))

print("🎄 christmas-lights.svg gerado com sucesso")

