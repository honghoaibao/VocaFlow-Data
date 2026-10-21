# VocaFlow Vocabulary Pack Authoring Guide

Required production standard for all new or revised vocabulary packs. A pack must teach words in context, support active recall, and preserve reliable study progress—not merely list English–Vietnamese translations.

## 1. File placement and publication

- File path: `assets/vocabulary/packs/<topic>_<level>_YYYY-MM-DD.json`.
- Use `schemaVersion: 1`, `status: "published"`, a stable pack `id`, `topic`, CEFR `level`, `publishDate`, `title`, `description`, a non-empty `words` array, and cover image metadata.
- The date in the filename, pack `publishDate`, and `assets/content/index.json` manifest entry must match.
- Word IDs must be stable, lower-case kebab-case, and unique across every published pack. Do not rename an ID after release merely to improve its label: stored learner progress refers to the ID.
- Never put learner records, account information, passwords, access tokens or secrets into this public repository.

## 2. Required fields for each word

Every word must include `id`, `word`, `meaning`, `partOfSpeech`, `pronunciation`, `example`, `imageUrl`, `imageAlt`, and `imageCredit`.

**Meaning:** use concise Vietnamese, distinguish important senses with semicolons, and avoid translations too vague to separate from the pack's distractors.

**Part of speech:** choose an accurate label such as `noun`, `verb`, `adjective`, `adverb`, or `phrasal verb`. If a word has several uses, make sure the chosen label and example agree.

**Pronunciation:** use IPA checked against a reputable dictionary and keep one intended pronunciation variety (UK or US) consistent within the pack. Do not guess pronunciation from spelling.

**Example:** create a natural, grammatical sentence appropriate to the CEFR level. Include the exact headword/phrase so the app can mask it for contextual cloze practice. Review articles, subject–verb agreement, tense, prepositions, punctuation and collocations. Do not simply restate the translation.

**Distractors:** the app may use pack words to create multiple-choice options. Avoid duplicate meanings and near-synonyms in the same study batch unless the exercise explicitly tests their distinction. There must be one defensible correct answer.

## 3. Images and accessibility

Each pack cover, word illustration, article cover/block image and discovery-resource image must have a distinct underlying image source across the entire published catalog. Reusing the same photo with a different crop, width or query string is still a duplicate.

- Use an absolute HTTPS URL from a source with appropriate reuse rights.
- Provide a short, meaningful `imageAlt` and accurate `imageCredit`.
- Choose imagery that reinforces the word or topic; avoid generic photographs that could represent almost anything.
- Check how the image crops in the app's fixed mobile card frame.
- Do not copy publisher graphics or third-party video thumbnails without verified permission.
- The validator identifies a source by hostname and path, deliberately ignoring crop parameters.

## 4. How a VocaFlow pack is taught

The app can select up to six words for one short lesson and prioritizes words due for review. Keep the learning sequence consistent:

1. **Familiarize:** show the illustration, English word, pronunciation, part of speech, Vietnamese meaning and example when available.
2. **Recall meaning:** ask the learner to retrieve the meaning before seeing feedback. Wrong options should be plausible but clearly distinguishable.
3. **Use in context:** hide the target word/phrase in its complete example sentence. The intended answer must fit naturally in the sentence.
4. **Type the word:** require recall of spelling without exposing automatic hints.
5. **Match pairs:** when at least two suitable words are available, match English words to Vietnamese meanings. Avoid duplicate meanings within the same batch.
6. **Review adaptively:** each judged answer updates the learner's local record immediately. Mistakes should increase review priority; confident correct responses may lengthen the interval. Record lesson completion once.

A content pack must not hard-code user mastery, due dates or review state. Spaced repetition belongs to the individual learner's progress record, not the public content file.

## 5. Pack size and balance

- Prefer focused packs of approximately 10–20 related words; do not force this range when the topic needs a smaller or larger pack.
- Prioritize common and useful words at the selected level, including vocabulary that supports high-school graduation exam tasks when relevant.
- Include a practical mix of nouns, verbs, adjectives and phrases where the theme allows.
- Keep examples brief enough for mobile without stripping away the context needed to understand the word.
- Do not inflate pack size with near-duplicates, obscure words, or entries whose example does not demonstrate the intended meaning.

## 6. Required checks before publishing

1. Validate the JSON, metadata, schema and manifest dates.
2. Check all word IDs for duplicates across the repository.
3. Review Vietnamese meaning, part of speech, IPA, spelling, example grammar and the exact target word in the example.
4. Review every image URL, alternative text, credit, relevance and underlying source uniqueness.
5. Run `python3 tool/validate_content.py`.
6. Inspect the pack on a narrow Android screen, including card crops, answer choices and the offline cached/bundled experience.
7. Update the manifest with the pack and commit the JSON, metadata and documentation together.

## Release checklist

- [ ] Metadata and filename are consistent.
- [ ] IDs are stable and unique across packs.
- [ ] Meaning, POS, IPA and example are accurate.
- [ ] The target word occurs in a natural example sentence.
- [ ] Practice choices are fair and unambiguous.
- [ ] Every image is unique, topic-relevant, HTTPS and credited.
- [ ] No user data, passwords or tokens are present.
- [ ] Automated validation and Android rendering checks pass.
