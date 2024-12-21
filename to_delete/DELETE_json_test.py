import json 

with open("prastalo_pitanja.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    for i, entry in enumerate(data):
        print(i, entry["odgovor"] + "\n-----------------------------\n\n")

#print(data)