// KI-Grenzgänger – statische Seite (GitHub Pages).
// Berater, Steckbriefe, Grundlagen und Marktanalyse funktionieren ohne JavaScript;
// das Skript ergänzt Schublade, Filter im Verzeichnis und Suchvorschläge.
document.documentElement.classList.add("js");

const ROOT = document.documentElement.dataset.root || "";
// Suche: Treffer im Produktnamen zählen am meisten, dann Anbieter, dann Kategorie, zuletzt der Rest
// (z.B. Modellliste). So stehen bei «claude» die Claude-Produkte vor Plattformen, die Claude nur anbieten.
const relevanz = (t, woerter) => {
  let p = 0;
  for (const w of woerter) {
    if (!t.such.includes(w) && !t.n.includes(w)) return -1;
    const wort = new RegExp("(^|[^a-z0-9äöüé])" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    p += t.n.startsWith(w) ? 100 : wort.test(t.n) ? 80 : t.n.includes(w) ? 60
      : t.a.includes(w) ? 50 : t.k.includes(w) ? 20 : 5;
  }
  return p;
};
const suchwoerter = (q) => q.trim().toLowerCase().split(/\s+/).filter(Boolean);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

document.addEventListener("DOMContentLoaded", () => {
  initSchublade();
  initDetails(document);
  initVerzeichnis();
  initSuche();
  initZurueck();
  initMenu();
});

/* ---------- Menü auf dem Handy ---------- */
function initMenu() {
  const btn = document.querySelector("[data-menu]");
  const nav = document.getElementById("hauptnav");
  if (!btn || !nav) return;
  const setzen = (auf) => {
    nav.classList.toggle("offen", auf);
    btn.setAttribute("aria-expanded", String(auf));
  };
  btn.addEventListener("click", (e) => { e.stopPropagation(); setzen(!nav.classList.contains("offen")); });
  document.addEventListener("click", (e) => { if (!nav.contains(e.target)) setzen(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("offen")) { setzen(false); btn.focus(); }
  });
}

/* ---------- Alle Details auf-/zuklappen ---------- */
function initDetails(root) {
  const btn = root.querySelector("[data-toggle-all]");
  if (!btn) return;
  const alle = [...root.querySelectorAll("details.acc")];
  btn.addEventListener("click", () => {
    const auf = !alle.every((d) => d.open);
    alle.forEach((d) => (d.open = auf));
    btn.textContent = auf ? "Alle zuklappen" : "Alle aufklappen";
  });
}

/* ---------- Steckbrief-Schublade ---------- */
function initSchublade() {
  const drawer = document.getElementById("drawer");
  if (!drawer) return;
  const scrim = document.getElementById("scrim");
  const body = document.getElementById("drawer-body");
  const link = document.getElementById("drawer-link");
  let zuletzt = null, aktiveZeile = null;

  const schliessen = () => {
    if (!drawer.classList.contains("on")) return;
    drawer.classList.remove("on");
    scrim.classList.remove("on");
    drawer.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    setTimeout(() => { scrim.hidden = true; }, 200);
    aktiveZeile && aktiveZeile.classList.remove("aktiv");
    zuletzt && zuletzt.focus();
  };

  const oeffnen = async (href, ausloeser) => {
    zuletzt = ausloeser;
    aktiveZeile && aktiveZeile.classList.remove("aktiv");
    aktiveZeile = ausloeser.classList.contains("vz-row") ? ausloeser : null;
    aktiveZeile && aktiveZeile.classList.add("aktiv");
    const seite = new URL(href, location.href);
    link.href = seite.href;
    body.innerHTML = '<p class="dr-laden">Steckbrief wird geladen …</p>';
    scrim.hidden = false;
    requestAnimationFrame(() => { scrim.classList.add("on"); drawer.classList.add("on"); });
    drawer.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    try {
      // Zu jeder Steckbrief-Seite gibt es ein Fragment ohne Kopf und Fuss
      const r = await fetch(new URL("steckbrief.html", seite));
      if (!r.ok) throw new Error(r.status);
      body.innerHTML = await r.text();
      body.scrollTop = 0;
      initDetails(body);
      drawer.querySelector("[data-close]").focus();
    } catch (_) {
      location.href = seite.href; // Fallback: normale Seite
    }
  };

  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-drawer]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    if (window.matchMedia("(max-width: 700px)").matches) return; // Handy: normale Seite
    e.preventDefault();
    oeffnen(a.getAttribute("href"), a);
  });
  drawer.querySelector("[data-close]").addEventListener("click", schliessen);
  scrim.addEventListener("click", schliessen);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") schliessen(); });
}

/* ---------- Verzeichnis: Filter, Zähler, Sortierung im Browser ---------- */
function initVerzeichnis() {
  const form = document.getElementById("filter");
  const tbl = document.getElementById("vz-tbl");
  const cfgEl = document.getElementById("vz-config");
  if (!form || !tbl || !cfgEl) return;
  const cfg = JSON.parse(cfgEl.textContent);
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => [...document.querySelectorAll(sel)];

  const tools = [...tbl.querySelectorAll(".vz-row")].map((el) => {
    const d = el.dataset;
    return {
      el, dh: d.dh, pd: d.pd, bg: d.bg, gruppe: d.gruppe, cloud: d.cloud, vischer: d.vischer === "1",
      rdh: +d.rDh, rpd: +d.rPd, rbg: +d.rBg, rgr: +d.rGr, pp: +d.pp, name: d.name, such: d.such, n: d.name, a: d.an, k: d.kt,
      funk: new Set(d.funk.split(" ").filter(Boolean)),
      l: { ch: d.lCh, eu: d.lEu, gl: d.lGl }, lCell: el.querySelector("[data-lst]"),
    };
  });
  const L = cfg.leistung;
  const lstIcon = (tbl.querySelector(".lst svg") || { outerHTML: "" }).outerHTML;
  // Leistung passend zum Datenort-Filter: nur Schweiz → CH-Variante, Schweiz/Europa → EU-Variante
  const variante = (s) => {
    if (!s.orte.length) return "gl";
    const keys = s.orte.flatMap((o) => cfg.orte[o]);
    if (keys.every((k) => k === "ch")) return "ch";
    if (keys.every((k) => k === "ch" || k === "eu")) return "eu";
    return "gl";
  };
  const total = tools.length;
  const FUNK = $$('input[name="funk"]').map((i) => i.value);
  const ARTEN = $$('input[name="art"]').map((i) => i.value);
  const GUT = new Set(["gruen", "gelb"]);
  const SORT_TEXT = { "": "Eignung (beste zuerst)", name: "Name", ort: "Datenort", leistung: "Leistung", pd: "Personendaten", bg: "Berufsgeheimnis" };

  const leer = () => ({ orte: [], sens: "", art: "", funk: [], cloud: false, vischer: false, q: "", sort: "" });

  const ausParams = (p) => ({
    orte: p.getAll("ort").filter((o) => o in cfg.orte),
    sens: ["pd", "bg"].includes(p.get("sens")) ? p.get("sens") : "",
    art: ARTEN.includes(p.get("art")) ? p.get("art") || "" : "",
    funk: p.getAll("funk").filter((f) => FUNK.includes(f)),
    cloud: p.get("cloud") === "1",
    vischer: p.get("vischer") === "1",
    q: p.get("q") || "",
    sort: p.get("sort") in SORT_TEXT ? p.get("sort") : "",
  });

  const passt = (t, s) => {
    if (s.orte.length && !s.orte.some((o) => cfg.orte[o].includes(t.dh))) return false;
    if (s.sens === "pd" && !GUT.has(t.pd)) return false;
    if (s.sens === "bg" && !GUT.has(t.bg)) return false;
    if (s.art && t.gruppe !== s.art) return false;
    if (s.funk.some((f) => !t.funk.has(f))) return false;
    if (s.cloud && t.cloud !== "nein") return false;
    if (s.vischer && !t.vischer) return false;
    const woerter = suchwoerter(s.q);
    if (woerter.length && relevanz(t, woerter) < 0) return false;
    return true;
  };
  const anzahl = (s, aenderung) => { const x = { ...s, ...aenderung }; return tools.filter((t) => passt(t, x)).length; };

  const vergleich = (a, b) => { for (let i = 0; i < a.length; i++) { if (a[i] < b[i]) return -1; if (a[i] > b[i]) return 1; } return 0; };
  const sortieren = (liste, s) => {
    const rel = s.sens === "bg" ? "rbg" : "rpd";
    liste.sort((a, b) => vergleich([a[rel], a.rdh, a.rgr, a.pp, a.name], [b[rel], b.rdh, b.rgr, b.pp, b.name]));
    const v = variante(s);
    const k = { name: (t) => [t.name], ort: (t) => [t.rdh, t.rpd], pd: (t) => [t.rpd, t.rdh], bg: (t) => [t.rbg, t.rdh],
      leistung: (t) => [L[t.l[v]].rang, t.rpd, t.rdh] }[s.sort];
    if (k) liste.sort((a, b) => vergleich(k(a), k(b)));
    else if (s.q.trim()) {
      const woerter = suchwoerter(s.q);
      liste.sort((a, b) => relevanz(b, woerter) - relevanz(a, woerter));
    }
    return liste;
  };

  const formular = (s) => {
    form.q.value = s.q;
    $$('input[name="sens"]').forEach((i) => (i.checked = i.value === s.sens));
    $$('input[name="art"]').forEach((i) => (i.checked = i.value === s.art));
    $$('input[name="ort"]').forEach((i) => (i.checked = s.orte.includes(i.value)));
    $$('input[name="funk"]').forEach((i) => (i.checked = s.funk.includes(i.value)));
    form.cloud.checked = s.cloud;
    form.vischer.checked = s.vischer;
    form.sort.value = s.sort;
  };
  const ausFormular = () => ausParams(new URLSearchParams(new FormData(form)));

  const query = (s) => {
    const p = new URLSearchParams();
    s.orte.forEach((o) => p.append("ort", o));
    if (s.sens) p.set("sens", s.sens);
    if (s.art) p.set("art", s.art);
    s.funk.forEach((f) => p.append("funk", f));
    if (s.cloud) p.set("cloud", "1");
    if (s.vischer) p.set("vischer", "1");
    if (s.q) p.set("q", s.q);
    if (s.sort) p.set("sort", s.sort);
    const str = p.toString();
    return str ? "?" + str : location.pathname;
  };

  let s = ausParams(new URLSearchParams(location.search));

  const zeigen = () => {
    const liste = sortieren(tools.filter((t) => passt(t, s)), s);
    const sichtbar = new Set(liste);
    tools.forEach((t) => (t.el.hidden = !sichtbar.has(t)));
    liste.forEach((t) => tbl.appendChild(t.el));
    const v = variante(s);
    liste.forEach((t) => {
      const key = t.l[v];
      if (t.lCell.dataset.k === key) return;
      t.lCell.dataset.k = key;
      t.lCell.innerHTML = key === "na" || key === "keine" ? ""
        : `<span class="lst lst-${key}" title="Leistung: ${esc(L[key].label)}">${lstIcon}${esc(L[key].kurz)}</span>`;
    });
    tbl.hidden = !liste.length;
    $("[data-leer]").hidden = !!liste.length;

    // Zähler neben den Optionen
    const setzeZahl = (key, n, aktiv) => {
      const em = document.querySelector(`[data-n="${key}"]`);
      if (!em) return;
      em.textContent = n;
      em.closest("label").classList.toggle("leer", !n && !aktiv);
    };
    ["", "pd", "bg"].forEach((w) => setzeZahl("sens:" + w, anzahl(s, { sens: w }), true));
    ARTEN.forEach((w) => setzeZahl("art:" + w, anzahl(s, { art: w }), s.art === w));
    FUNK.forEach((f) => {
      const an = s.funk.includes(f);
      setzeZahl("funk:" + f, an ? liste.length : anzahl(s, { funk: [...s.funk, f] }), an);
    });

    // Datenort-Leiste
    $("#vz-bar").classList.toggle("sel", s.orte.length > 0);
    $$("#vz-bar a").forEach((a) => a.setAttribute("aria-pressed", String(s.orte.includes(a.dataset.ort))));

    // Kopfzeile, Hinweise, Sortierung
    const aktiv = !!(s.orte.length || s.sens || s.art || s.funk.length || s.cloud || s.vischer || s.q);
    $("[data-aktiv]").hidden = !aktiv;
    $$("[data-reset]").forEach((a) => (a.hidden = !aktiv));
    $("[data-anzahl]").textContent = `${liste.length} ${liste.length === 1 ? "Tool" : "Tools"}`;
    $("[data-anzahl-info]").textContent = aktiv ? `von ${total}` : "– alle Einträge";
    $("[data-sort-info]").textContent = "Sortiert nach " + (!s.sort && s.q.trim() ? "Relevanz" : SORT_TEXT[s.sort]);
    $("[data-sort-select]").value = s.sort;
    $$("[data-sort]").forEach((a) => {
      const an = a.dataset.sort === s.sort;
      a.toggleAttribute("data-on", an);
      a.textContent = a.textContent.replace(/ ↓$/, "") + (an ? " ↓" : "");
    });
    $("[data-bg-hinweis]").hidden = s.sens !== "bg";
    $("[data-sens-hilfe]").hidden = !s.sens;
    history.replaceState(null, "", query(s));
  };

  formular(s);
  zeigen();

  form.addEventListener("change", (e) => { if (e.target.type !== "search") { s = ausFormular(); zeigen(); } });
  let timer;
  form.q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(() => { s = ausFormular(); zeigen(); }, 120); });
  form.addEventListener("submit", (e) => { e.preventDefault(); s = ausFormular(); zeigen(); });
  $$("#vz-bar a").forEach((a) => a.addEventListener("click", (e) => {
    e.preventDefault();
    const o = a.dataset.ort;
    s = { ...s, orte: s.orte.includes(o) ? s.orte.filter((x) => x !== o) : [...s.orte, o] };
    formular(s); zeigen();
  }));
  $$("[data-sort]").forEach((a) => a.addEventListener("click", (e) => {
    e.preventDefault();
    s = { ...s, sort: s.sort === a.dataset.sort ? "" : a.dataset.sort };
    formular(s); zeigen();
  }));
  $("[data-sort-select]").addEventListener("change", (e) => { s = { ...s, sort: e.target.value }; formular(s); zeigen(); });
  $$("[data-reset], [data-leer] a").forEach((a) => a.addEventListener("click", (e) => {
    e.preventDefault();
    s = leer(); formular(s); zeigen();
  }));

  if (s.q) { form.q.focus(); form.q.setSelectionRange(s.q.length, s.q.length); }
  // Auf dem Handy Filter standardmässig einklappen
  const det = form.querySelector("details");
  if (det && window.matchMedia("(max-width: 1000px)").matches) det.open = false;
}

/* ---------- Berater: Vorschläge im Suchfeld ---------- */
function initSuche() {
  const eingabe = document.getElementById("vb-q");
  const sugg = document.getElementById("vb-sugg");
  if (!eingabe || !sugg) return;
  let tools = null, laden = null, treffer = [], sel = -1;
  const holen = () => laden || (laden = fetch(ROOT + "suche.json").then((r) => r.json()).then((d) => (tools = d)).catch(() => (tools = [])));

  const zeigen = async () => {
    await holen();
    const q = eingabe.value.trim().toLowerCase();
    const woerter = suchwoerter(q);
    treffer = woerter.length ? tools.map((t) => [relevanz(t, woerter), t]).filter(([p]) => p >= 0)
      .sort((x, y) => y[0] - x[0] || x[1].r - y[1].r || x[1].n.localeCompare(y[1].n)).slice(0, 8).map(([, t]) => t) : [];
    sel = -1;
    sugg.hidden = !treffer.length;
    sugg.innerHTML = treffer.map((t, i) =>
      `<a href="${ROOT}tool/${encodeURIComponent(t.id)}/" data-drawer data-i="${i}"><span>${esc(t.name)} <span class="muted klein">· ${esc(t.kat)}</span></span><span class="ort ort-${esc(t.dh)}">${esc(t.ort)}</span></a>`).join("");
  };
  eingabe.addEventListener("focus", holen, { once: true });
  eingabe.addEventListener("input", zeigen);
  eingabe.addEventListener("keydown", (e) => {
    if (!treffer.length) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + treffer.length) % treffer.length;
      [...sugg.children].forEach((a, i) => a.classList.toggle("sel", i === sel));
    } else if (e.key === "Enter" && sel >= 0) {
      e.preventDefault();
      sugg.children[sel].click();
    } else if (e.key === "Escape") {
      sugg.hidden = true;
    }
  });
  document.addEventListener("click", (e) => { if (!e.target.closest(".vb-comp")) sugg.hidden = true; });
}

/* ---------- Zurück-Link: Filter/Antworten beibehalten ---------- */
function initZurueck() {
  document.querySelectorAll("[data-back]").forEach((a) => {
    if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) {
      a.addEventListener("click", (e) => { e.preventDefault(); history.back(); });
    }
  });
}
