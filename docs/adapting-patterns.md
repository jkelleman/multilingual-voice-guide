# Adapting conversation patterns across cultures

Translation keeps the words. Adaptation keeps the **intent**. A conversation pattern that works in en-US can fail in another market even when the translation is perfect, because what counts as polite, clear, or trustworthy is different.

This doc covers the patterns that change most across the five locales in this repo. Patterns reference the companion repo [support-agent-pattern-library](https://github.com/jkelleman/support-agent-pattern-library).

## Apologies (`recover-from-misunderstanding`, every pattern)

**en-US rule:** one short apology at most, only when something went wrong on our side.

| Locale | Adaptation |
|---|---|
| ja-JP | A short apology for the inconvenience (ご不便をおかけして申し訳ありません) is expected even when it isn't our fault. Leaving it out reads as cold. Keep it to one, then lead with the answer. |
| de-DE | A brief "Das tut mir leid" is fine. Extended apologizing reads as insincere. Precision ("bis zum 3. Dezember") builds more trust than apology. |
| es-419, pt-BR | Close to en-US. A warm, brief "Lo siento" / "Sinto muito" works. Avoid the formal written-letter style ("Lamentamos informarle..."). |

**Eval impact:** the `empathy_appropriate` criterion in [golden-dataset-kit](https://github.com/jkelleman/golden-dataset-kit) needs locale-specific boundary examples. A ja-JP turn with one apology for something that wasn't our fault is a pass, not a fail.

## Formality and register (every pattern)

| Locale | Choice | The risk |
|---|---|---|
| es-419 | tú | usted feels distant for a streaming brand in most markets; voseo only works in some countries |
| pt-BR | você | o senhor / a senhora feels like a bank |
| de-DE | du (match UI) | switching between du and Sie across app and support feels like two companies |
| ja-JP | 丁寧語 polite form | over-honorific scripts slow members down; casual form feels disrespectful |

**Rule:** register is chosen once per locale and never changes mid-conversation, even for serious moments. A fraud case in de-DE stays *du*. Tone gets more serious; register doesn't move.

## Cancellation (`respectful-cancellation`)

- **de-DE:** use the plain legal verb *kündigen*. Softer wording ("beenden", "pausieren") can confuse members about whether they've actually cancelled. Some markets also regulate how easy online cancellation must be, so check with legal for each market.
- **All locales:** the one-offer limit holds everywhere. Guilt phrasing has local versions ("¿Seguro que quieres irte?") and every one goes on the banned list.

## Clarifying questions (`clarify-ambiguous-intent`)

- Option labels must be written in the locale, not translated from English. Members in each market describe problems differently. Mine local "something else" replies to rename options.
- **ja-JP:** direct either/or questions can feel abrupt. Soften with のでしょうか rather than adding more options.

## Dates, money, numbers (`confirm-before-action`)

The confirmation pattern depends on exact values, so formats have to be right:

| Locale | Date | Money |
|---|---|---|
| en-US | December 3 | $7.99 |
| es-419 | 3 de diciembre | varies by country |
| pt-BR | 3 de dezembro | R$ 20,90 |
| de-DE | 3. Dezember | 7,99 € |
| ja-JP | 12月3日 | ¥990 |

Formatting comes from the platform's locale library, never from the model. A model asked to "format the date for Germany" will sometimes get it wrong.

## Escalation (`escalate-to-human`)

- Wait times: say minutes in every locale, but never promise a time the queue system didn't provide.
- Human agent availability differs by language and hour. If the member's language isn't staffed right now, say so up front and offer the options: wait, callback, or another language. Don't silently route a Japanese-speaking member to an English queue.

## Live events across time zones

A live event at 8pm in New York is morning in Tokyo and early hours in Europe. Surge support (see [live-event-surge-playbook](https://github.com/jkelleman/live-event-surge-playbook)) has to work in every locale at once, which is why `known_incident` is one of the turns every locale must cover.
