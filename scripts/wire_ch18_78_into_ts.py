import re

part1_path = 'frontend/src/data/gita/part1.ts'
with open(part1_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update import statement at the top of part1.ts
old_import = 'import ch18_50_Shlokas from "./bhagavad_gita_ch18_50_shlokas.json";'
new_import = 'import ch18_78_Shlokas from "./bhagavad_gita_ch18_78_shlokas.json";'

if old_import in content:
    content = content.replace(old_import, new_import)

# 2. Update ch20Data inside part1.ts to use ch18_78_Shlokas
content = content.replace('shlokasData: ch18_50_Shlokas as any,', 'shlokasData: ch18_78_Shlokas as any,')
content = content.replace('(ch18_50_Shlokas as any[]).map', '(ch18_78_Shlokas as any[]).map')

with open(part1_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated part1.ts with all 78 Shlokas of Chapter 18!")
