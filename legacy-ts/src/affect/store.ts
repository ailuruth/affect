import { tx, type Db } from '../db/db.ts';
import type { BotId, EpochMs } from '../types.ts';
import { newBody, type Body } from './body.ts';

export const affectOn = (db: Db, bot: BotId): boolean =>
  (db.prepare('SELECT affect FROM bot WHERE id = ?').get(bot) as { affect: number } | undefined)?.affect === 1;

export function setAffect(db: Db, bot: BotId, on: boolean): void {
  db.prepare('UPDATE bot SET affect = ? WHERE id = ?').run(on ? 1 : 0, bot);
}

export function bodyOf(db: Db, bot: BotId, now: EpochMs): Body {
  const row = db.prepare('SELECT state FROM affect_body WHERE bot_id = ?').get(bot) as { state: string } | undefined;
  if (!row) return newBody(now);
  const b = JSON.parse(row.state) as Omit<Body, 'lastCall'> & { lastCall?: EpochMs | null };
  return { ...b, lastCall: b.lastCall ?? null };
}

/** Read, change and write one Bot's body in one transaction, so two processes never lose each other's update. */
export function updateBody(db: Db, bot: BotId, now: EpochMs, fn: (b: Body) => Body): Body {
  return tx(db, () => {
    const next = fn(bodyOf(db, bot, now));
    db.prepare(`INSERT INTO affect_body (bot_id, state, updated_at) VALUES (?, ?, ?)
      ON CONFLICT (bot_id) DO UPDATE SET state = excluded.state, updated_at = excluded.updated_at`).run(bot, JSON.stringify(next), now);
    return next;
  });
}

export type AffectEventKind = 'contact' | 'call';

/** Append to the Bot's feature stream: when, and what kind. Never text, audio or video. */
export function recordEvent(db: Db, bot: BotId, at: EpochMs, kind: AffectEventKind): void {
  db.prepare('INSERT INTO affect_event (bot_id, at, kind) VALUES (?, ?, ?)').run(bot, at, kind);
}

export const eventsOf = (db: Db, bot: BotId, kind: AffectEventKind): EpochMs[] =>
  (db.prepare('SELECT at FROM affect_event WHERE bot_id = ? AND kind = ? ORDER BY at, id').all(bot, kind) as Array<{ at: EpochMs }>).map((r) => r.at);
