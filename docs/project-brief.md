# Project Brief

## Purpose

Bettors build tickets on gut feeling and bookmaker odds, and often miss what matters: a top scorer is injured, a coach plans to rest players, a team has not scored without its striker. Bet Researcher researches every game on a ticket and explains, in plain language backed by past results, how likely each pick and the whole ticket are to win.

## Users

| User | Need | Workflow |
| --- | --- | --- |
| Casual bettor | Know if a ticket makes sense before placing it | Paste picks or drop a bet slip screenshot → read the verdict |
| Regular bettor | Understand why a pick is risky, find safer swaps | Open each game's research page → swap weak picks |

## Goals

- Estimate each team's goals in a match the same way every time ([method](method.md)).
- Explain every number with what has happened before ("Kane scores almost every game: 11 in 12").
- Give the chance of each pick and of the whole ticket, and compare with the bookmaker.
- Surface team news people might miss.

## Non-Goals

- Placing bets or handling money.
- Guaranteeing outcomes or selling "sure tips".
- Sports other than football; markets other than goal-based ones in v1 (no corners or cards).
- Live in-play predictions in v1.

## Success Criteria

| Metric | Target |
| --- | --- |
| Calibration | Picks we rate around 60% win around 60% of the time, measured over at least 200 picks |
| Versus bookmaker | Our chances are at least as accurate as closing odds (Brier score) |
| Speed | A 3-game ticket is fully analysed in under 2 minutes |
| Clarity | Every verdict has a plain-language reason backed by a number |

## Scope

In scope (v1): ticket input by text or image; per-game research page; combined ticket page; top 5 European leagues.

Out of scope (v1): Champions League (needs league-strength adjustment), corners and cards, user accounts, live alerts.

## Constraints

- Budget: API-Football free plan (100 requests a day) during development; Gemini pay-as-you-go.
- Platform: web (desktop and mobile).
- Compliance: research tool, not a bookmaker. Check local rules on betting-tips services and app-store gambling policies before launch.
- Data: API-Football terms restrict redistribution; check before showing data publicly.

## Key Decisions Needed

- [ ] Hosting platform (own decision record before first deploy).
- [ ] Gemini model choice (set in `GEMINI_MODEL`).

## Open Questions

- [ ] Which leagues beyond the top 5, and when?
- [ ] Free product, paid, or both?
