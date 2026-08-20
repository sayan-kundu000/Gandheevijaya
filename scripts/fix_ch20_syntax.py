import re

filepath = 'frontend/src/data/gita/part1.ts'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Clean up any malformed ch20Data paragraphs property containing leftover string arrays
content_modified = False

# Replace legacy ch18_50_Shlokas references in fix patterns
legacy_50_shlokas = 'shlokasData: ch18_50_Shlokas as any,'
target_78_shlokas = 'shlokasData: ch18_78_Shlokas as any,'

if legacy_50_shlokas in content:
    content = content.replace(legacy_50_shlokas, target_78_shlokas)
    content_modified = True

legacy_map_50 = '(ch18_50_Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),'
target_map_78 = '(ch18_78_Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),'

if legacy_map_50 in content:
    content = content.replace(legacy_map_50, target_map_78)
    content_modified = True

# Regex fix for any orphaned paragraph strings left after paragraphs mapping
pattern = r'(paragraphs:\s*\(ch18_78_Shlokas as any\[\]\)\.map\(s => s\.paragraphText \|\| s\.fullExplanation\),)\s*(?:"[^"]*",?\s*)*\],?'
if re.search(pattern, content):
    content = re.sub(pattern, r'\1', content)
    content_modified = True

if content_modified:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully verified and cleaned ch20Data syntax in part1.ts!')
else:
    print('No syntax errors found. ch20Data in part1.ts is clean!')

