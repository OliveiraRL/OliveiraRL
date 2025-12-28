import random
import requests

USERNAME = "OliveiraRL"
TOKEN = "${{ secrets.GITHUB_TOKEN }}"
OUTPUT = "christmas-lights.svg"

COLORS = ["#ff0000", "#00ff00", "#ffd700", "#ffffff"]
BG = "#0a0a0a"
SIZE = 11
GAP = 3

query = """
query($user:String!) {
  user(login:$user) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            contributionCount
          }
        }
      }
    }
  }
}
"""

r = requests.post(
    "https://api.github.com/graphql",
    json={"query": query, "variables": {"user": USERNAME}},
    headers={"Authorization": f"Bearer {TOKEN}"}
)

weeks = r.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="140">',
    f'<rect width="100%" height="100%" fill="{BG}"/>'
]

x = 10
for week in weeks:
    y = 10
    for day in week["contributionDays"]:
        color = random.choice(COLORS) if day["contributionCount"] > 0 else BG
        delay = round(random.uniform(0, 2), 2)

        svg.append(f'''
        <rect x="{x}" y="{y}" width="{SIZE}" height="{SIZE}" rx="3" fill="{color}">
          <animate attributeName="opacity"
                   values="1;0.3;1"
                   dur="1.5s"
                   begin="{delay}s"
                   repeatCount="indefinite"/>
        </rect>
        ''')
        y += SIZE + GAP
    x += SIZE + GAP

svg.append("</svg>")

with open(OUTPUT, "w") as f:
    f.write("\n".join(svg))
