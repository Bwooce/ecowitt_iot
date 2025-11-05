# ecowitt_iot custom integration for HACS HomeAssistant

## ⚠️ DEPRECATION NOTICE ⚠️

**This integration is deprecated and will no longer be maintained.**

Please migrate to the **official Ecowitt company integration**: https://github.com/Ecowitt/ha-ecowitt-iot

### Why Migrate?
- ✅ **Official company support** from Ecowitt
- ✅ **Same functionality** - supports WFC01 water timer and AC1100 smart plug
- ✅ **Better maintenance** - regular updates and bug fixes
- ✅ **Same architecture** - local polling, no cloud dependency

### For Existing Users
📖 **See [MIGRATION.md](MIGRATION.md) for complete step-by-step migration instructions.**

### For New Users
❌ **Do not install this integration.** Use the official integration instead: https://github.com/Ecowitt/ha-ecowitt-iot

---

## About This Integration (Historical)

This custom integration supports the WFC01 WittFlow water timer and the AC1100 WittSwitch smart plug.

Created as the existing core ecowitt integration is a push based implementation (runs a server listening for weather station data), and the Ecowitt IOT devices need a polling/local api approach. Smooshing them together seemed overly complicated, so this is a different standalone integration. There's no cross-over interference with the core ecowitt integration, they're not working with the same end-devices, and if you have both Ecowitt IOT and non-IOT (weatherstation, soil sensors) devices then you want both this integration and the core one [docs](https://www.home-assistant.io/integrations/ecowitt/).

# Status
## In active development

## WFC01 Wittflow water timer
Working, pending update to add more tests and better cope with the activation delay where the switch un-sets itself while the Ecowitt gateway/device are 
## AC1100 WittSwitch smart plug 
Untested (unowned). Should work but feedback welcome

# Installation Instructions

## Prerequisites: Installing HACS

If you haven't installed HACS yet, follow the [official HACS installation instructions](https://hacs.xyz/docs/setup/download).

## Installing the ecowitt_iot Integration

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the "+" button in the bottom right corner
4. Search for "ecowitt_iot" or click the three dots menu (⋮) in the top right corner and select "Custom repositories"
5. Add `https://github.com/Bwooce/ecowitt_iot` as a new custom repository:
   - Category: Integration
   - URL: `https://github.com/Bwooce/ecowitt_iot`
6. Click "Add"
7. A new repository card should appear
8. Click "Download"
9. Restart Home Assistant

## Configuration

After installation, add the integration through the Home Assistant UI:

1. Navigate to Configuration → Integrations
2. Click the "+ Add Integration" button
3. Search for "Ecowitt IoT" and select it
4. Follow the configuration steps to complete the setup, see the [setup instructions](ecowitt_iot.markdown) for further guidance.

If you encounter any issues, please check the [Issues](https://github.com/Bwooce/ecowitt_iot/issues) section of the repository.
