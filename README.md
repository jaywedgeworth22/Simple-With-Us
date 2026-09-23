# Simple With Us

Marketing pages for tools published at [simplewithus.com](https://simplewithus.com).

This repository hosts the static landing pages that appear under
`/apps/<slug>/` on the Simple With Us site, one directory per published
tool.  It is intentionally thin: build artifacts live alongside the
sources, and there are no runtime services.  Each app lives in its own
fleet repo under the jaywedgeworth22 organization, this repo is the
shared marketing surface for them all.

## What lives here

```
apps/                  one sub-directory per published tool
  .gitkeep             forces the empty-apps convention until the owner adds the first one
index.html             (none yet) — the per-app landing pages generate into apps/<slug>/index.html
assets/                shared visual assets (logos, favicons, og images)
```

## Hosting

Deployed via GitHub Pages on the `main` branch root, exposed at
`simplewithus.com` through the `simplewithus.com` Cloudflare DNS zone.
Sub-paths (`/apps/<slug>/`) become their own static sites, one per
published tool.

## Conventions

* Use sentence case for prose, Title Case for buttons, headings, and the
  page `<title>`.
* Two literal ASCII spaces between sentences in every human-readable
  surface, including this README.
* Default UI theme follows the system preference, never a hard-coded light
  or dark mode.
* Keep this repo read-only-friendly: do not commit generated images
  larger than 1 MB without re-encoding them first.

## License

Apache 2.0.  See [LICENSE](LICENSE).
