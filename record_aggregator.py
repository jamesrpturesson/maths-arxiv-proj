from pathlib import Path
import xml.etree.ElementTree as ET
import json

OA = "{http://www.openarchives.org/OAI/2.0/}"
ARX = "{http://arxiv.org/OAI/arXiv/}"

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

RECORDS = Path("records.jsonl")

def fetch_result_paths():
    return list(RESULTS.glob("results-*.xml"))

def strip_record(record):
    arxiv = record.find(f"{OA}metadata/{ARX}arXiv")
    if arxiv is None:
        return None
    
    authors = []

    for a in arxiv.findall(f"{ARX}authors/{ARX}author"):
        keyname = a.findtext(f"{ARX}keyname")
        fornames = a.findtext(f"{ARX}forenames")
        authors.append({"keyname" : keyname, "forenames" : fornames})

    cats = (arxiv.findtext(f"{ARX}categories") or "").split()

    return{
        "id" : arxiv.findtext(f"{ARX}id"),
        "title" : arxiv.findtext(f"{ARX}title") or "",
        "created" : arxiv.findtext(f"{ARX}created"),
        "categories" : cats,
        "primary" : cats[0] if cats else None,
        "authors" : authors
    }

def iterate_records():
    for path in fetch_result_paths():
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        for record in root.findall(f".//{OA}record"):
            rec = strip_record(record)
            if rec is not None:
                yield rec

def dump_records():
    n = 0
    with RECORDS.open("w", encoding="utf-8") as rf:
        for record in iterate_records():
            rf.write(json.dumps(record, ensure_ascii=False) + "\n")
            n += 1
    print(f"Populated {str(RECORDS)} with {n} records.")

dump_records()
    