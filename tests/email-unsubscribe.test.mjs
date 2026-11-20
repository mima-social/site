// netlify/functions/email-unsubscribe.mjs (#41): the app's consent withdrawal.
import test, { beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";

const { default: handler, config } = await import("../netlify/functions/email-unsubscribe.mjs");

const URL_ = "https://www.mima.social/api/email-unsubscribe";
const EMAIL = "someone@example.com";
let calls, logged, realFetch, realError, realLog, loops;

beforeEach(() => {
  process.env.LOOPS_API_KEY = "test-key";
  calls = []; logged = [];
  loops = { found: [{ id: "c1", email: EMAIL }], findStatus: 200, updateStatus: 200 };
  realFetch = globalThis.fetch; realError = console.error; realLog = console.log;
  console.error = console.log = (...a) => logged.push(a.join(" "));
  globalThis.fetch = async (url, opt = {}) => {
    calls.push({ url: String(url), method: opt.method || "GET", body: opt.body ? JSON.parse(opt.body) : null });
    if (String(url).includes("/contacts/find")) return new Response(JSON.stringify(loops.found), { status: loops.findStatus });
    return new Response(JSON.stringify({ success: loops.updateStatus === 200 }), { status: loops.updateStatus });
  };
});
afterEach(() => { globalThis.fetch = realFetch; console.error = realError; console.log = realLog; });

const post = (body, headers = {}) => handler(new Request(URL_, {
  method: "POST", headers: { "Content-Type": "application/json", ...headers },
  body: typeof body === "string" ? body : JSON.stringify(body)
}));

test("unsubscribes a known contact with subscribed:false", async () => {
  const res = await post({ email: EMAIL });
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true });
  const update = calls.find((c) => c.url.endsWith("/contacts/update"));
  assert.equal(update.method, "PUT");
  assert.deepEqual(update.body, { email: EMAIL, subscribed: false });
});

test("never creates a contact: unknown address gets 200 and no update", async () => {
  loops.found = [];
  const res = await post({ email: "stranger@example.com" });
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true });
  assert.equal(calls.filter((c) => !c.url.includes("/contacts/find")).length, 0);
});

test("rejects bad input with 400 and calls nothing", async () => {
  for (const body of ["not json", { email: "nope" }, {}, { email: "a@b.c".padStart(300, "a") }]) {
    assert.equal((await post(body)).status, 400);
  }
  assert.equal(calls.length, 0);
});

test("rejects other methods with 405", async () => {
  const res = await handler(new Request(URL_, { method: "GET" }));
  assert.equal(res.status, 405);
});

test("returns 502 when Loops fails, so the app can retry", async () => {
  loops.updateStatus = 500;
  assert.equal((await post({ email: EMAIL })).status, 502);
  loops.updateStatus = 200; loops.findStatus = 500;
  assert.equal((await post({ email: EMAIL })).status, 502);
});

test("never logs the email address", async () => {
  loops.updateStatus = 500;
  await post({ email: EMAIL });
  loops.findStatus = 500;
  await post({ email: EMAIL });
  assert.ok(logged.length > 0, "failures should still be logged");
  for (const line of logged) assert.ok(!line.includes(EMAIL), `logged the email: ${line}`);
});

test("is rate limited per IP at /api/email-unsubscribe", () => {
  assert.equal(config.path, "/api/email-unsubscribe");
  assert.ok(config.rateLimit.windowLimit > 0);
  assert.ok(config.rateLimit.aggregateBy.includes("ip"));
});
