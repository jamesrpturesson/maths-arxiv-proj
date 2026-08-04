import json
from collections import Counter
from pathlib import Path

RECORDS = Path("records.jsonl")
AUTHORS = Path("authors.json")

def load_records():
    with RECORDS.open(encoding = "utf-8") as rf:
        for line in rf:
            yield json.loads(line)

def author_key(author):
    keyname = (author.get("keyname") or "").strip().lower()
    forenames = (author.get("forenames") or "").strip().lower()
    return f"{keyname}_{forenames}"

def count_papers():
    counts = Counter()
    display = {}

    for rec in load_records():
        for a in rec["authors"]:
            key = author_key(a)
            counts[key] += 1
            display.setdefault(key, f"{a.get("fornames") or ""} {a.get("keyname")}".strip())
    
    out = {
        key : {"name" : display[key], "papers" : n}
        for key, n in counts.most_common()
    }

    with AUTHORS.open("w", encoding="utf-8") as af:
        json.dump(out, af, indent = 2, ensure_ascii = False)
    
    print(f"Wrote to {str(AUTHORS)} with {len(out)} entries")

count_papers()