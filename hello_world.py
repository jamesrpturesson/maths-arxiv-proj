import requests
from collections import Counter
import xml.etree.ElementTree as ET

print("Hello arXiv!")
BASE = "https://oaipmh.arxiv.org/oai"
NS = "{http://www.openarchives.org/OAI/2.0/}"
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
record_list = root.findall(f".//{NS}record")
spec_counter = Counter()
for record in record_list:
    #print("SPECS")
    record_specs = record.findall(f".//{NS}setSpec")
    for spec in record_specs:
        spec_counter[spec.text] += 1
    #print("\n")
print(spec_counter)
print(f"{len(record_list)} records")