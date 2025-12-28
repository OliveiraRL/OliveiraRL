import os
import requests
import random

USERNAME = "OliveiraRL"
TOKEN = os.getenv("GITHUB_TOKEN")
OUTPUT = "christmas-lights.svg"

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN não encontrado")

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

# 🎄 cores das lâmpadas
colors = ["#ff0000", "#00ff00", "#ffd700", "#ffffff"]
off = "#1a1a1a"

size = 14
gap = 6

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="160">',
    '<rect width="100%" height="100%" fill="#0a0a0a"/>',

    # ✨ filtro de brilho
    '''
    <defs>
      <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
        <feMerge>
          <feMergeNode in="coloredBlur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    '''
]

x = 20
delay = 0

for week in weeks:
    y = 20
    for day in week["contributionDays"]:
        if day["contributionCount"] > 0:
            color = random.choice(colors)
            flicker = "1"
        else:
            color = off
            flicker = "0.2"

        svg.append(f'''
        <circle cx="{x}" cy="{y}" r="7" fill="{color}" opacity="0.25" filter="url(#glow)">
          <animate attributeName="opacity"
                   values="0.2;1;0.4"
                   dur="1.8s"
                   begin="{delay * 0.15}s"
                   repeatCount="indefinite" />
        </circle>

        <circle cx="{x}" cy="{y}" r="4" fill="{color}">
          <animate attributeName="opacity"
                   values="0.3;1;0.6"
                   dur="1.8s"
                   begin="{delay * 0.15}s"
                   repeatCount="indefinite" />
        </circle>
        ''')

        y += size + gap
        delay += 1

    x += size + gap

svg.append("</svg>")

with open(OUTPUT, "w") as f:
    f.write("\n".join(svg))

print("🎄 christmas-lights.svg gerado com sucesso")
