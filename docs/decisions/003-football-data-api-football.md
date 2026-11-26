# ADR 003: Football Data Source (API-Football)

## Status

Accepted (26 Nov 2026)

## Context

The method needs fixtures, results, standings, lineups, player stats, injuries, head-to-head records and odds, for many leagues, from one affordable source.

## Decision

Use API-Football (api-sports.io). Start on the free plan (100 requests a day) and move to a paid plan when needed.

## Consequences

- Better: one key covers every data need in the method. All endpoints are on every plan.
- Worse: the free plan's daily limit is tight, and it may restrict which seasons can be queried.
- Know: finished matches never change, so they are fetched once and stored. All calls go through one client in `integrations/` that handles rate limits, retries and response validation.

## Alternatives Considered

- Sportmonks: richer (xG add-on) but more expensive.
- football-data.org: free, but lacks injuries and lineups.
- Scraping (SofaScore, FotMob, Transfermarkt): breaks their terms; not acceptable for a public product.
