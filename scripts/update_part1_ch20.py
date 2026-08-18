import re

filepath = 'frontend/src/data/gita/part1.ts'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import_line = 'import ch18_50_Shlokas from "./bhagavad_gita_ch18_50_shlokas.json";\n'
if 'ch18_50_Shlokas' not in content:
    content = import_line + content

target = 'export const ch20Data: ChapterDetailContent = {'

replacement = '''export const ch20Data: ChapterDetailContent = {
  chapterId: 20,
  title: "Chapter 18: Moksha Sannyasa Yoga — Ultimate Freedom & Renunciation",
  subtitle: "Renunciation of outcome anxiety, duty, decision-making, surrender, and supreme mastery.",
  confidenceScore: 99.9,
  shlokasData: ch18_50_Shlokas as any,
  paragraphs: (ch18_50_Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),'''

pattern = r'export const ch20Data: ChapterDetailContent = \{\s*chapterId: 20,\s*title: [^\n]+\s*subtitle: [^\n]+\s*confidenceScore: 99\.9,\s*paragraphs: \['

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully wired ch18_50_Shlokas into ch20Data!')
else:
    print('Pattern not matched in part1.ts')
