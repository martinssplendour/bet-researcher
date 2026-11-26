# ADR 002: AI Provider (Google Gemini)

## Status

Accepted (26 Nov 2026)

## Context

The method needs an AI to search for team news, read bet slip screenshots, reason over a fact sheet, and show its thinking to the user.

## Decision

Use Google Gemini through the official `google-genai` Python SDK, in two separate calls per match:

1. **News scout:** Gemini with Google Search; returns findings with source links and dates.
2. **Analyst:** no search; reads the fact sheet and returns capped multipliers, a per-factor breakdown, reasons and confidence in a fixed JSON format, with thought summaries streamed to the user.

The model name is configuration (`GEMINI_MODEL`), not code.

## Consequences

- Better: one provider for search, vision and reasoning. Separate calls keep each output checkable.
- Worse: Google's search-grounding terms require showing "Google Search suggestions" in the UI.
- Know: Gemini never produces core numbers. Code caps every multiplier and rejects text with numbers missing from the fact sheet.

## Alternatives Considered

- Claude or OpenAI models: comparable reasoning. The project owner chose Gemini.
- One combined call: simpler, but search and fixed-format output don't combine reliably on every model version.
