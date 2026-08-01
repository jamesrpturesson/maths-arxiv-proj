import requests
from collections import Counter
import xml.etree.ElementTree as ET

print("Hello arXiv!")
BASE = "https://oaipmh.arxiv.org/oai"
OA = "{http://www.openarchives.org/OAI/2.0/}"
ARX = "{http://arxiv.org/OAI/arXiv/}"
user = "maths-arxiv-proj/0.1"

r = requests.get(
    BASE, 
    params={"verb": "ListRecords", "set": "math", "metadataPrefix": "arXiv"},
    headers={"User-Agent": user},
    timeout=40
)

with open("results.xml", "w", encoding="utf-8") as rf:
    rf.write(r.text)

r.raise_for_status()
root = ET.fromstring(r.text)
record_list = root.findall(f".//{OA}record")
spec_counter = Counter()
cat_counter = Counter()
for record in record_list:
    #print("SPECS")
    record_specs = record.findall(f".//{OA}setSpec")
    for spec in record_specs:
        spec_counter[spec.text] += 1/len(record_specs)
    #print("\n")
    record_cats = record.findall(f".//{ARX}categories")
    rc_split = record_cats[0].text.split()
    for cat in rc_split:
        cat_counter[cat] += 1/len(rc_split)
print(spec_counter)
print(cat_counter)
print(f"{len(record_list)} records")

r = requests.get(
    BASE, 
    params={"verb": "ListSets"},
    headers={"User-Agent": user},
    timeout=40
)
r.raise_for_status()
with open("sets.xml", "w", encoding="utf-8") as rf:
    rf.write(r.text)

root = ET.fromstring(r.text)

for st in root.findall(f".//{OA}set"):
    spec = st.find(f"{OA}setSpec").text
    name = st.find(f"{OA}setName").text
    print(f"{spec} {name}")