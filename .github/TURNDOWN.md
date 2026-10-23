# Turndown runbook

Steps to run once PR #22 is merged. Each one is a public action.
Timeline: released 23 October 2026; issues closed the same day;
archive on 23 January 2027, three months later.

## 1. Release 1.1.0

Why 1.1.0 and not 0.2.0: the existing release is tagged `1.0.0`
(Nov 2024, manifest said 0.1.0). HACS sorts by release tag, so a
lower-numbered final release would never be offered as an update and
the deprecation notice would reach nobody. Tag `main` as `1.1.0` (no
`v` prefix, matching the existing tag) and publish a GitHub release
with this body
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
announcing the deprecation, faster switch state after a command, clean
unload, and brand assets (#21). Validated on a GW2000 with a live WFC01.

Thank you to everyone who tested, reported and sent fixes, and for
your patience while this sat untouched for most of a year; a one-person
side project did not keep up with the demand, and I am glad the vendor
has taken it on properly. No further releases. This repository will be
archived on 23 January 2027; 1.1.0 stays installable through HACS after
that, but nothing more will change.

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
Release 1.1.0 of this integration is final; the README has a migration
guide. The repository will be archived on 23 January 2027.

Thank you for your patience - this went unanswered far longer than it
should have.

---

Issues: #1 #2 #3 #4 #5 #11 #12 #13 #14 #15 #16 #17 #18 #20.

For #16 add: "Thanks for the heads-up — this is what prompted the
turndown."

For #20 add: "The integration was never in the HACS default list, only
installable as a custom repository; HACS 2.x stopped listing custom
repositories you have not added, which is what you saw."

## 2a. Pull requests

- #21 (brand assets): its commit is on `turndown` unchanged, so GitHub
  marks it merged when #22 lands. Verify; close manually if not.
- #19 (fabricated readings, closed unmerged): comment and leave closed:

  > Thank you for this - the diagnosis was exactly right and the fix in
  > 1.1.0 (final release) does what your PR did: a bare `200 OK` now
  > keeps the last real reading or leaves the device unavailable, never
  > zeroed values. Credited in the README and release notes. Sorry it
  > sat unanswered; the project is winding down in favour of Ecowitt's
  > official integration (see the README).

## 3. Archive (on 23 January 2027, three months after release)

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
