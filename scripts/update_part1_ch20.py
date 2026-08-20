import re

filepath = 'frontend/src/data/gita/part1.ts'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ensure correct import statement for all 78 shlokas
if 'ch18_50_Shlokas' in content:
    content = content.replace(
        'import ch18_50_Shlokas from "./bhagavad_gita_ch18_50_shlokas.json";',
        'import ch18_78_Shlokas from "./bhagavad_gita_ch18_78_shlokas.json";'
    )

import_line = 'import ch18_78_Shlokas from "./bhagavad_gita_ch18_78_shlokas.json";\n'
if 'ch18_78_Shlokas' not in content:
    content = import_line + content

# 2. Safely wire shlokasData and dynamic paragraphs mapping into ch20Data
content = re.sub(
    r'shlokasData:\s*ch18_(?:50|78)_Shlokas as any,',
    'shlokasData: ch18_78_Shlokas as any,',
    content
)

content = re.sub(
    r'paragraphs:\s*\(ch18_(?:50|78)_Shlokas as any\[\]\)\.map\(s => s\.paragraphText \|\| s\.fullExplanation\),',
    'paragraphs: (ch18_78_Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully wired ch18_78_Shlokas into ch20Data in part1.ts!')

