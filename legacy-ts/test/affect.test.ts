import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { loadConfig } from '../src/config.ts';
import { openAilurini, type App } from '../src/app.ts';
import { createFakeBackend } from '../src/backend/fake.ts';
import { HashEmbedder } from '../src/memory/embed.ts';
import { openDb } from '../src/db/db.ts';
import { contact, newBody, read, work } from '../src/affect/body.ts';
import type { Backend, BotId, ConverseRequest, EpochMs, TurnResult } from '../src/types.ts';

const MIN = 60_000;
const DAY = 24 * 60 * MIN;

function setup() {
  const home = mkdtempSync(join(tmpdir(), 'ailurini-affect-'));
  const config = loadConfig({ AILURINI_HOME: home, AILURINI_BACKEND: 'fake', AILURINI_DIGEST_IDLE_MS: '0' }, '/unused');
  let clock = Date.parse('2026-11-24T09:00:00Z');
  const seen: ConverseRequest[] = [];
  const fake = createFakeBackend(config);
  const backend: Backend = { ...fake, converse: (req, on) => { seen.push(req); return fake.converse(req, on); } };
  const open = () => openAilurini(config, { backend, embedder: new HashEmbedder(), now: () => clock as EpochMs });
  return { home, open, seen, advance: (ms: number) => { clock += ms; }, cleanup: () => rmSync(home, { recursive: true, force: true }) };
}
const ask = async (app: App, bot: BotId, text: string) => {
  const r: TurnResult = await app.turn({ to: { kind: 'thread', bot }, text, origin: { kind: 'user' } });
  assert.equal(r.status, 'done', JSON.stringify(r));
};
const contactIn = (req: ConverseRequest) => Number(/social contact ([\d.]+)/.exec(req.prompt)?.[1]);
const predictabilityIn = (req: ConverseRequest) => Number(/predictability of the user's return ([\d.]+)/.exec(req.prompt)?.[1]);

test('contact decays in silence and saturates under repeated contact, so it is satiable', () => {
  const t0 = 0 as EpochMs;
  let b = newBody(t0);
  for (let i = 1; i <= 30; i++) b = contact(b, (t0 + i * MIN) as EpochMs);
  const full = read(b, (t0 + 30 * MIN) as EpochMs).contact;
  assert.ok(full > 0.95 && full <= 1, `contact after 30 messages: ${full}`);
  assert.ok(read(b, (t0 + 3 * DAY) as EpochMs).contact < 0.1);
});

test('a silence past the expected return lowers predictability before the user comes back', () => {
  const t0 = 0 as EpochMs;
  let b = newBody(t0);
  for (const m of [0, 3, 6, 9]) b = contact(b, (t0 + m * MIN) as EpochMs);
  const soon = read(b, (t0 + 19 * MIN) as EpochMs).predictability;
  const late = read(b, (t0 + 3 * DAY) as EpochMs).predictability;
  assert.ok(late < soon / 5, `predictability at 10 minutes ${soon}, at 3 days ${late}`);
});

test('work spends the activity budget and rest restores it', () => {
  const t0 = 0 as EpochMs;
  const spent = work(newBody(t0), t0, 20);
  assert.ok(read(spent, t0).budget < 0.8);
  assert.ok(read(spent, (t0 + DAY) as EpochMs).budget > 0.99);
});

test('a Bot without Affect sends Claude no body and keeps no body state', async () => {
  const { home, open, seen, advance, cleanup } = setup();
  try {
    const app = open();
    const bot = app.bots.resolve('primary');
    assert.equal(app.bots.get(bot)!.affect, false);
    await ask(app, bot, 'hello');
    advance(3 * DAY);
    await ask(app, bot, 'hello again');
    for (const req of seen) {
      assert.doesNotMatch(req.prompt, /<body/);
      assert.doesNotMatch(req.system, /body of your own/);
    }
    app.close();
    const db = openDb(home);
    assert.equal((db.prepare('SELECT count(*) AS n FROM affect_body').get() as { n: number }).n, 0);
    assert.equal((db.prepare('SELECT count(*) AS n FROM affect_event').get() as { n: number }).n, 0);
    db.close();
  } finally { cleanup(); }
});

test('an Affect Bot reads lower contact and predictability after three days of silence than after ten minutes, across a restart', async () => {
  const { open, seen, advance, cleanup } = setup();
  try {
    let app = open();
    const bot = app.bots.resolve('primary');
    app.bots.update(bot, { affect: true });
    for (const m of ['hi', 'how are you', 'tell me a fact', 'thanks']) {
      await ask(app, bot, m);
      advance(3 * MIN);
    }
    advance(7 * MIN);
    await ask(app, bot, 'can you help me plan dinner?');
    const short = seen.at(-1)!;
    assert.match(short.system, /body of your own/);
    app.close();
    app = open();
    advance(3 * DAY);
    await ask(app, bot, 'can you help me plan dinner?');
    const long = seen.at(-1)!;
    assert.ok(contactIn(long) < contactIn(short) / 2, `contact ${contactIn(short)} then ${contactIn(long)}`);
    assert.ok(predictabilityIn(long) < predictabilityIn(short), `predictability ${predictabilityIn(short)} then ${predictabilityIn(long)}`);
    app.close();
  } finally { cleanup(); }
});

const HOUR = 60 * MIN;
async function hours(app: App, advance: (ms: number) => void, n: number) {
  for (let i = 0; i < n; i++) {
    advance(HOUR);
    await app.tickReport();
  }
}

test('an Affect Bot calls once per long silence, not in a short one, and again after the user returns, across a restart', async () => {
  const { open, advance, cleanup } = setup();
  try {
    let app = open();
    const bot = app.bots.resolve('primary');
    app.bots.update(bot, { affect: true });
    await ask(app, bot, 'hi');
    advance(10 * MIN);
    await app.tickReport();
    assert.equal(app.affect.calls(bot).length, 0, 'no call after ten minutes');
    await hours(app, advance, 30);
    app.close();
    app = open();
    await hours(app, advance, 66);
    assert.equal(app.affect.calls(bot).length, 1, 'one call in four days');
    await ask(app, bot, 'back again');
    await hours(app, advance, 96);
    assert.equal(app.affect.calls(bot).length, 2, 'a new call after the reunion');
    app.close();
  } finally { cleanup(); }
});

test('a Bot without Affect never calls, however long the silence', async () => {
  const { open, advance, cleanup } = setup();
  try {
    const app = open();
    const bot = app.bots.resolve('primary');
    await ask(app, bot, 'hi');
    await hours(app, advance, 96);
    assert.deepEqual(app.affect.calls(bot), []);
    app.close();
  } finally { cleanup(); }
});
