# Localization QA checklist

Run this before any new or changed agent turn ships in a locale.

## Automated (CI)

- [ ] `python scripts/lint_locales.py` passes (coverage, placeholders, glossary, register)
- [ ] Warnings reviewed: banned phrases, expansion, voice length
- [ ] Golden-set items for this locale re-run against the judge (see golden-dataset-kit)

## Linguist review (native speaker, per locale)

- [ ] Reads as written in this language, not translated from English
- [ ] Register matches the locale decision (tú / você / du / 丁寧語) in every turn
- [ ] Vocabulary is right for the region (es-419 not es-ES; pt-BR not pt-PT)
- [ ] Glossary terms match the in-product UI exactly
- [ ] Dates, money, and numbers come from placeholders, not hard-coded
- [ ] No local support-speak or guilt phrasing
- [ ] Apology level fits local expectations (see docs/adapting-patterns.md)

## Voice (if the turn is used on the phone line)

- [ ] Listened to the actual TTS output, not just read the text
- [ ] Under ~10 seconds spoken
- [ ] No URLs, lists, or more than two options
- [ ] Numbers and codes are pronounced correctly by the TTS voice
- [ ] Pauses land at natural places (adjust punctuation if not)

## Conversation context

- [ ] The turn makes sense after the turns that come before it in this locale (pronoun references, gender agreement)
- [ ] Gender-neutral where the member's gender is unknown (es/pt/de can force a gendered form; rephrase rather than guess)
- [ ] Option labels match how members in this market describe the problem

## Sign-off

| Locale | Linguist | Date | Notes |
|---|---|---|---|
| es-419 | | | |
| pt-BR | | | |
| de-DE | | | |
| ja-JP | | | |

Update `review_status` in the locale file to `reviewed` after sign-off.
