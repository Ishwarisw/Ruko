# 🌷 BLOOM — Your Tiny Digital Garden

*Small steps. Beautiful growth.*

## Concept
BLOOM is a browser-based task manager that turns completed work into a living, procedurally generated garden. Effort, consistency and urgency are measured by an original Growth Algorithm and rendered as plants, flowers, weather and wildlife.

## Problem statement
Ordinary to-do lists only show what's left. They rarely make progress feel visible or rewarding, which makes consistency hard to sustain.

## Objective
Make progress tangible: every finished task grows something, weighted by how meaningful it was, so the user can *see* consistency over time.

## Features
- Create, edit, delete and complete tasks (name, category, importance, difficulty, deadline, estimated time incl. custom)
- Weighted Growth Algorithm (per-task dynamic points)
- Growth Score (0–100) with 5 garden stages
- Procedurally generated garden (plants, leaves, flowers, sun, moon, clouds, rain, stars, butterflies, fireflies, glowing "perfect day" flower)
- Category decorations (study books, coding pixels, creative petals, wellness leaves, career stars…)
- Today's Growth with configurable daily goal (default 30)
- Bloom streak with automatic reset after a missed day
- 8 achievements with unlock animation
- Category progress bars
- Rule-based "Today's Little Insight"
- Garden weather / mood
- Growth Journal (last 14 days)
- Settings → Reset Garden with confirmation
- About section, responsive layout, reduced-motion support

## Technology
HTML5 · CSS3 · Vanilla JavaScript · localStorage. No frameworks, backend or external APIs (only optional Google Fonts).

## System workflow
```
USER INPUT
↓
TASK DATA
↓
GROWTH CALCULATION ENGINE
↓
PROGRESS ANALYSIS
↓
GARDEN STATE
↓
VISUAL OUTPUT
```

## Growth algorithm
Each factor is normalised to 0–100:

| Factor | Weight | Normalisation |
|---|---|---|
| Importance | 30% | Low 33 · Medium 66 · High 100 |
| Difficulty | 25% | Easy 33 · Medium 66 · Hard 100 |
| Time investment | 15% | min(100, minutes / 120 × 100) |
| Deadline urgency | 20% | overdue/today 100 · tomorrow 80 · ≤3d 60 · ≤7d 40 · later 20 · none 10 |
| Consistency | 10% | min(100, 10 + streak × 15) |

`Task Growth Value = I×0.30 + D×0.25 + T×0.15 + U×0.20 + C×0.10`

Points awarded = `round(value / 4)` (1–25). Growth Score = `min(100, totalPoints / 2.5)`.

## Garden evolution system
| Score | Stage |
|---|---|
| 0–20 | 🌱 Seed |
| 21–40 | 🌿 Sprout |
| 41–60 | 🌷 Growing |
| 61–80 | 🌸 Flowering |
| 81–100 | 🌺 Blooming |

Plant count = 1 + score/9, heights scale with score, flower probability rises above 40, butterflies above 70, fireflies above 80. A glowing flower appears when every task for the day is complete. Weather: streak ≥ 7 → Magical Evening, progress ≥ 70% → Sunny, some progress → Soft Clouds, none → Gentle Rain.

## Achievement system
First Seed, First Bloom, Garden Keeper, Consistent Soul, Full Bloom, Little Steps, Code Bloom, Creative Bloom — each evaluated after every state change.

## Data storage
All data is stored as one JSON object under the `bloom.v1` key in localStorage: tasks, totals, daily history, streak, best streak, achievements, preferences.

## Testing
Manually verified: add/edit/delete/complete tasks, point calculation (`BLOOM.factors(task)` in console), stage changes, streak, achievements, categories, insight, weather, journal, persistence after refresh, reset and mobile layouts.

## Limitations
- Data lives in one browser; clearing site data erases it.
- No sync across devices; no recurring tasks.

## Future improvements
Export/import JSON, recurring tasks, seasonal garden themes, weekly reports.

## How to run locally
Open `index.html` in any modern browser — no install or server needed.
