import type { EpochMs } from '../types.ts';

/**
 * Innate body variables an affect Bot regulates (design/affect/brief.md, "Body variables").
 * Theory: Damasio's homeostatic basis of feeling and Barrett's body budget; the return-time estimate is predictive
 * processing, so a silence longer than expected is itself prediction error. None of these is an emotion: they are
 * regulated quantities, and what they amount to is left to the latent state and to Claude.
 */
export type Body = {
  at: EpochMs;
  contact: number;
  budget: number;
  predictability: number;
  gapMean: number;
  gapVar: number;
  lastContact: EpochMs | null;
  /** When the separation-call subsystem last called (src/affect/separation.ts); it re-arms when the user writes. */
  lastCall: EpochMs | null;
};

export type Range = { lo: number; hi: number };
export type Reading = { contact: number; predictability: number; budget: number };

const HOUR = 3_600_000;
const MINUTE = 60_000;
export const RANGES: Readonly<Record<keyof Reading, Range>> = {
  contact: { lo: 0.35, hi: 0.85 },
  predictability: { lo: 0.4, hi: 1 },
  budget: { lo: 0.3, hi: 1 },
};
const CONTACT_TAU = 24 * HOUR;
const CONTACT_GAIN = 0.35;
const BUDGET_TAU = 6 * HOUR;
const TURN_COST = 0.03;
const TOOL_COST = 0.01;
const RATE = 0.2;
const PREDICT_RATE = 0.3;
const MIN_SD = 0.5;

const clamp = (x: number) => Math.min(1, Math.max(0, x));
const logGap = (ms: number) => Math.log(Math.max(ms, 1000) / MINUTE);
const surprise = (body: Body, gapMs: number) => (logGap(gapMs) - body.gapMean) / Math.max(MIN_SD, Math.sqrt(body.gapVar));

export function newBody(at: EpochMs): Body {
  return { at, contact: 0.5, budget: 1, predictability: 0.5, gapMean: Math.log(240), gapVar: 4, lastContact: null, lastCall: null };
}

/** Drift with the passage of time: contact decays toward 0, the activity budget recovers toward 1. */
export function advance(body: Body, now: EpochMs): Body {
  const dt = Math.max(0, now - body.at);
  return {
    ...body,
    at: Math.max(now, body.at) as EpochMs,
    contact: body.contact * Math.exp(-dt / CONTACT_TAU),
    budget: 1 - (1 - body.budget) * Math.exp(-dt / BUDGET_TAU),
  };
}

/** The user wrote. Contact saturates toward 1, so it is satiable; the return time updates the gap estimate. */
export function contact(body: Body, now: EpochMs): Body {
  const b = advance(body, now);
  if (b.lastContact === null) return { ...b, contact: b.contact + CONTACT_GAIN * (1 - b.contact), lastContact: now };
  const gap = now - b.lastContact;
  const hit = Math.exp(-(surprise(b, gap) ** 2) / 2);
  const x = logGap(gap);
  const d = x - b.gapMean;
  return {
    ...b,
    contact: b.contact + CONTACT_GAIN * (1 - b.contact),
    predictability: b.predictability + PREDICT_RATE * (hit - b.predictability),
    gapMean: b.gapMean + RATE * d,
    gapVar: (1 - RATE) * (b.gapVar + RATE * d * d),
    lastContact: now,
  };
}

/** The Bot did work: a turn, plus each tool call. */
export function work(body: Body, now: EpochMs, toolCalls: number): Body {
  const b = advance(body, now);
  return { ...b, budget: clamp(b.budget - TURN_COST - TOOL_COST * toolCalls) };
}

/** What the body reads as now. A silence past the expected return lowers predictability before the user returns. */
export function read(body: Body, now: EpochMs): Reading {
  const b = advance(body, now);
  const overdue = b.lastContact === null ? 0 : Math.max(0, surprise(b, now - b.lastContact));
  return { contact: b.contact, predictability: b.predictability * Math.exp(-(overdue ** 2) / 2), budget: b.budget };
}

const LINES: Readonly<Record<keyof Reading, string>> = {
  contact: 'social contact',
  predictability: "predictability of the user's return",
  budget: 'activity budget',
};
const where = (x: number, r: Range) => (x < r.lo ? 'below' : x > r.hi ? 'above' : 'within');

export function renderBody(r: Reading): string {
  const keys = Object.keys(LINES) as Array<keyof Reading>;
  return [
    '<body note="Your own body variables, not the user\'s. Each is 0 to 1, with the range it is regulated to.">',
    ...keys.map((k) => `${LINES[k]} ${r[k].toFixed(2)} (range ${RANGES[k].lo.toFixed(2)}-${RANGES[k].hi.toFixed(2)}; ${where(r[k], RANGES[k])})`),
    '</body>',
  ].join('\n');
}
