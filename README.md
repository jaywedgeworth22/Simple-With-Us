# Simple With Us

Marketing pages for tools published at [simplewithus.com](https://simplewithus.com).

This repository hosts the static landing pages that appear at
`/<slug>/` on the Simple With Us site, one directory per published
tool.  It is intentionally thin: build artifacts live alongside the
sources, and there are no runtime services.  Each app lives in its own
fleet repo under the jaywedgeworth22 organization; this repo is the
shared marketing surface for them all.

## What lives here

```
index.html             family-directory homepage listing every fleet app
privacy.html           universal privacy notice
support.html           general support landing
terms.html             universal terms
style.css              single stylesheet, no preprocessor, no JS framework
<slug>/                per-app marketing (index.html) + support (support.html)
assets/                shared visual assets (logos, favicons, og images)
LICENSE                Apache 2.0
```

## URL scheme

Today every published tool lives at a path under the apex:

* `https://simplewithus.com/`                family directory
* `https://simplewithus.com/codecaps/`       CodeCaps iOS landing
* `https://simplewithus.com/minimax-remote/` MiniMax Remote landing

The long-term intent in `AGENTS.md` is one subdomain per app
(`codecaps.simplewithus.com`, `remote.simplewithus.com`,
etc.) with a Cloudflare wildcard CNAME.  That migration is parked
until each per-app page has its own canonical URL and the wildcard
DNS / Pages routing layer is ready.

## Hosting

Deployed via GitHub Pages on the `main` branch root, exposed at
`simplewithus.com` through the `simplewithus.com` Cloudflare DNS
zone.  Apex maps via Cloudflare CNAME flattening to GitHub Pages;
the repo root carries a `CNAME` file so the Pages build serves the
apex directly.

## Conventions

* Use sentence case for prose, Title Case for buttons, headings, and
  the page `<title>`.
* Two literal ASCII spaces between sentences in every human-readable
  surface, including this README.
* Default UI theme follows the system preference, never a hard-coded
  light or dark mode.
* Keep this repo read-only-friendly: do not commit generated images
  larger than 1 MB without re-encoding them first.

## Local preview

```
cd Simple-With-Us
python3 -m http.server 8080
```

Open `http://localhost:8080/` for the homepage,
`http://localhost:8080/codecaps/` for the CodeCaps landing,
etc.

## License

Apache 2.0.  See [LICENSE](LICENSE).
