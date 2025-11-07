import requests
import re
import json

targets = [
    "Disneyland",
    "Disney California Adventure",
    "Six Flags Magic Mountain",
    "Knott's Berry Farm",
    "Universal Studios Hollywood"
]

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())

target_norm = {norm(t): t for t in targets}

parks = requests.get("https://queue-times.com/parks.json").json()

park_ids = {}
for group in parks:
    for park in group["parks"]:
        n = norm(park["name"])
        for k, original in target_norm.items():
            if k in n or n in k:
                park_ids[original] = park["id"]

for name, pid in park_ids.items():
    data = requests.get(f"https://queue-times.com/parks/{pid}/queue_times.json").json()
    filename = name.lower().replace(" ", "_").replace("'", "") + ".json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(name, pid, "->", filename)
