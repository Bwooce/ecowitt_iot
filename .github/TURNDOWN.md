# Turndown runbook

Steps to run once PR #22 is merged. Each one is a public action.
Timeline: release and close issues on day 0; archive three months
later, to give people time to migrate. Set ARCHIVE_DATE = release date
+ 3 months and substitute it below before posting.

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

Also new: `set_valve_timer`, `set_power_timer` and `run_by_volume`
services that run the timer on the gateway itself (#3), a Repairs notice
announcing the deprecation, clean unload, and brand assets (#21).

Thank you to everyone who tested and reported. No further releases.
This repository will be archived on ARCHIVE_DATE; 0.2.0 stays
installable through HACS after that, but nothing more will change.

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
guide. The repository will be archived on ARCHIVE_DATE.

---

Issues: #1 #2 #3 #4 #5 #11 #12 #13 #14 #15 #16 #17 #18 #20.

For #16 add: "Thanks for the heads-up — this is what prompted the
turndown."

For #20 add: "The integration was never in the HACS default list, only
installable as a custom repository; HACS 2.x stopped listing custom
repositories you have not added, which is what you saw."

## 3. Archive (on ARCHIVE_DATE, three months after release)

Settings → General → Archive this repository. Archiving is reversible
and keeps releases installable through HACS. Between release and
archive, respond to new issues only with the pointer above.

## Not done

- No reformat of untouched files to 76 columns; this is a final
  release, not a tidy-up.
- The WFC02 requests (#15, #17, #18) are met by the official
  integration, not here.
- #3 (water by volume) and #4 (water this session) — #3 is now done via
  `run_by_volume`; #4 is `water_total - happen_water` and is left for
  the official integration.
- Ecowitt's "Local IoT API" document says `val_type` 3 is "volume (L)".
  It is tenths of a litre (confirmed on a live WFC01 and by the
  `wittiot` library's `val / 10`). Worth noting if anyone raises the
  volume feature on the official repository.
