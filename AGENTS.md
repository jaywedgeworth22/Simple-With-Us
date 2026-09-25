# AGENTS.md — Simple-With-Us repo memory

## What this repo is

`Simple-With-Us` is the **fleet marketing repo**.  It hosts static landing
pages served at `https://simplewithus.com` and at `https://<app>.simplewithus.com`
for each published tool.  There is no app code in this repository; each
shipped tool lives in its own fleet repo.

| App          | Fleet repo                                                      | Public URL                                |
| ------------ | --------------------------------------------------------------- | ----------------------------------------- |
| CodeCaps iOS | `jaywedgeworth22/codecaps`                                      | `https://codecaps.simplewithus.com/...`   |
| CodeCaps Mac | `jaywedgeworth22/codecaps`                                      | `https://codecaps.simplewithus.com/mac...`|
| Harness      | `jaywedgeworth22/harness`                                       | `https://harness.simplewithus.com/...`    |
| Usage Local  | `jaywedgeworth22/usage-local`                                   | `https://local.simplewithus.com/...`      |
| Usage Client | `jaywedgeworth22/usage-client`                                  | `https://client.simplewithus.com/...`     |
| MiniMax Remote | `jaywedgeworth22/minimax-remote`                              | `https://remote.simplewithus.com/...`     |

To add a new app: create `<slug>/index.html` at the repo root, link it from the
top-level nav, and add the matching brand domain in
`~/apps/ios-fleet/apps.json` (cross-link with the iOS-fleet registry).

## Branch and worktree conventions

* Default branch is `main`.
* Per-seat worktrees live at `~/apps/simplewithus-mm-<lane>` and branches
  follow the `mm/<lane>` convention.  All MM-side work happens in
  worktrees; never edit `~/Code/Simple-With-Us` directly (the daemon
  resets it).
* The `main` branch deploys automatically through GitHub Pages;
  DNS at Cloudflare maps the apex `simplewithus.com` to GitHub Pages.

## Adding a new app landing page

1. Copy `_template/` (when one exists) to `<slug>/` at the repo root.
2. Replace the brand mark, copy, and links.  Follow the fleet UI copy
   guide at `/Users/jay/apps/FLEET-UI-COPY.md` and the brand-domain map
   in agent memory (search `fleet-brand-domains`).
3. Add a `<link rel="canonical">` and an Open Graph block to the page
   `<head>`.
4. Open a PR against `main`.  Once merged, GitHub Pages publishes within
   ~60 seconds.

## Licensing

Apache 2.0.  See [LICENSE](LICENSE).  New app directories must include
an attribution block at the bottom of `index.html` linking back to the
upstream fleet repo.
