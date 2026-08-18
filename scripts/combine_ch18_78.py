import json

part1_json = 'frontend/src/data/gita/bhagavad_gita_ch18_50_shlokas.json'
part2_json = 'frontend/src/data/gita/bhagavad_gita_ch18_part2_28_shlokas.json'
full_json = 'frontend/src/data/gita/bhagavad_gita_ch18_78_shlokas.json'

with open(part1_json, 'r', encoding='utf-8') as f:
    data1 = json.load(f)

with open(part2_json, 'r', encoding='utf-8') as f:
    data2 = json.load(f)

full_data = data1 + data2
print(f"Combined {len(data1)} + {len(data2)} = {len(full_data)} shlokas!")

with open(full_json, 'w', encoding='utf-8') as f:
    json.dump(full_data, f, ensure_ascii=False, indent=2)

print("Saved complete 78 shlokas JSON to:", full_json)
