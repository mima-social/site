// Emails the Mac download link to someone who tapped Download on a phone or
// tablet (#12) as a Loops transactional email. Signing up for updates happens
// in the browser through the Loops form, so double opt-in applies.
//
// Netlify environment variables:
//   LOOPS_API_KEY          Loops API key (Settings → API)
//   LOOPS_DOWNLOAD_EMAIL_ID  id of the "Your Mima download link" transactional email
const LOOPS = "https://app.loops.so/api/v1";
const DOWNLOAD_URL = "https://mima.social/download";
const ORIGINS = ["https://mima.social", "https://www.mima.social"];

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

export default async (req) => {
  if (req.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);
  const origin = req.headers.get("origin");
  if (origin && !ORIGINS.includes(origin) && !origin.endsWith(".netlify.app")) {
    return json({ ok: false, error: "Not allowed." }, 403);
  }

  let body;
  try { body = await req.json(); } catch { return json({ ok: false, error: "Bad request." }, 400); }
  // Honeypot: people never see this field, bots fill it. Pretend it worked.
  if (body.website) return json({ ok: true });

  const email = String(body.email || "").trim();
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: "Enter a valid email address." }, 400);
  }

  const headers = { Authorization: `Bearer ${process.env.LOOPS_API_KEY}`, "Content-Type": "application/json" };

  const sent = await fetch(`${LOOPS}/transactional`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      transactionalId: process.env.LOOPS_DOWNLOAD_EMAIL_ID,
      email,
      dataVariables: { downloadUrl: DOWNLOAD_URL }
    })
  });
  if (!sent.ok) {
    console.error("Loops transactional failed", sent.status, await sent.text());
    return json({ ok: false, error: "Couldn’t send the email. Please try again." }, 502);
  }

  return json({ ok: true });
};

export const config = {
  path: "/api/email-download",
  // Keeps the endpoint from being used to spam an inbox.
  rateLimit: { windowLimit: 5, windowSize: 60, aggregateBy: ["ip", "domain"] }
};
