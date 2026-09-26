# AGENTS.md — Simple-With-Us repo memory

## What this repo is

`Simple-With-Us` is the **fleet marketing repo**.  It hosts the static
catalog at `https://simplewithus.com/` and one page per app at
`https://simplewithus.com/<slug>/` (plus `/<slug>/support.html`).  There is
no app code in this repository; each shipped tool lives in its own fleet
repo.  The design brief and the hosting, DNS, and AASA plan live in
[docs/DESIGN-BRIEF.md](docs/DESIGN-BRIEF.md).

The app list is data, not prose: `apps/index.json` is the single source of
truth, and `python3 scripts/build_catalog.py` regenerates the card grid in
`index.html` (CI runs it with `--check`).  Paths and repos as of 2026-09-25:

| App                  | Fleet repo                          | Page on this site        | Other hostname                        |
| -------------------- | ----------------------------------- | ------------------------ | ------------------------------------- |
| CodeCaps (Mac, iOS)  | `jaywedgeworth22/CodeCaps`          | `/codecaps/`             | `codecaps.simplewithus.com` (CodeCaps repo's own Pages) |
| Usage Client Monitor | `jaywedgeworth22/Usage-Monitor`     | `/usage-client/`         | `usage.jays.services` (web app)       |
| Usage Local Monitor  | `jaywedgeworth22/Usage-Monitor`     | `/usage-local/`          | none                                  |
| MiniMax Remote       | `jaywedgeworth22/MiniMax-ios` (private) | `/minimax-remote/`   | none                                  |
| Harness              | `jaywedgeworth22/Harness`           | none yet                 | none (`harness.` is not claimed)      |
| HogHunter            | `jaywedgeworth22/HogHunter`         | none yet                 | none                                  |
| BotFleet             | `jaywedgeworth22/BotFleet`          | `/botfleet/`             | `botfleet.app`                        |
| Socratic.Trade       | `jaywedgeworth22/Socratic-Trade`    | `/socratic-trade/`       | `socratictrade.com`                   |
| Congress.Trade       | `jaywedgeworth22/Congress.Trade`    | `/congress-trade/`       | `congress.trade`                      |
| ContactLogo          | `jaywedgeworth22/ContactLogo`       | `/contactlogo/`          | `contactlogo.com`                     |
| DealDex              | `jaywedgeworth22/DealDex`           | `/dealdex/`              | `dealdex.net`                         |
| Autorotate           | `jaywedgeworth22/Autorotate`        | `/autorotate/`           | `autorotate.codes` (no A record yet)  |

`harness.`, `local.`, `client.`, `remote.`, and every other unlisted label
currently resolve only through a wildcard `*` CNAME to
`jaywedgeworth22.github.io` that no Pages site claims.  Do not link to them.
The brief's section 6 has the fix.

To add a new app: add its entry to `apps/index.json`, copy `_template/` to
`<slug>/` at the repo root, run `python3 scripts/build_catalog.py`, and add
the matching brand domain in `~/apps/ios-fleet/apps.json` (cross-link with
the iOS-fleet registry).  Never move or delete an existing
`<slug>/support.html`: App Store Connect records point at those URLs.

Hosting and routing (apexes, hostnames, hosts, deploy paths): see [`Fleet-OPS/docs/DOMAINS-AND-ROUTING.md`](https://github.com/jaywedgeworth22/Fleet-OPS/blob/main/docs/DOMAINS-AND-ROUTING.md). Built from live Cloudflare, Vercel, Coolify, Namecheap/RDAP, and GitHub APIs by CLAUDE on 2026-09-25; refresh via `Fleet-OPS/scripts/domain-inventory/run-all.sh`.

## Branch and worktree conventions

* Default branch is `main`.
* Per-seat worktrees live at `~/apps/simplewithus-mm-<lane>` and branches
  follow the `mm/<lane>` convention.  All MM-side work happens in
  worktrees; never edit `~/Code/Simple-With-Us` directly (the daemon
  resets it).
* The `main` branch deploys automatically through GitHub Pages;
  DNS at Cloudflare maps the apex `simplewithus.com` to GitHub Pages.

## Adding a new app landing page

1. Add the app to `apps/index.json`, then copy `_template/` to `<slug>/`
   at the repo root.
2. Replace the brand mark, copy, and links.  Follow the fleet UI copy
   guide at `/Users/jay/apps/FLEET-UI-COPY.md` and the brand-domain map
   in agent memory (search `fleet-brand-domains`).
3. Add a `<link rel="canonical">` and an Open Graph block to the page
   `<head>`.
4. Run `python3 scripts/build_catalog.py`, then open a PR against `main`.
   Once merged, GitHub Pages publishes within ~60 seconds.

## Licensing

Apache 2.0.  See [LICENSE](LICENSE).  New app directories must include
an attribution block at the bottom of `index.html` linking back to the
upstream fleet repo.
