# Migration from Ailurini (2026-11-24)

The Affect work began inside Ailurini (`~/dev/ailurini`, branch `ailurini-app`, HEAD `2700624`) and was moved here, the engine's own project (brief.md, Principle 9). Ailurini is back to its state before Affect. This file lists what moved, what was removed from Ailurini, and what was checked.

## Files moved

55 files, moved with `mv`. A SHA-256 checksum of each was taken before the move and checked after it, and all 55 match.

| From (Ailurini) | To (here) |
|---|---|
| `design/affect/brief.md` | `brief.md` |
| `research/affect/` (index.md, predictions.md, questions.md, 40 notes, `runs/` with 5 run files) | `research/` |
| `src/affect/body.ts`, `separation.ts`, `store.ts` | `legacy-ts/src/affect/` |
| `test/affect.test.ts` | `legacy-ts/test/affect.test.ts` |
| `eval/affect/p1-separation.ts`, `p2-separation-call.ts` | `legacy-ts/eval/affect/` |

Paths inside moved files still name their Ailurini locations (for example `eval/affect/p1-separation.ts` or `design/affect/brief.md` in research/predictions.md). They were left as written because content was to stay unchanged. Use the table above to map them.

`legacy-ts/` is reference for porting only, not built or run. Its imports (`../../src/...`, `../src/app.ts`) point at Ailurini modules that do not exist here. Two of its parts conflict with the brief as it now stands:
- **The body section and the system-prompt paragraph** (`renderBody` in body.ts; `BODY` in Ailurini's prompt.ts, now removed) show Claude body values as numbers. Principle 4 now forbids this, and P1 found the shortcut has no effect. Do not port them.
- **The separation call** (separation.ts) acts as final behavior. Under "Learning the latent state" it becomes an input to $h$ and an initial bias on the policy, with a threshold that $h$ learns to modulate.

## Decision logs

- `DECISIONS.md`: D54 and D55, the only Affect entries, were copied verbatim under a new header and keep their numbers. They were checked line by line against the uncommitted hunk that had added them to Ailurini.
- `decisions.tsv`: the same header row, plus the 12 rows whose phase is `affect` (2026-11-24T12:21:11Z to 12:59:28Z), checked against the added hunk. Ailurini's committed log had no `affect` rows.

## Removed from Ailurini

Every uncommitted change to a tracked file in Ailurini was Affect work. At the start of the Affect session the tree was clean at `2700624`. HEAD has not moved since, and each hunk was read before removal. The 13 files were therefore restored to HEAD with `git restore`, and `git status` is now clean.

| File | Hunks removed |
|---|---|
| `src/agent/prompt.ts` | `BODY` paragraph; `affect` parameter of `systemPrompt` |
| `src/agent/turn.ts` | imports of `../affect/body.ts` and `../affect/store.ts`; reading the body, recording contact, passing `body` to `contextFor`, passing `affect` to `systemPrompt`, spending the activity budget after the turn |
| `src/app.ts` | affect imports; `BotRef` in the type import; `App.affect.calls`; the `separation` dependency of `openAilurini`; `affectPass` in `tickOnce` and in the daemon loop |
| `src/bots/bots.ts` | `affect` in `BotRow` and `toBot`; `affect` in `update` and its SQL |
| `src/cli/main.ts` | `bots affect` and `bots calls` commands |
| `src/cli/render.ts` | `affect` in `botRecord` |
| `src/db/db.ts` | `SCHEMA_VERSION` 16 back to 15; the `toV16` migration (bot.affect column, `affect_body`, `affect_event` and its index); `15: toV16` in `MIGRATIONS` |
| `src/db/schema.sql` | `affect` column on `bot`; `affect_body` and `affect_event` tables and index; schema_version 16 back to 15 |
| `src/memory/retrieve.ts` | `body` on `ContextRequest`; the `body` argument and its line in `render` |
| `src/types.ts` | `Bot.affect`; `'affect'` in `BotPatch`; `BotRecord.affect` |
| `src/web/server.ts` | `affect` in `BotPatchBody` |
| `DECISIONS.md` | D54, D55 |
| `decisions.tsv` | the 12 `affect` rows |

**The v16 migration existed only for Affect, so it was removed entirely.** It had never been committed and carried no other work.

The empty folders `design/affect/`, `research/affect/`, `src/affect/` and `eval/affect/` were removed. `test/`, `eval/` and `research/` keep their other files.

After the restore, Ailurini type-checks with only the two errors in `scripts/verify-p1.ts`, which predate Affect and are unrelated to it. All 355 tests pass. Before Affect there were 355; Affect had added 7.

## Left in place

- **In Ailurini's tracked files:** nothing. No hunk was unclear. A search for "affect" in src, test, eval, design and research finds only the English verb in `design/PLAN-grokbot.md`, which is a committed file.
- **Outside both repositories** (not touched, listed for cleanup):
  - **Temporary homes from the P1 runs:** `ailurini-p1-*` (5 directories under `/var/folders/nm/fhy2t5yj1wj_zk64gslcqpd00000gn/T/`). They hold scripted conversation copies and no user data. The P2 runs deleted their own homes.
  - **Claude Code session files from the P1 real-backend runs:** 2 project folders matching `~/.claude/projects/*ailurini-p1*`. One of them holds the contaminated shared session described in research/predictions.md.
  - **Finder metadata:** `.DS_Store` files that appeared in this project after the move. Their contents were not checked.

## The data/ check

The Affect code never migrated `ailurini/data/ailurini.db`.
- The file was last modified on Nov 16 at 19:48:10, eight days before any Affect code existed.
- There are no `-wal` or `-shm` files beside it.
- A copy, inspected with the original left alone, has `schema_version` 15, no `affect_*` tables and no `affect` column on `bot`.

Every Affect run used temporary homes or `:memory:` databases.

## Not done

- Nothing is committed here. `git init` only.
- The Affect loop (`/loop`) that was building in Ailurini was stopped before the move.
