# ecowitt_iot — DEPRECATED

> **This integration is no longer maintained.** Ecowitt now publishes an
> official Home Assistant integration that covers the same devices over
> the same local API, and is actively developed:
>
> **https://github.com/Ecowitt/ha-ecowitt-iot**
>
> Release 0.2.0 is the final release of `ecowitt_iot`. It contains one
> safety fix (see below), the long-promised timer services, and a
> Repairs notice pointing you here. No further changes will be made
> and new issues will not be worked on.
>
> **The repository will be archived three months after the 0.2.0
> release date** (the exact date is in the release notes). Archiving
> makes it read-only; the 0.2.0 release stays installable through HACS,
> but nothing will be updated and issues cannot be opened.

Thank you to everyone who tested, reported bugs and sent pull requests.
This started because the core `ecowitt` integration is push-based and
could not drive the WFC01 WittFlow water timer or the AC1100 WittSwitch
plug; the vendor has now filled that gap properly.

## Migrating to the official integration

1. In HACS, add `https://github.com/Ecowitt/ha-ecowitt-iot` as a custom
   repository (category *Integration*), download it and restart Home
   Assistant.
2. Add **Ecowitt Official Integration** from *Settings → Devices &
   services*, pointing it at the same gateway IP you used here. Both
   integrations can run side by side during the changeover.
3. Confirm your valves and plugs appear and that switching them works.
4. Update automations, scripts, dashboards and helpers (in particular
   any `utility_meter`) to the new entity IDs. **Entity IDs do not carry
   over**: this integration keyed entities by device ID, the official
   one keys them by the device nickname.
5. Remove the `Ecowitt IoT (deprecated)` integration, then remove the
   repository from HACS.

### What the official integration does differently

| Feature | `ecowitt_iot` (this repo) | Official |
|---|---|---|
| WFC01 / AC1100 | Yes | Yes |
| WFC02 | No | Yes |
| Valve / plug switch | Yes | Yes, with optimistic state |
| Flow rate, water total, power, voltage, energy | Yes | Yes |
| Water temperature unit | °C or °F | °F, converted by HA |
| Warning-bit binary sensors (leak, no water, temp, battery) | Yes | No |
| Device-side timed run / run by volume (services) | Yes | No |
| Weather-station sensors on the same gateway | No | Yes |
| Poll interval | Fixed 30 s | Configurable, default 10 s |

If you relied on the warning-bit binary sensors or the timer services,
raise those as feature requests on the official repository; the data and
commands are in the local API and in the `wittiot` library the official
integration already uses (it supports a run duration internally but does
not expose it).

## 0.2.0 — final release

* **Fix:** a bare `200 OK` from the gateway (command accepted, no reading
  yet) was turned into a complete set of fabricated zero readings.
  `water_total: 0.00` is a valid value for a `total_increasing` sensor,
  so the next real reading looked like a meter rollover and
  `utility_meter` helpers booked the whole lifetime counter as
  consumption. The coordinator now keeps the last good reading or leaves
  the device unavailable. Reported with a precise diagnosis in #19.
* Added a Repairs issue announcing the deprecation.
* Added `async_unload_entry` so the integration can be reloaded and
  removed cleanly.
* **New:** the `set_valve_timer` and `set_power_timer` services that
  `services.yaml` has advertised since 0.1.0 now exist, plus
  `run_by_volume` for the WFC01 (#3). All three run the timer on the
  gateway (`quick_run` with `always_on: 0`), so the output stops even if
  Home Assistant goes away mid-cycle. The config flow's temperature unit
  option is unchanged; the API documents `water_temp` as °F, so if your
  reading looks wrong under °C that is why (#14).
* Merged local brand assets (#21).

## Reference

The local HTTP API this integration used is Ecowitt's "Local IoT API"
document (`get_iot_device_list` and `parse_quick_cmd_iot` with the
`read_device`, `quick_run` and `quick_stop` commands); the official
integration's `wittiot` library implements the same calls.

This project is licensed under the terms in `LICENSE`.
