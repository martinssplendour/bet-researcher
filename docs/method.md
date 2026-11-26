# Bet Researcher: Match Analysis Method

How the app estimates each team's goals in a match, then turns that into the chance each prediction wins, and the chance the whole ticket wins. Every match goes through the same steps, in the same order.

**Status:** v1.1, 26 Nov 2026. Numbers marked *(tunable)* are starting values, to be adjusted once we have a track record.

---

## Who does what

| | Does |
|---|---|
| **Code** | Collects the data, does every calculation, builds a one-page fact sheet, and checks Gemini's output |
| **Gemini** | Searches the web for news about the match and both teams, turns that news into player statuses, weighs the fact sheet into a capped adjustment for each team, and explains its thinking to the user |

**Principle:** Gemini never receives raw data. It gets a one-page fact sheet plus the news it found. It never invents the core numbers: it adjusts them within limits and must give a reason for every adjustment.

## Overview

```
A. Gather data
B. History window                 last 12 games, current season first
C. Baseline expected goals        team ratings vs. opponent
D. Form and patterns
E. Players and availability
F. Schedule and motivation
G. Team news                      official list + Gemini news scout (web search)
H. Fact sheet and flags
I. Gemini analyst                 → final expected goals for each team
J. Predictions                    scoreline table → chance each prediction wins
K. Ticket                         chance the whole ticket wins
L. Updates and track record
```

Sections A–H, J and K are all code (deterministic). Gemini appears only in G (news scout) and I (analyst).

---

## A. Gather data (code)

Source: API-Football.

1. **Match details:** competition, season, home and away team, kickoff time. `/fixtures`
2. **Team matches:** each team's matches this season and last season, in all competitions. For each match: goals for and against, home or away, date, opponent, competition. `/fixtures` (by team and season)
3. **League matches:** every match in the league this season and last season, used for league averages. `/fixtures` (by league)
4. **League table:** position, points, games left. `/standings`
5. **Player stats:** goals, assists, minutes, starts, average match rating, penalties, cards. Current season, plus last season for players with little data this season. A new signing's numbers from their old club count. `/players`
6. **Lineups and player match ratings** for the matches used in the analysis. `/fixtures/lineups`, `/fixtures/players`
7. **Injuries and suspensions** for this match. `/injuries`
8. **Head-to-head:** the last 5–10 meetings. `/fixtures/headtohead`
9. **Bookmaker odds:** for comparison only, never used as an input. `/odds`

Finished matches never change, so their data is fetched once and stored. That keeps us within the free plan's 100 requests a day.

---

## B. History window (code)

10. **Each team's window is its last 12 matches,** chosen in this priority order, newest first within each tier:

    | Tier | Matches | Weight *(tunable)* |
    |---|---|---|
    | 1 | This season, this competition | 1.0 |
    | 2 | This season, other competitions | 0.7 |
    | 3 | Last season, this competition | 0.5 |

    Fill from tier 1 first and move to the next tier only if there are fewer than 12. Examples:
    - Mid-season league match: all 12 are this season's league games.
    - Early season (4 league games played): 4 league games, plus this season's cup and European games, then last season's league games until there are 12.
    - Champions League match: this season's Champions League games first, then this season's league games.
11. **Special cases** (each one raises a flag for Gemini):
    - **Promoted team:** last season's games were in a lower league, so they get weight 0.3 *(tunable)*.
    - **New manager:** the fact sheet states how many of the 12 games were under the current coach.
    - **Fewer than 6 games** in the window in total: low confidence.
12. **League averages** (home goals per game, away goals per game) come from every league match this season, not just the window. If fewer than 6 rounds have been played, blend in last season's averages.

---

## C. Baseline expected goals (code)

13. **Attack rating** = the team's weighted goals scored per game in the window ÷ the league average goals per team per game.
14. **Defence rating** = the team's weighted goals conceded per game in the window ÷ the same league average.
    Both ratings use all 12 games, home and away together. Splitting 12 games into 6 home and 6 away is too thin; home advantage comes in through step 16 instead.
15. **Protect against small samples.** Pull each rating toward average (1.0) when there are few games:
    `rating = (weighted games × raw rating + 5 × 1.0) ÷ (weighted games + 5)` *(the 5 is tunable)*.
16. **Baseline expected goals:**
    - Home = league average home goals × home attack × away defence
    - Away = league average away goals × away attack × home defence
17. **Bookmaker check.** Turn the odds into chances with the bookmaker's margin removed:
    `chance = (1 ÷ odds) ÷ the sum of (1 ÷ odds) over all outcomes`.
    Compare with our baseline win chance (section J). If they differ by more than 10 percentage points *(tunable)*, flag it, and Gemini must explain the gap.

How to read the ratings: an attack above 1.0 scores more than the league average. A defence above 1.0 concedes more than average, so it is weaker.

---

## D. Form and patterns (code)

18. **Form:** goals scored and conceded per game over the 5 most recent games, compared with the window average, as a percentage (for example, "attack −21%").
19. **Results:** W/D/L run and points per game over the last 5, compared with the window.
20. **Scoring habits** in the window, home and away separately: clean-sheet rate, failed-to-score rate, over 2.5 goals rate, both-teams-score rate.
21. **Goal spread:** the top scorer's share and the top 3's share of the team's goals. Is it a one-man team, or are there many threats?
22. **Head-to-head:** W/D/L, average goals and over 2.5 rate across the last 5–10 meetings. Light weight, because squads change.

---

## E. Players and availability (code)

23. **Starter rate:** games started ÷ games available, over the window. A first-choice player starts 70%+ of the games they're available for. Record each player's position.
24. **Player output:** goals + assists per 90 minutes, share of team goals, and average match rating. Use this season; if a player has fewer than 450 minutes, add last season. The rating covers defenders, midfielders and keepers, who rarely score.
25. **With/without split:** the team's goals scored and conceded per game with the player starting and without them, plus how many games each figure is based on. This uses this season and last season, not just the window, because absences are rare. Fewer than 4 games without the player means low confidence.
26. **Out or doubtful:** from the official injury list.
27. **Suspension risk:** red cards, and yellow cards against the league's ban threshold. Thresholds differ by league, so they're stored per league.
28. **Returning player:** missed the last 3+ games and is no longer on the injury list, so probably short of match fitness.
29. **Fatigue:** minutes played in the last 7 days, days since the last match, and the rest-day difference between the two teams.
30. **Expected XI:** the usual starters minus unavailable players. Each gap is filled by whoever most often starts in that position. The confirmed lineup replaces it about an hour before kickoff.
31. **Missing share:** the total goal share of players who are out, and separately of players who are out or doubtful.
32. **Lineup strength:** the expected XI's average rating ÷ the usual XI's average rating × 100.
33. **Replacement gap:** the replacement's goals + assists per 90 compared with the missing player's.
34. **Suggested adjustment** (code's starting point for Gemini):
    - **Attack factor:** take the most important missing attacker (highest goal share). `ratio = team goals per game without them ÷ with them`, then `factor = (games without × ratio + 5 × 1.0) ÷ (games without + 5)`.
    - **Defence factor:** the same calculation using goals conceded, for the most important missing defender or keeper.
    - **Team A's suggested multiplier** = A's attack factor × B's defence factor. A missing B centre-back makes A's number go up.

---

## F. Schedule and motivation (code)

35. **Rotation risk:** whether the next match is within 4 days, and how important it is. Importance ranking *(tunable)*: European knockout or final > title or relegation decider > European group or league phase > league > early domestic cup rounds. Also record how many lineup changes this coach usually makes before such games, from this season's and last season's lineups.
36. **Motivation:** the points gap to the title, European places and relegation, compared with the points still available. Code sets flags such as "title race", "relegation fight", "already safe" and "nothing to play for".

---

## G. Team news

37. **Official injury list** (step 26) is the starting point.
38. **Gemini news scout (Gemini with Google Search).**
    - **Code sends:** both teams, the competition, the match date, and the official injury list.
    - **Gemini searches** for news from the last 7 days about the match and both teams. It looks for injuries, doubts, press-conference quotes, predicted lineups, rotation hints, suspensions, illness, the manager's situation and off-field problems. It includes local-language press, which often has team news first.
    - **It returns a list of findings.** Each finding has: the player or topic; a status (out / doubtful / fit / returning / likely rested / other); the claim; the source link; the date; and whether it's confirmed or a rumour.
39. **Code checks the findings:**
    - every source link must appear in the search results Google returned, so no made-up links get through
    - findings older than 7 days are dropped
    - news that contradicts the official list is flagged as "things people might miss", never applied silently
    - all findings are saved with the analysis
40. **Display requirement:** Google's terms for search grounding require the app to show "Google Search suggestions" next to results that used search. Check the current terms before launch.

---

## H. Fact sheet and flags (code)

41. **Flags.** Rules point Gemini at what matters *(thresholds tunable)*:
    - missing share above 30%
    - fewer than 4 games of with/without history
    - bookmaker gap above 10 points
    - under 3 days' rest
    - high rotation risk
    - form swing above 30%
    - news contradicts the official list
    - new manager (fewer than 5 games)
    - promoted team
    - fewer than 6 games in the window
42. **Fact sheet.** Code bundles everything into one page per match. Example (made-up numbers):

```
MATCH      Bayern (H) vs Opponent · Bundesliga · Sat 15:30
WINDOW     Bayern: 12 league games this season · Opponent: 12 league games this season
BASELINE   Bayern 2.6 · Opponent 0.9 expected goals
BOOKMAKER  Bayern win 74% · our baseline 77% · gap 3 pts

BAYERN
  Form, last 5     2.2 scored / 0.8 conceded per game (window 2.8 / 0.9) → attack −21%
  Lineup strength  78 (usual XI = 100)
  Missing          Kane OUT 41% of goals · Olise DOUBT 19% · Díaz OUT 15% → total 74%
  Without Kane     1.6 goals/game in 3 games (2.9 with him)
  Goal spread      top 3 = 74% of goals (concentrated)
  Suggested adj.   ×0.83
  Schedule         4 days' rest · next: Champions League in 3 days · coach makes 3.1 changes before such games
  Motivation       1st, +4 pts, 22 games left
OPPONENT
  ... same format ...
FLAGS      ⚠ high missing share  ⚠ small sample (3 games)  ⚠ rotation risk
NEWS       [club site, Thu] "Kane will miss the next two weeks with a hamstring problem"
           [local paper, Fri] coach on Olise: "we'll see tomorrow"
```

---

## I. Gemini analyst → final expected goals

43. **A second Gemini call, without search.** Input: the fact sheet plus the checked news findings. The user watches its thinking live (Gemini's thought summaries). Output, in a fixed format, for each team:
    - a multiplier for that team's expected goals, starting from the suggested adjustment (step 34)
    - a breakdown of that multiplier by factor: players, lineup, news, schedule and motivation, form. The parts must add up to the multiplier, and each becomes one row of "How we reached this forecast"
    - its reasons, each linked to a fact or news finding and written in plain language (see "How results are explained to users")
    - a confidence level: low / medium / high
44. **Code applies the multipliers,** capped between 0.7 and 1.3 (±30%) *(tunable)*. The result is the **final expected goals** for each team.

The scout and the analyst are separate calls so that each output can be checked on its own. It also avoids depending on search and fixed-format output working together in one call, which differs between Gemini versions.

---

## J. Predictions (code)

45. **Scoreline table.** Use the Poisson distribution to work out the chance of each team scoring 0, 1, 2 … 10 goals, then the chance of every scoreline (0-0, 1-0, 2-1 …).
46. **Chance a prediction wins** = the sum of every scoreline where it wins. This covers home/draw/away, double chance, over/under goals, both teams to score, team goals, handicaps and correct score.
47. **Several predictions on the same match** are worked out together from the same table, never multiplied. They're linked: a Bayern win usually comes with goals.
48. **Fair odds** = 1 ÷ chance. If the bookmaker's odds are higher than the fair odds, the bet is good value. If they're lower, it's poor value.
49. **Verdict label** *(tunable)*. It is shown together with Gemini's confidence (step 43) and the value check (step 48).

| Chance | Label |
|---|---|
| 70% or more | Strong |
| 55–69% | Likely |
| 40–54% | Risky |
| Under 40% | Unlikely |

---

## K. The whole ticket (code)

50. **Ticket chance** = the chances of predictions on different matches multiplied together. Predictions on the same match are combined first, as in step 47.
51. **Show the user:**
    - the weakest prediction
    - the ticket's fair odds compared with the bookmaker's
    - how much the ticket's chance improves if each prediction is removed

---

## L. Updates and track record

52. **Re-run the analysis** when confirmed lineups arrive, when important news lands, and once a day.
53. **Alert users** who have that match on a ticket whenever its verdict changes.
54. **Save every analysis:** the fact sheet, news findings, Gemini's multipliers and reasons, final numbers, chances, and later the actual result.
55. **Check accuracy regularly.** Do our "60%" predictions win about 60% of the time? Are we closer to the results than the bookmaker? Adjust the *(tunable)* numbers based on the answers.

---

## How results are explained to users

Lead with what has happened before, in plain words. Expected goals come after, in brackets.

> "Bayern usually score about 3 at home (2.8 a game in their last 12). Without Kane and Díaz, expect about 2 today (2.10 expected goals)."

- **Team patterns (code):** goals scored and conceded per game over the last 5, 10, 12 and 15 games, at home and away. For example: "Bayern score about 3 a game at home (2.8 in their last 12 · 3.0 in their last 10)." The model itself still uses the 12-game window (step 10); the other windows are shown for context.
- **Streaks (code):** for example, "scored in 12 of their last 12 home games" or "conceded in 10 of their last 12 away games".
- **Player patterns (code):** goals and assists per game turned into simple rates, always with the count behind them. For example: "scores almost every game (11 in 12)", "sets up a goal every 2 games (6 assists in 12)", "scores every 3 games (4 in 12)".
- **With and without (code):** for example, "In the 3 games Kane missed, Bayern scored 1.6 a game."
- **Forecasts:** round expected goals to the nearest whole goal in the sentence ("about 2") and put the exact figure in brackets ("2.10 expected goals").
- **Forecast steps:** each row of "How we reached this forecast" is one plain sentence about the past, followed by its effect in brackets. The effects come from Gemini's per-factor breakdown (step 43).
- **Averages are not promises:** a player who scores about 1 a game still fails to score in roughly 4 games out of 10. Where it helps, show the chance as well, for example "scores in about 6 of 10 games like this".

**Who writes the sentences:** code builds every pattern sentence from templates, so the numbers are always correct. Gemini may join and reword them but must not add any number that isn't in the fact sheet. Code checks that every number in Gemini's text appears in the fact sheet, and rejects the text if one doesn't.

---

## Worked example (made-up numbers)

Bayern at home, with Kane, Olise and Díaz unavailable.

```
C. Baseline
   Bayern:    1.6 league avg home goals × 1.88 attack × 0.88 opponent defence = 2.6
   Opponent:  1.2 league avg away goals × 0.92 attack × 0.83 Bayern defence   = 0.9

E. Suggested adjustment
   Bayern ×0.83 (without Kane: 1.6 vs 2.9 goals/game, 3 games, pulled toward 1.0)

I. Gemini analyst
   "Kane, Olise and Díaz are out: 74% of Bayern's goals. Only 3 games without
    Kane, but the other two absences make it worse, not better."
   Bayern × 0.8 = 2.1      Opponent × 1.0 = 0.9
   Confidence: medium

J. Predictions
   Bayern win               65%    fair odds 1.54
   Draw                     20%
   Opponent win             15%
   Over 2.5 goals           58%
   Both teams score         52%
   Bayern win + over 2.5    44%    (not 65% × 58% = 38%; they're linked)

K. Ticket
   Bayern win 65% × Game 2 over 1.5 goals 80% × Game 3 home win 70% = 36%
   Weakest prediction: Bayern win
```

---

## Known limits (for later)

- **Strength of opponents isn't adjusted for.** A team whose last 12 games were mostly against weak sides will look stronger than it is. A later version can adjust each game for the opponent's quality.
- **Cup games against lower-league teams** can inflate goal numbers. Their lower weight (0.7) softens this but doesn't remove it.
- **Champions League and other cross-league games:** the teams' ratings come from different leagues, so they need a league-strength adjustment (for example using ClubElo). Not in v1.
- **xG instead of goals** in steps 13–14 would give steadier ratings. Later.
- **Posts on X (Twitter)** are often where team news breaks first, and they're poorly covered by web search. Later.
- **Corners and cards** need their own models. This method covers goal-based predictions only.
- **Draws:** the Poisson method slightly under-predicts low-scoring draws (0-0, 1-1). A standard correction (Dixon-Coles) can be added later.
- **These are chances, not certainties.** A 70% prediction still loses 3 times in 10.
