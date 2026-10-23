# Turndown runbook

Steps to run once PR #22 is merged. Each one is a public action.

## 1. Release v0.2.0

Tag `main` as `v0.2.0` and publish a GitHub release with this body
(HACS surfaces it in the update prompt, which is the only channel that
reaches installed users):

---

**Final release — this integration is deprecated.**

Ecowitt now publishes an official Home Assistant integration for the
WFC01, WFC02 and AC1100 over the same local API, and it is actively
maintained: https://github.com/Ecowitt/ha-ecowitt-iot

Install it, check your valves and plugs appear, move your automations
and `utility_meter` helpers to the new entity IDs (they do not carry
over), then remove this integration. The README has a migration guide
and a feature comparison.

This release contains one fix worth taking even if you plan to migrate
later: a bare `200 OK` from the gateway was being turned into zeroed
readings, which `utility_meter` helpers booked as a meter rollover
(#19). The coordinator now keeps the last real reading instead.

Also: a Repairs notice announcing the deprecation, clean unload, brand
assets (#21), and the never-implemented timer services removed.

Thank you to everyone who tested and reported. No further releases.

---

## 2. Close open issues

Post this comment on each open issue, then close it as
"not planned" (#16 gets the extra thank-you line):

---

Closing as part of winding this project down. Ecowitt now publishes an
official Home Assistant integration that covers the WFC01, WFC02 and
AC1100 over the same local API, and is actively maintained:

https://github.com/Ecowitt/ha-ecowitt-iot

If this issue still applies there, please raise it on that repository.
Release 0.2.0 of this integration is final; the README has a migration
guide.

---

Issues: #1 #2 #3 #4 #5 #11 #12 #13 #14 #15 #16 #17 #18 #20.

For #16 add: "Thanks for the heads-up — this is what prompted the
turndown."

For #20 add: "The integration was never in the HACS default list, only
installable as a custom repository; HACS 2.x stopped listing custom
repositories you have not added, which is what you saw."

## 3. Archive

Settings → General → Archive this repository. Archiving is reversible
and keeps releases installable through HACS.

## Not done

- No reformat of untouched files to 76 columns; this is a final
  release, not a tidy-up.
- The WFC02 requests (#15, #17, #18) are met by the official
  integration, not here.
