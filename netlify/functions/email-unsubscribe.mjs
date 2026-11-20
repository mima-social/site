// Unsubscribes an address from Mima's email updates in Loops when someone
// withdraws consent in the app (Settings → Privacy, mima-social/desktop#2318).
// The app can't hold the Loops API key, so it calls this instead (#41).
//
// Contract: POST /api/email-unsubscribe, JSON {"email": "..."}.
//   200 {ok:true}  done, or the address isn't in Loops (we don't say which)
//   400            bad JSON or invalid email
//   405            not a POST
//   502            Loops failed; the app should retry
//
// Anyone who knows an address could unsubscribe it; the owner accepted that
// (the person can resubscribe) over a per-install token. Limits instead:
// per-IP rate limit below, a JSON body (so a page on another site can't send
// it without a CORS preflight, which this function doesn't answer), and a 200
// that doesn't reveal whether an address is on the list.
//
// Never logs the email or puts it in our URL.
//
// Netlify environment variables:
//   LOOPS_API_KEY  Loops API key (Settings → API)
const LOOPS = "https://app.loops.so/api/v1";

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

export default async (req) => {
  if (req.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);

  let body;
  try { body = await req.json(); } catch { return json({ ok: false, error: "Bad request." }, 400); }

  const email = String(body?.email || "").trim();
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: "Enter a valid email address." }, 400);
  }

  const headers = { Authorization: `Bearer ${process.env.LOOPS_API_KEY}`, "Content-Type": "application/json" };

  // Loops' update endpoint creates a contact when none matches, which would
  // add strangers' addresses to the audience. Look it up first.
  const found = await fetch(`${LOOPS}/contacts/find?email=${encodeURIComponent(email)}`, { headers });
  if (!found.ok) {
    console.error("Loops find failed", found.status);
    return json({ ok: false, error: "Couldn’t unsubscribe. Please try again." }, 502);
  }
  const contacts = await found.json().catch(() => []);
  if (!Array.isArray(contacts) || contacts.length === 0) return json({ ok: true });

  // subscribed:false stops all campaign and workflow email. Transactional
  // email (e.g. the download link) still works.
  const updated = await fetch(`${LOOPS}/contacts/update`, {
    method: "PUT",
    headers,
    body: JSON.stringify({ email, subscribed: false })
  });
  if (!updated.ok) {
    console.error("Loops unsubscribe failed", updated.status);
    return json({ ok: false, error: "Couldn’t unsubscribe. Please try again." }, 502);
  }
  return json({ ok: true });
};

export const config = {
  path: "/api/email-unsubscribe",
  // Slows anyone trying to unsubscribe a list of addresses they know.
  rateLimit: { windowLimit: 5, windowSize: 60, aggregateBy: ["ip", "domain"] }
};
