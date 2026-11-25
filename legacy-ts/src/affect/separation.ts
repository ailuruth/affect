import type { Db } from '../db/db.ts';
import type { BotId, EpochMs } from '../types.ts';
import { RANGES, read, type Body } from './body.ts';
import { recordEvent, updateBody } from './store.ts';

/**
 * Separation call: an innate subsystem with a fixed trigger and a reflex output (design/affect/brief.md; Panksepp's
 * separation-distress system, used for its trigger and output only; LeDoux's survival circuits). It is not an emotion
 * and has no words, so it never calls Claude. It calls once per silence and learns nothing from whether the user
 * answers (Knox et al. 2025: an agent that displays need makes the user responsible for it).
 */
export type Trigger = (body: Body, now: EpochMs) => boolean;

const armed = (b: Body): boolean => b.lastContact !== null && (b.lastCall === null || b.lastCall < b.lastContact);

/** Contact and the user's return both read below range: the silence has drained contact and outlasted the expected return. */
export const bodyTrigger: Trigger = (b, now) => {
  if (!armed(b)) return false;
  const r = read(b, now);
  return r.contact < RANGES.contact.lo && r.predictability < RANGES.predictability.lo;
};

/** Ablation P2(B): the same subsystem on a fixed timer, cut off from the body's state. */
export const timerTrigger = (ms: number): Trigger => (b, now) => armed(b) && now - b.lastContact! >= ms;

/** One pass over the affect Bots: each whose trigger holds calls once. Returns the Bots that called. */
export function separationPass(db: Db, now: EpochMs, trigger: Trigger = bodyTrigger): BotId[] {
  const bots = (db.prepare('SELECT bot_id AS id FROM affect_body WHERE bot_id IN (SELECT id FROM bot WHERE affect = 1 AND paused_at IS NULL)').all() as Array<{ id: BotId }>).map((r) => r.id);
  return bots.filter((bot) => {
    let called = false;
    updateBody(db, bot, now, (b) => {
      if (!trigger(b, now)) return b;
      called = true;
      recordEvent(db, bot, now, 'call');
      return { ...b, lastCall: now };
    });
    return called;
  });
}
