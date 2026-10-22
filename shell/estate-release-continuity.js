/* Estate release continuity v1: disclose browser staleness without destructive reload.
 * Current release is proved by the origin's explicit no-store release endpoint.
 * No access to page authoring state or media, no service worker registration,
 * no history/cache deletion and no automatic page refresh.
 */
(() => {
  "use strict";
  const localRelease = document.documentElement.getAttribute("data-estate-release");
  if (!/^[a-f0-9]{64}$/.test(localRelease || "")) return;
  const root = document.documentElement;
  let inFlight = null;
  let alertBox = null;
  let lastCheck = 0;
  const setState = value => { root.setAttribute("data-estate-freshness", value); };
  function notice(stale) {
    if (!stale) { if (alertBox) { alertBox.remove(); alertBox = null; } return; }
    if (alertBox) return;
    alertBox = document.createElement("aside");
    alertBox.setAttribute("role", "status");
    alertBox.setAttribute("aria-live", "polite");
    alertBox.setAttribute("data-estate-release-notice", "");
    alertBox.style.cssText =
      "position:fixed;right:12px;bottom:12px;z-index:2147483600;max-width:min(92vw,370px);" +
      "padding:12px 14px;background:#243129;color:#f6f4eb;border:1px solid #94ab9a;" +
      "border-radius:8px;box-shadow:0 2px 15px #0006;font:13px/1.5 system-ui,sans-serif";
    const text = document.createElement("span");
    text.textContent = "A newer estate release is available. Your current reading or work has not been interrupted.";
    const button = document.createElement("button");
    button.textContent = "Open current edition";
    button.style.cssText =
      "display:block;margin-top:9px;padding:7px 11px;border:1px solid #b7cebc;" +
      "border-radius:5px;background:#eff3ea;color:#17251d;font:inherit;cursor:pointer";
    button.addEventListener("click", () => {
      // A new navigation, not location.reload(). Back remains available.
      const target = new URL(location.href);
      target.searchParams.set("estate_release", root.getAttribute("data-estate-current-release") || "");
      location.assign(target.href);
    });
    alertBox.append(text, button);
    document.body.appendChild(alertBox);
  }
  async function check(force = false) {
    if (inFlight) return inFlight;
    if (!force && Date.now() - lastCheck < 700) return;
    lastCheck = Date.now();
    setState("checking");
    inFlight = (async () => {
      try {
        if (navigator.serviceWorker?.controller) throw Error("unexpected controlling service worker");
        const request = "/__estate/current.json?probe=" + encodeURIComponent(
          String(Date.now()) + "-" + Math.random().toString(36).slice(2));
        const r = await fetch(request, {
          cache: "no-store",
          redirect: "error",
          headers: {"Cache-Control": "no-store", "Accept": "application/json"}
        });
        if (!r.ok || r.headers.get("X-Estate-Authority") !== "source-locked") throw Error("unverified endpoint");
        if (!/no-store/i.test(r.headers.get("Cache-Control") || "")) throw Error("cacheable authority");
        const body = await r.json();
        if (body.schema !== "fountain.estate.release-continuity.v1" ||
            !/^[a-f0-9]{64}$/.test(body.releaseId || "") ||
            body.publicPublished !== false) throw Error("unverified release manifest");
        root.setAttribute("data-estate-current-release", body.releaseId);
        const old = body.releaseId !== localRelease;
        setState(old ? "stale" : "fresh");
        notice(old);
        return old ? "stale" : "fresh";
      } catch (_) {
        // Unknown is not freshness; don't clear a previously detected stale notice.
        if (root.getAttribute("data-estate-freshness") !== "stale") setState("unverified");
        return "unverified";
      } finally { inFlight = null; }
    })();
    return inFlight;
  }
  root.setAttribute("data-estate-freshness", "checking");
  const start = () => { void check(true); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, {once:true});
  else start();
  window.addEventListener("pageshow", () => { void check(true); });
  window.addEventListener("focus", () => { void check(true); });
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) void check(true);
  });
  // Foreground probe: detects deployments without disrupting the active reading or audio.
  setInterval(() => { if (!document.hidden) void check(true); }, 60000);
  // No automatic reload, no private browsing-state mutation.
  window.EstateReleaseContinuity = Object.freeze({check: () => check(true), releaseId: localRelease});
})();
