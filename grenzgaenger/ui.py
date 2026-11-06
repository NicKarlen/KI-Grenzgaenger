"""Icons und kleine HTML-Bausteine für die Templates."""
from markupsafe import Markup, escape

ICONS = {
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.6-3 3-4.8 5.5-4.8s4.9 1.8 5.5 4.8"/><path d="M16 5.2a3 3 0 0 1 0 5.6M17.5 14.4c1.6.6 2.7 2.2 3 4.6"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    "ch": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M12 7.5v9M7.5 12h9" stroke-width="2.6"/>',
    "eu": '<circle cx="12" cy="12" r="8.5"/><path d="M12 6.5v.01M12 17.5v.01M6.5 12h.01M17.5 12h.01M8.1 8.1h.01M15.9 15.9h.01M8.1 15.9h.01M15.9 8.1h.01" stroke-width="2.6"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.6 5.4 3.6 8.5s-1.1 5.9-3.6 8.5c-2.5-2.6-3.6-5.4-3.6-8.5S9.5 6.1 12 3.5z"/>',
    "chat": '<path d="M20 12a7.5 7.5 0 0 1-11 6.6L4 20l1.4-4.6A7.5 7.5 0 1 1 20 12z"/>',
    "layers": '<path d="M12 3.5 3.5 8 12 12.5 20.5 8z"/><path d="M3.5 12 12 16.5 20.5 12M3.5 16 12 20.5 20.5 16"/>',
    "tool": '<rect x="4" y="4" width="7" height="7" rx="1.8"/><rect x="13" y="4" width="7" height="7" rx="1.8"/><rect x="4" y="13" width="7" height="7" rx="1.8"/><circle cx="16.5" cy="16.5" r="3.6"/>',
    "code": '<path d="M8.5 8 4.5 12l4 4M15.5 8l4 4-4 4M13.5 5.5l-3 13"/>',
    "server": '<rect x="4" y="4" width="16" height="7" rx="1.5"/><rect x="4" y="13" width="16" height="7" rx="1.5"/><path d="M8 7.5h.01M8 16.5h.01" stroke-width="2.6"/>',
    "spark": '<path d="M12 3.5v4M12 16.5v4M3.5 12h4M16.5 12h4M6 6l2.6 2.6M15.4 15.4 18 18M6 18l2.6-2.6M15.4 8.6 18 6"/>',
    "db": '<ellipse cx="12" cy="6" rx="7" ry="2.5"/><path d="M5 6v12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V6M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>',
    "route": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M8 18h8M6 16V9a3 3 0 0 1 3-3h7"/>',
    "mic": '<rect x="9" y="3.5" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5v3"/>',
    "lang": '<path d="M4 6h9M8.5 4v2c0 4-2 7-4.5 8.5M6.5 10c1 2 3 3.6 5 4.5"/><path d="M13 20l3.5-8 3.5 8M14.2 17.5h4.6"/>',
    "scan": '<path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16M8 9h8M8 12h8M8 15h5"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    "office": '<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="m3.5 7.5 8.5 6 8.5-6"/>',
    "agent": '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9.5 13h.01M14.5 13h.01" stroke-width="2.2"/><path d="M3 13v2M21 13v2"/>',
    "brief": '<rect x="3.5" y="7" width="17" height="12.5" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3.5 12.5h17"/>',
    "model": '<path d="M12 3.5 20 8v8l-8 4.5L4 16V8z"/><path d="M4 8l8 4.5L20 8M12 12.5v8"/>',
    "image": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><circle cx="9" cy="10" r="1.8"/><path d="m4 18 5-5 4 4 2.5-2.5L20 19"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "filter": '<path d="M4 6h16M7 12h10M10 18h4"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.3"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "link":'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "linkedin": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 10.5V16M8 7.8v.01M11.5 16v-5.5M11.5 13c0-1.6 1-2.6 2.3-2.6s2.2.9 2.2 2.6V16" stroke-width="2"/>',
    "github": '<path d="M9 19c-4 1.3-4-2-5.5-2.5M14.5 21v-3.2c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.3 4.3 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6.2 0C6.1 3.1 5.1 3.4 5.1 3.4a4.3 4.3 0 0 0-.1 3.2A4.6 4.6 0 0 0 3.7 9.8c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    "external":'<path d="M14 4h6v6M20 4l-9 9M18 14v4.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 18.5v-11A1.5 1.5 0 0 1 5.5 6H10"/>',
}


def icon(name, size=20):
    pfad = ICONS.get(name, ICONS["spark"])
    return Markup(
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true" fill="none" stroke="currentColor" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{pfad}</svg>'
    )


def kann_auch(tool, maximal=0):
    """«Kann auch: …» – Funktionen zusätzlich zur Hauptkategorie, optional gekürzt."""
    fs = tool.extra_funktionen
    if not fs:
        return ""
    zeigen = fs[:maximal] if maximal else fs
    chips = "".join(f'<span class="chip chip-f">{icon(f["icon"], 13)}{escape(f["label"])}</span>' for f in zeigen)
    rest = len(fs) - len(zeigen)
    if rest:
        namen = escape(", ".join(f["label"] for f in fs[len(zeigen):]))
        chips += f'<span class="chip chip-o" title="{namen}">+{rest}</span>'
    return Markup(f'<div class="kann"><span class="l">Kann auch:</span>{chips}</div>')
