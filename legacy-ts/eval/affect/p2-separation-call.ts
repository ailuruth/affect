/**
 * P2 (research/affect/predictions.md): the separation call, with the subsystem, without it (A), and on a fixed
 * 24-hour timer instead of the body (B). Fake backend; the call is a reflex below Claude, so no model is needed.
 *
 *   node eval/affect/p2-separation-call.ts <out.json>
 */
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { loadConfig } from '../../src/config.ts';
import { openAilurini, type App } from '../../src/app.ts';
import { HashEmbedder } from '../../src/memory/embed.ts';
import { bodyTrigger, timerTrigger, type Trigger } from '../../src/affect/separation.ts';
import type { BotId, EpochMs } from '../../src/types.ts';

const MIN = 60_000;
const HOUR = 60 * MIN;
const ARMS: Record<string, Trigger | null> = { subsystem: bodyTrigger, 'A-removed': null, 'B-timer': timerTrigger(24 * HOUR) };
const DOSES = { short: 1, long: 20 };

async function run(arm: string, dose: keyof typeof DOSES) {
  const home = mkdtempSync(join(tmpdir(), 'ailurini-p2-'));
  const config = loadConfig({ AILURINI_HOME: home, AILURINI_BACKEND: 'fake', AILURINI_EMBEDDER: 'hash', AILURINI_DIGEST_IDLE_MS: '0', AILURINI_NOTIFY: '0' }, '/unused');
  let clock = Date.parse('2026-11-02T18:00:00Z');
  const open = () => openAilurini(config, { embedder: new HashEmbedder(), now: () => clock as EpochMs, separation: ARMS[arm]! });
  let app: App = open();
  const bot: BotId = app.bots.resolve('primary');
  app.bots.update(bot, { affect: true });
  const say = async (text: string) => {
    const r = await app.turn({ to: { kind: 'thread', bot }, text, origin: { kind: 'user' } });
    if (r.status !== 'done') throw new Error(JSON.stringify(r));
  };
  const log: Array<{ phase: string; at: number }> = [];
  const phase = (name: string) => log.push({ phase: name, at: clock });
  const calls = () => app.affect.calls(bot);

  phase('meeting');
  for (let i = 0; i < DOSES[dose]; i++) {
    if (i) clock += MIN;
    await say(`message ${i + 1}`);
  }
  const meetingEnd = clock;
  const duringMeeting = calls().length;
  clock += 10 * MIN;
  await app.tickReport();
  const after10min = calls().length;
  for (let h = 1; h <= 96; h++) {
    clock = meetingEnd + h * HOUR;
    await app.tickReport();
    if (h === 30) {
      app.close();
      app = open();
    }
  }
  const silence1 = calls().filter((t) => t > meetingEnd).map((t) => (t - meetingEnd) / HOUR);
  phase('reunion');
  await say('back again');
  const reunion = clock;
  for (let h = 1; h <= 96; h++) {
    clock = reunion + h * HOUR;
    await app.tickReport();
  }
  const silence2 = calls().filter((t) => t > reunion).map((t) => (t - reunion) / HOUR);
  app.close();
  rmSync(home, { recursive: true, force: true });
  return { arm, dose, duringMeeting, after10min, silence1Hours: silence1, silence2Hours: silence2 };
}

const out = process.argv[2] ?? join(tmpdir(), 'p2.json');
const rows = [];
for (const arm of Object.keys(ARMS)) for (const dose of Object.keys(DOSES) as Array<keyof typeof DOSES>) rows.push(await run(arm, dose));
writeFileSync(out, JSON.stringify({ backend: 'fake', tickEveryHours: 1, rows }, null, 2));
for (const r of rows) console.log(`${r.arm.padEnd(10)} ${r.dose.padEnd(5)} meeting=${r.duringMeeting} 10min=${r.after10min} silence1=[${r.silence1Hours}] silence2=[${r.silence2Hours}]`);
console.log(`wrote ${out}`);
