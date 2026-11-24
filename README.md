# Offline-first sync: how do sync strategies compare?

This is a small study of what happens when phones edit data without signal and sync it later. The question I am working on:

How do last-write-wins, an operation log with idempotency keys, and a CRDT compare when phones go offline, send duplicates and have wrong clocks?

So far I have built and tested last-write-wins. The other two strategies come next. I am not claiming this question is new. The aim is a careful measurement that anyone can repeat.

## What is here

- `sync/lww.py` holds the last-write-wins store. Each record keeps one value and the time the phone gave it, and the later time wins.
- `sim/harness.py` simulates five phones editing offline, each with a clock that is wrong by a random amount, and then syncing to a server.
- `tests/test_lww.py` has the unit tests, including one that shows last-write-wins picking the wrong edit when a clock is slow.

Only the Python standard library is used.

## How to run it

Tests: `python -m unittest discover -s tests -t .`

Simulation: `python -m sim.harness`

## What counts as correct

For each record that at least two phones edited, the correct final value is the edit that really happened last, whatever any phone's clock said. A wrong winner is a record where the server ends up with a different value. Every run uses a fixed seed, so any result can be replayed.

## First result

Five phones, 20 records, 30 edits per phone spread over one hour, and all phones offline until the end. The table shows the median over 30 seeded runs.

| Max clock error | Wrong winners |
| --- | --- |
| 0 s | 0% |
| 1 s | 0% |
| 10 s | 0% |
| 60 s | 5% |
| 300 s | 10% |
| 900 s | 26% |
| 3600 s | 55% |

With accurate clocks, last-write-wins always keeps the right edit. As the clock error grows it keeps the wrong one more and more often, and nobody is told.

## Limits so far

- All phones sync once, at the end. Dropped requests, duplicate messages and syncs during the hour are not simulated yet.
- Edits are spread evenly over the hour. Real field data is clumpier.
- Each record holds one whole value, so two phones editing different fields of the same record is not modelled.
- This is a simulation. The offline web app has not been built.