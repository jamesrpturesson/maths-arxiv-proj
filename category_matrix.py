import json
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

RECORDS = Path("records.jsonl")
CATEGORIES = Path("categories/categories.json")

def load_records():
    with RECORDS.open(encoding = "utf-8") as rf:
        for line in rf:
            yield json.loads(line)

def build_categories():
    with CATEGORIES.open(encoding = "utf-8") as cf:
        categories_json = json.load(cf)
        return sorted(c for c in categories_json if c.startswith("math."))

def build_category_matrix():
    category_list = build_categories()
    index = {c: i for i, c in enumerate(category_list)}

    pc, sc = count_categories()

    M = np.zeros((len(category_list), len(category_list)), dtype = np.int64)
    for cat, n in pc.items():
        if cat in index:
            M[index[cat], index[cat]] = n
    for (p, s), n in sc.items():
        if p in index and s in index:
            M[index[p], index[s]] = n
    
    return M

def count_categories():
    primary_count = Counter()
    secondary_count = Counter()

    for rec in load_records():
        primary = rec.get("primary")
        if not primary:
            continue
        primary_count[primary] += 1
        for sec in set(rec.get("categories", [])):
            if sec != primary:
                secondary_count[(primary, sec)] += 1
    return primary_count, secondary_count
