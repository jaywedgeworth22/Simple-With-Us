#!/usr/bin/env python3
"""Render the simplewithus.com catalog from apps/index.json.

Usage:
  python3 scripts/build_catalog.py          # rewrite the generated regions of index.html
  python3 scripts/build_catalog.py --check  # exit 1 if index.html is stale or a rule fails

Standard library only.  The generated regions sit between
<!-- catalog:<name>:start --> and <!-- catalog:<name>:end --> markers.
Everything outside the markers is hand-written and left alone.

Rules enforced (see docs/DESIGN-BRIEF.md sections 5 and 9):
  * a link is either null or a real URL of the right shape (no bare testflight.apple.com)
  * every page, support page, and icon named in the data exists in the repo
  * no committed image is over 200 KB, except the legacy files listed below
  * the AASA file is valid JSON and lists every app that sets associatedDomains
  * index.html matches what this script would generate
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "apps" / "index.json"
PAGE = ROOT / "index.html"
AASA = ROOT / ".well-known" / "apple-app-site-association"
IMAGE_BUDGET = 200 * 1024
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg"}
# Oversize files that predate the budget.  Delete or re-encode them, then drop them from this list.
LEGACY_OVERSIZE = {
    "assets/app-icons/ar.png",
    "assets/app-icons/bf.png",
    "assets/app-icons/ct.png",
    "assets/app-icons/dd.png",
    "assets/app-icons/st.png",
    "assets/app-icons/um.png",
    "assets/logos/swu-logo-wide.svg",
    "assets/logos/swu-logo-wide.webp",
}
NBSP_GAP = "  "  # FLEET-UI-COPY: U+00A0 plus a space between sentences in HTML

LINK_RULES = {
    "website": re.compile(r"^https://[a-z0-9.-]+\.[a-z]{2,}(/.*)?$"),
    "github": re.compile(r"^https://github\.com/jaywedgeworth22/[A-Za-z0-9._-]+$"),
    "appStore": re.compile(r"^https://apps\.apple\.com/app/id\d+$"),
    "testFlight": re.compile(r"^https://testflight\.apple\.com/join/[A-Za-z0-9]+$"),
    "brew": re.compile(r"^brew install (--cask )?[a-z0-9/_-]+$"),
}


def gap(text: str) -> str:
    """Escape, then turn a two-ASCII-space sentence gap into U+00A0 plus a space."""
    out = html.escape(text, quote=True)
    for mark in ".?!":
        out = out.replace(mark + "  ", mark + NBSP_GAP)
    return out


def attr(text: str) -> str:
    return html.escape(text, quote=True)


def app_store_url(url: str, slug: str, provider_token) -> str:
    if provider_token:
        return f"{url}?pt={provider_token}&ct=swu-{slug}-card"
    return f"{url}?ct=swu-{slug}-card"


def card(app: dict, provider_token) -> str:
    links = app["links"]
    primary = app.get("page") or links.get("website") or links.get("github")
    secondary = []
    if links.get("website") and links["website"] != primary:
        secondary.append((links["website"], "Website"))
    if links.get("appStore"):
        secondary.append((app_store_url(links["appStore"], app["slug"], provider_token), "App Store"))
    if links.get("testFlight"):
        secondary.append((links["testFlight"], "Join the Beta"))
    if links.get("github") and links["github"] != primary:
        secondary.append((links["github"], "Source"))
    if app.get("support"):
        secondary.append((app["support"], "Support"))

    out = [f'<li class="card" style="--card-accent: {attr(app["accent"])}">']
    out.append('  <div class="card-head">')
    out.append(f'    <img class="card-icon" src="{attr(app["icon"])}" alt="" width="48" height="48" loading="lazy" decoding="async">')
    out.append("    <div>")
    rel = "" if primary.startswith("/") else ' rel="noopener"'
    out.append(f'      <h3><a href="{attr(primary)}"{rel}>{gap(app["name"])}</a></h3>')
    pills = "".join(f'<li class="pill">{gap(p)}</li>' for p in app["platforms"])
    out.append(f'      <ul class="pills" aria-label="Platforms">{pills}</ul>')
    out.append("    </div>")
    out.append("  </div>")
    out.append(f'  <p>{gap(app["tagline"])}</p>')
    out.append(f'  <span class="status status-{attr(app["status"])}">{gap(app["statusText"])}</span>')
    if secondary:
        out.append('  <div class="card-links">')
        for href, label in secondary:
            if href.startswith("/"):
                out.append(f'    <a href="{attr(href)}">{label}</a>')
            else:
                out.append(f'    <a href="{attr(href)}" rel="noopener">{label}<span aria-hidden="true"> ↗</span></a>')
        out.append("  </div>")
    out.append("</li>")
    return "\n".join(out)


def render(data: dict) -> dict:
    apps = data["apps"]
    token = data.get("appStoreProviderToken")
    grid = ['<ul class="grid" role="list">'] + [card(a, token) for a in apps] + ["</ul>"]
    public_src = sum(1 for a in apps if a["links"].get("github"))
    facts = f'<p class="facts">{len(apps)} apps · {public_src} with public source · Apache\u20112.0</p>'
    return {"facts": facts, "grid": "\n".join(grid)}


def splice(page: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- catalog:{name}:start -->)(.*?)(\s*<!-- catalog:{name}:end -->)", re.S)
    if not pat.search(page):
        raise SystemExit(f"index.html is missing the catalog:{name} markers")
    return pat.sub(lambda m: m.group(1) + "\n" + body + m.group(3), page, count=1)


def exists(path: str) -> bool:
    p = ROOT / path.lstrip("/")
    return p.is_file() or (p / "index.html").is_file()


def lint(data: dict) -> list:
    errors = []
    seen = set()
    for app in data["apps"]:
        slug = app["slug"]
        if slug in seen:
            errors.append(f"{slug}: duplicate slug")
        seen.add(slug)
        for key, rule in LINK_RULES.items():
            val = app["links"].get(key)
            if val is not None and not rule.match(val):
                errors.append(f"{slug}: links.{key} does not match {rule.pattern}")
        for key in ("page", "support", "icon"):
            val = app.get(key)
            if val and not exists(val):
                errors.append(f"{slug}: {key} {val} does not exist in the repo")
        if not (app.get("page") or app["links"].get("website") or app["links"].get("github")):
            errors.append(f"{slug}: needs at least one of page, links.website, links.github")
    for img in ROOT.rglob("*"):
        rel = img.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or img.suffix.lower() not in IMAGE_EXTS or not img.is_file():
            continue
        if img.stat().st_size > IMAGE_BUDGET and rel not in LEGACY_OVERSIZE:
            errors.append(f"{rel} is {img.stat().st_size} bytes, over the 200 KB image budget")
    try:
        aasa = json.loads(AASA.read_text())
        listed = {i for d in aasa["applinks"]["details"] for i in d["appIDs"]}
        for app in data["apps"]:
            if app.get("associatedDomains"):
                for bid in app["bundleIds"]:
                    if f'{data["teamId"]}.{bid}' not in listed:
                        errors.append(f"{app['slug']}: {bid} declares associated domains but is not in the AASA file")
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"AASA file invalid: {exc}")
    return errors


def main() -> int:
    check = "--check" in sys.argv
    data = json.loads(DATA.read_text())
    errors = lint(data)
    page = PAGE.read_text()
    new = page
    for name, body in render(data).items():
        new = splice(new, name, body)
    if new != page:
        if check:
            errors.append("index.html is stale: run python3 scripts/build_catalog.py and commit the result")
        else:
            PAGE.write_text(new)
            print("index.html regenerated")
    for e in errors:
        print("error:", e, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
