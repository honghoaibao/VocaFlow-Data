# VocaFlow editorial style guide

This guide sets an original editorial standard for vocabulary and English-learning articles in VocaFlow. It draws on high-level patterns visible in established learner resources—clear level labels, skill-focused organization, worked examples, practice, and a defined next step—without copying another publisher's text, branding, layout, or lesson content.

## 1. Begin with the learner

- Name the intended audience and level (CEFR A1, A2, B1, etc.) in metadata or the opening.
- State one practical learning outcome in everyday language.
- Prefer one small problem or question over a broad essay topic.
- Use a respectful, encouraging voice. Do not shame learners for forgetting or making errors.
- Explain technical terms briefly in Vietnamese when the intended reader may not know them.

## 2. Use a predictable teaching structure

For most 4–7 minute learning articles:

1. **Opening:** a relatable situation and the main learning goal.
2. **Core idea:** explain one concept without overloading the reader.
3. **Worked example:** show a short, original English example and explain why it works.
4. **Practice steps:** give a manageable task the reader can do immediately.
5. **Error guidance:** show what to do when an answer is wrong or a rule is confusing.
6. **Recap and next action:** summarize the key idea and suggest one small activity.

Adjust this structure for a grammar note, reading guide, or vocabulary explainer; it is a guide, not a rigid template.

## 3. Write for comprehension

- Use descriptive headings that tell the learner what they will do or understand.
- Keep paragraphs focused on one idea. Prefer active voice and concrete verbs.
- Introduce no more than a few new technical terms at once.
- Give correct, natural, level-appropriate English examples. Check articles, verb agreement, tense, punctuation, capitalization, and British/American spelling consistency.
- Explain an example in context rather than merely translating it.
- Avoid unsupported promises such as “learn anything instantly” or invented claims about memory or exam results.
- Keep word counts and reading-time estimates realistic; reading time is an estimate, not a performance promise.

## 4. Make practice purposeful

- Include an action the learner can complete now: retrieve a meaning, finish a sentence, compare two examples, read and answer a question, or plan a brief review.
- Make instructions unambiguous and provide a clear way to check the work.
- Explain that an error helps identify what to practise next; do not treat an error as a judgement of ability.
- Keep exercises aligned with the article's stated outcome and learner level.
- When suggesting a review timetable, call it a starting suggestion and allow intervals to adapt to the learner's results.

## 5. Vocabulary-pack requirements

Each published vocabulary record must include:
- a stable unique ID;
- the English word or phrase;
- a concise Vietnamese meaning with important senses separated by semicolons when useful;
- part of speech;
- an IPA pronunciation guide checked for the intended UK/US variety;
- a natural, grammatical example sentence;
- a clear topic and CEFR level supplied by the pack or record.

Before publishing, review duplicate words/IDs across packs, misleading translations, unnatural collocations, examples that merely repeat the definition, inconsistent spelling varieties, and IPA typos. Keep examples original and suitable for a general audience.

## 6. Research without copying

- Consult reputable learner-facing publishers (for example, British Council LearnEnglish and Cambridge English) to understand structure, level labeling, how examples are explained, and how practice is integrated.
- Write all explanations, examples, headings, and exercises in VocaFlow's own words. Do not copy paragraphs, quizzes, lesson sequences, images, or distinctive interface design.
- Link to external learning resources for the original publisher's page; describe what learners can do there without promising that a particular activity will remain unchanged.
- Record a source URL for editorial fact-checking when a specific claim needs verification. Do not invent a source or citation.

## 7. JSON and reader compatibility

- Use schemaVersion 1, status "published", a stable kebab-case article ID, an ISO date (YYYY-MM-DD) matching the filename and manifest, and an honest readingMinutes estimate.
- Prefer supported block types: paragraph, heading, quote, callout, bulletList, numberedList, divider, image, and video.
- Every text span should have meaningful text. Use only approved styling fields and colors; image sources must be safe HTTPS URLs or allowed app asset paths; YouTube IDs must be 11 valid characters.
- Keep useful text if an optional image/video is removed. Never make essential instructions available only through an image.
- Run python3 tool/validate_content.py and inspect the rendered article in the app before approving a release.

## 8. Final editorial checklist

- [ ] Target reader and level are clear.
- [ ] Learning outcome is specific and supported by the article.
- [ ] English and Vietnamese wording, punctuation, translations, IPA and examples have been reviewed.
- [ ] The article contains an original worked example and a concrete practice step.
- [ ] Claims are measured and credible; no guarantee of outcomes is implied.
- [ ] The content is original and avoids reproducing a publisher's text.
- [ ] Title, date, author, reading time, topic metadata, block schema and assets are valid.
- [ ] A second pass checks typos, duplicate IDs, missing fields and the in-app reading experience.


## 9. Long-form article quality gate (VocaFlow)

- A first-party in-app article requested as a substantial guide should contain 200–2,000 words. Aim for roughly 600–1,000 words when the topic supports it; do not pad a narrow topic merely to increase length.
- If an older article feels skeletal, improve it with clearer explanations, original worked examples, common-error guidance, and a self-check rather than simply changing its title.
- Add at least one practical exercise and include enough context for the learner to check the answer. Keep answers close to the exercise or explain how to verify them.
- Give each article an appropriate cover image with relevant imageAlt and accurate imageCredit. Do not use a third-party video thumbnail without permission.
- Count text from the blocks actually rendered by the app. Update readingMinutes conservatively after editing.
