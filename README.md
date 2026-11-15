<p align="center"><img src="assets/banner.png" alt="Multilingual Voice Guide banner: speech bubbles saying hello in five languages" width="100%"></p>

# Multilingual Voice Guide: Voice and Tone Localization for Conversational AI

[![Lint locales](https://github.com/jkelleman/multilingual-voice-guide/actions/workflows/lint.yml/badge.svg)](https://github.com/jkelleman/multilingual-voice-guide/actions/workflows/lint.yml)
![locales: en · es · pt · de · ja](https://img.shields.io/badge/locales-en%20%C2%B7%20es%20%C2%B7%20pt%20%C2%B7%20de%20%C2%B7%20ja-14627a)
![focus: voice & tone](https://img.shields.io/badge/focus-voice%20%26%20tone-7ce0c3)
![channels: chat + voice](https://img.shields.io/badge/channels-chat%20%2B%20voice-0c3c4c)
![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Built by Jen Kelleman](https://img.shields.io/badge/built%20by-Jen%20Kelleman-555555?logo=github&logoColor=white)](https://github.com/jkelleman)

A voice-and-tone system for an AI customer-support agent that works in many languages: one core voice, decisions for each locale (register, apology level, vocabulary), the same seven support turns written in five locales, a shared glossary, a localization QA checklist, and a linter that catches missing turns, broken placeholders, glossary drift, wrong register, and voice turns that run too long.

> Independent portfolio project by [Jen Kelleman](https://github.com/jkelleman). Not affiliated with or endorsed by Netflix. Translations are design drafts by the author and are marked `draft-needs-native-review`. Production use requires native-speaking linguists, and the QA checklist includes that step.

---

## Why this exists

A global support agent has to sound like the same company in every language, and that's harder than translating a style guide. Formality, how much to apologize, how direct to be, and what's even legally required in a cancellation flow all change by market. A turn that's warm in English can read as cold in Japanese or vague in German, and a turn that fits a 10-second voice budget in English can run 12 seconds in German.

This repo treats multilingual voice as a system with rules you can check, not a set of translated strings.

## One turn, five locales

The `known_incident` turn: something is broken on our side during a busy moment.

| Locale | Turn |
|---|---|
| en-US | We're seeing a problem right now that's affecting some members in your area. Our team is working on it, and you don't need to restart anything. |
| es-419 | En este momento hay un problema que afecta a algunos miembros de tu zona. Nuestro equipo ya está trabajando en ello y no necesitas reiniciar nada. |
| pt-BR | Estamos com um problema no momento que está afetando alguns assinantes na sua região. Nossa equipe já está trabalhando nisso, e você não precisa reiniciar nada. |
| de-DE | Gerade gibt es ein Problem, das einige Mitglieder in deiner Region betrifft. Unser Team arbeitet bereits daran. Du musst nichts neu starten. |
| ja-JP | 現在、お住まいの地域の一部のメンバーに影響する問題が発生しています。担当チームが対応中のため、機器を再起動していただく必要はありません。 |

Notice what changed besides the words: pt-BR says *assinantes* (subscribers) because "members" isn't natural for a paid service there; de-DE splits into short sentences; ja-JP explains *why* no restart is needed (the team is handling it), which reads as more considerate.

## What's inside

```
voice/core-voice.md           4 voice attributes, tone by moment, words to use/avoid, chat vs voice
docs/adapting-patterns.md     how apologies, register, cancellation, and dates change by culture
locales/*.yaml                7 support turns × 5 locales, with register decisions and notes
glossary/glossary.csv         shared terms across locales
checklists/localization-qa.md automated + linguist + voice QA before shipping
scripts/lint_locales.py       the linter (runs in CI)
scripts/lint_config.yaml      per-locale budgets, banned phrases, register rules
```

## Locale decisions at a glance

| Locale | Register | Biggest adaptation |
|---|---|---|
| en-US | you, contractions | Source, not standard |
| es-419 | tú | Neutral Latin American vocabulary; no voseo or Spain-only terms |
| pt-BR | você | *Assinatura/assinante* instead of "member"; *estornar* for refunds |
| de-DE | du (match the UI) | Never switch register mid-conversation; *kündigen* for cancel; exact dates |
| ja-JP | 丁寧語 polite form | A short apology is expected even when it's not our fault; measure voice in seconds, not characters |

## Run the linter

```bash
pip install pyyaml
python scripts/lint_locales.py
```

```
locale  register       turns  length  longest  review
de-DE   du                 7   1.17x      12s  draft-needs-native-review
en-US   Direct second      7   1.00x      10s  source
es-419  tú                 7   1.05x       9s  draft-needs-native-review
ja-JP   丁寧語 (desu/mas      7   0.55x      10s  draft-needs-native-review
pt-BR   você               7   1.10x      11s  draft-needs-native-review

2 warning(s)
  ! de-DE/handoff: ~12s spoken (budget 10s) - trim or split for voice
  ! pt-BR/known_incident: ~11s spoken (budget 10s) - trim or split for voice
```

The two warnings are left in on purpose. They show the kind of problem that's invisible when you review each language on its own: the English turn fits the voice budget, and the German and Portuguese turns don't.

**What the linter checks**

| Check | Level | Example it catches |
|---|---|---|
| Turn coverage | Error | A new English turn shipped without a Japanese version |
| Placeholders | Error | `{date}` dropped or renamed in translation |
| Glossary | Error | pt-BR turn says "membro" where the glossary says "assinatura" |
| Register | Error | A formal *Sie* slipped into a *du* locale |
| Banned phrases | Warning | "Estimado cliente", "Sehr geehrte", "please be advised" |
| Expansion | Warning | A turn 1.5x longer than the source |
| Voice length | Warning | Estimated speaking time over 10 seconds |

## How this connects to a global streaming service

- **Scale.** Netflix describes its service as streaming in more than 30 languages across 190 countries ([Netflix job posting](https://builtincharlotte.com/job/senior-content-designer-ads-consumer/8558428)). A support agent has to keep up with that.
- **Netflix already does this for subtitles.** Netflix publishes a Timed Text Style Guide for each language, with rules that differ by market. The Dutch guide sets a 42-character line limit, for example, and the Simplified Chinese guide sets 16 ([Dutch](https://backlothelp.netflix.com/hc/en-us/articles/215350158-Dutch-Timed-Text-Style-Guide), [Simplified Chinese](https://backlothelp.netflix.com/hc/en-us/articles/215986007-Chinese-Simplified-Timed-Text-Style-Guide)). This repo applies the same idea to the support agent: shared rules, plus decisions for each locale that can be checked automatically.
- **The role asks for it directly.** The Conversational Designer posting calls for a consistent voice across multiple languages and attention to language and cultural nuance ([posting](https://www.workingnomads.com/jobs/conversational-designer-netflix)).

## Executive summary

**Problem.** A support agent localized string by string sounds like a different company in every market, breaks voice-time budgets in longer languages, and drifts from in-product terms.

**Approach.** One core voice, explicit per-locale decisions (register, apology level, vocabulary), a shared glossary, and a CI linter that blocks coverage, placeholder, glossary, and register errors before release.

**What it enables.**
- New turns ship in every locale together, or the build fails.
- Linguists review intent and nuance, not missing placeholders.
- Voice turns are checked against a speaking-time budget in every language.

## Companion repos

- [support-agent-pattern-library](https://github.com/jkelleman/support-agent-pattern-library): the patterns these turns come from
- [golden-dataset-kit](https://github.com/jkelleman/golden-dataset-kit): the eval rubric, including es-419 and pt-BR items
- [live-event-surge-playbook](https://github.com/jkelleman/live-event-surge-playbook): why `known_incident` has to work in every locale at once

## License

MIT. See [LICENSE](LICENSE).
