import requests
from collections import Counter
import xml.etree.ElementTree as ET
import json
import time
from pathlib import Path

print("Hello arXiv!")
BASE = "https://oaipmh.arxiv.org/oai"
OA = "{http://www.openarchives.org/OAI/2.0/}"
ARX = "{http://arxiv.org/OAI/arXiv/}"
user = "maths-arxiv-proj/0.1"

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)
CATEGORIES = Path("categories")
CATEGORIES.mkdir(exist_ok=True)

MAX_PAGES = 5

def grab_results():
    params = {"verb": "ListRecords", "set": "math", "metadataPrefix": "arXiv"}
    page = 0
    while True:
        print(f"Fetching page {page}")
        r = requests.get(
            BASE, 
            params=params,
            headers={"User-Agent": user},
            timeout=40
        )

        r.raise_for_status()
        root = ET.fromstring(r.text)
        yield r.text
        page += 1
        if page >= MAX_PAGES:
            return

        token = root.find(f".//{OA}resumptionToken")
        if token is None or not (token.text or "").strip():
            return
        params = {
            "verb": "ListRecords", 
            "resumptionToken" : token.text.strip()
            }
        time.sleep(3)

def generate_results():
    
    for i, txml in enumerate(grab_results()):
        path = RESULTS / f"results-{i:04d}.xml"
        print(f"Writing to results-{i:04d}.xml")
        with open(path, "w", encoding="utf-8") as rf:
            rf.write(txml)

    #record_list = root.findall(f".//{OA}record")
    #spec_counter = Counter()
    #cat_counter = Counter()
    #for record in record_list:
    #    #print("SPECS")
    #    record_specs = record.findall(f".//{OA}setSpec")
    #    for spec in record_specs:
    #        spec_counter[spec.text] += 1/len(record_specs)
    #    #print("\n")
    #    record_cats = record.findall(f".//{ARX}categories")
    #    rc_split = record_cats[0].text.split()
    #    for cat in rc_split:
    #        cat_counter[cat] += 1/len(rc_split)

def grab_list_set():
    params = {"verb": "ListSets"}
    page = 0
    while True:
        r = requests.get(
            BASE, 
            params=params,
            headers={"User-Agent": user},
            timeout=40
        )
        r.raise_for_status()
        root = ET.fromstring(r.text)
        yield r.text
        page += 1
        if page >= MAX_PAGES:
            return
        
        token = root.find(f".//{OA}resumptionToken")
        if token is None or not (token.text or "").strip():
            return
        params = {"verb": "ListSets", "resumptionToken" : token.text.strip()}
        time.sleep(3)

def generate_list_set():
    cat_dict = {}
    for i, s in enumerate(grab_list_set()):

        path = CATEGORIES / f"sets-{i:02d}.xml"

        print(f"Writing to sets-{i:02d}.xml")
        with open(path, "w", encoding="utf-8") as rf:
            rf.write(s)
        
        root = ET.fromstring(s)
        
        for st in root.findall(f".//{OA}set"):
            spec = st.find(f"{OA}setSpec").text
            name = st.find(f"{OA}setName").text
            hierarchy = spec.split(":")
            if len(hierarchy) == 3:
                cat_dict[f"{hierarchy[1]}.{hierarchy[2]}"] = name
            else:
                cat_dict[f"{hierarchy[-1]}"] = name

    path = CATEGORIES / "categories.json"
    print("Writing to categories.json")
    with open(path, "w", encoding="utf-8") as cf:
        json.dump(cat_dict, cf, indent=2, ensure_ascii=False)

generate_results()
generate_list_set()
