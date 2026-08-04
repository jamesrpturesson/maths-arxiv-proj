import json
from collections import Counter
import numpy as np

RECORDS = Path("records.jsonl")

def load_records():
    with RECORDS.open(encoding = "utf-8") as rf:
        for line in rf:
            yield json.loads(line)

def build_category_matrix():
    pass

def count_categories():
    pass
