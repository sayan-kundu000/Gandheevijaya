import re

filepath = 'frontend/src/data/gita/part1.ts'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern matching the broken ch20Data paragraphs property
old_broken_block = '''export const ch20Data: ChapterDetailContent = {
  chapterId: 20,
  title: "Chapter 18: Moksha Sannyasa Yoga — Ultimate Freedom & Renunciation",
  subtitle: "Renunciation of outcome anxiety, duty, decision-making, surrender, and supreme mastery.",
  confidenceScore: 99.9,
  shlokasData: ch18_50_Shlokas as any,
  paragraphs: (ch18_50_Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),
    "Chapter 18 Moksha Sannyasa Yoga is the grand synthesis of the entire Bhagavad Gita. It clarifies the critical distinction between Sannyasa (renunciation of selfish actions) and Tyaga (renunciation of anxiety over the fruits of action). True freedom comes not from abandoning your duties or quitting exams, but from executing your duty (Swadharma) with 100% focus while surrendering outcome panic.",
    "The chapter analyzes the 5 factors of action (the body, the actor, the instruments, the effort, and providential laws), the 3 types of knowledge, action, actor, intellect, fortitude, and happiness. It concludes with Krishna's ultimate declaration: 'Abandon all outcome anxieties and take refuge in Me alone; I shall liberate you from all fear; do not grieve.' When you step into the exam hall with complete commitment and total surrender of result obsession, you experience absolute cognitive freedom (Moksha)."
  ],'''

new_clean_block = '''export const ch20Data: ChapterDetailContent = {
  chapterId: 20,
  title: "Chapter 18: Moksha Sannyasa Yoga — Ultimate Freedom & Renunciation",
  subtitle: "Renunciation of outcome anxiety, duty, decision-making, surrender, and supreme mastery.",
  confidenceScore: 99.9,
  shlokasData: ch18_50_Shlokas as any,
  paragraphs: (ch18_50_Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),'''

if old_broken_block in content:
    content = content.replace(old_broken_block, new_clean_block)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully fixed ch20Data syntax in part1.ts!')
else:
    print('Pattern not matched in part1.ts')
