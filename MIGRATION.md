# Migration Guide: ecowitt_iot → Official Ecowitt Integration

## ⚠️ Important Notice

This custom integration (`ecowitt_iot`) is being deprecated in favor of the **official Ecowitt company integration**. The official integration provides the same functionality with company support and ongoing maintenance.

**Official Integration Repository:** https://github.com/Ecowitt/ha-ecowitt-iot

---

## Why Migrate?

- ✅ **Official Support**: Backed by Ecowitt company
- ✅ **Better Maintenance**: Regular updates for new devices and firmware
- ✅ **Same Functionality**: Supports WFC01 water timer and AC1100 smart plug
- ✅ **Local Polling**: Same architecture (no cloud dependency)
- ✅ **Active Development**: Dedicated development team

---

## Before You Begin

### 1. Document Your Current Setup

Take note of:
- Gateway IP address (you'll need this for the new integration)
- Device names and configurations
- Any automations using `ecowitt_iot` entities
- Dashboard cards showing `ecowitt_iot` entities

**Tip**: Take screenshots of your Lovelace dashboards before migration.

### 2. Backup Your Configuration

```bash
# Backup your Home Assistant configuration
# Method varies by installation type (HAOS, Docker, Core)
```

### 3. Check Compatibility

Ensure your gateway model is supported by the official integration:

**✅ Supported with IoT devices:**
- GW1200, GW2000, GW3000
- WS6210, WS3800, WS3820, WS3900, WS3910
- WN1700, WN1820, WN1821, WN1920, WN1980

**✅ Supported without IoT devices:**
- GW1100

**❌ Not supported:**
- GW1000, WS6006, WN1900, WN1910, WS2320, WS2910, HP2550, HP3500, HP2560

---

## Migration Steps

### Step 1: Install the Official Integration via HACS

1. Open **HACS** in your Home Assistant instance
2. Click on **Integrations**
3. Click the **three dots (⋮)** in the top right corner
4. Select **Custom repositories**
5. Add the official repository:
   - **URL**: `https://github.com/Ecowitt/ha-ecowitt-iot`
   - **Category**: `Integration`
6. Click **ADD**
7. Search for "**Ecowitt Official Integration**" in HACS
8. Click **Download**
9. **Restart Home Assistant**

### Step 2: Configure the Official Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "**Ecowitt Official Integration**"
4. Enter your gateway's **IP address** (same as before)
5. The integration will discover your devices automatically
6. Follow the setup wizard to complete configuration

### Step 3: Verify Devices Are Working

Check that all your devices appear:
- Go to **Settings** → **Devices & Services**
- Click on the **Ecowitt Official Integration**
- Verify all devices are listed
- Check that sensors are updating with current values

### Step 4: Update Entity IDs in Automations

Entity IDs will change due to the different integration domain. You'll need to update:

#### Entity ID Changes

**Old format** (ecowitt_iot):
```
sensor.ecowitt_iot_device_name_water_status
switch.ecowitt_iot_device_name
binary_sensor.ecowitt_iot_device_name_warning
```

**New format** (ha_ecowitt_iot):
```
sensor.ha_ecowitt_iot_device_name_water_status
switch.ha_ecowitt_iot_device_name
binary_sensor.ha_ecowitt_iot_device_name_warning
```

#### How to Update Automations

**Option A: Via UI**
1. Go to **Settings** → **Automations & Scenes**
2. Edit each automation that uses `ecowitt_iot` entities
3. Remove old entity triggers/conditions/actions
4. Add new entities from the official integration
5. Save changes

**Option B: Via YAML (Advanced)**

Find all references in your configuration:
```bash
# Search your config directory for ecowitt_iot references
grep -r "ecowitt_iot" config/
```

Update YAML files:
```yaml
# Before
- entity_id: switch.ecowitt_iot_water_timer

# After
- entity_id: switch.ha_ecowitt_iot_water_timer
```

### Step 5: Update Dashboard Cards

Go through each dashboard and update entity references:

1. Edit each dashboard
2. Edit cards that reference old entities
3. Select new entities from the official integration
4. Save changes

**Tip**: Use the entity search feature - start typing the device name to find the new entities.

### Step 6: Remove Old Integration

**⚠️ Only do this after verifying everything works!**

1. Go to **Settings** → **Devices & Services**
2. Find the **Ecowitt IoT** integration (old one)
3. Click the **three dots (⋮)**
4. Click **Delete**
5. Confirm deletion
6. **Restart Home Assistant**

### Step 7: Clean Up (Optional)

Remove the old custom integration files:

1. Navigate to your Home Assistant configuration directory
2. Go to `custom_components/`
3. Delete the `ecowitt_iot` folder
4. **Restart Home Assistant**

---

## Common Issues & Troubleshooting

### Issue: Official integration not finding devices

**Solution:**
- Verify gateway IP address is correct
- Ensure gateway firmware is up to date
- Check that devices are registered in the Ecowitt app
- Restart the gateway and try again

### Issue: Entities have different names

**Solution:**
- Entity naming may vary slightly between integrations
- Use the entity search feature to find the correct new entities
- You can rename entities via Settings → Entities

### Issue: Automations not working after migration

**Solution:**
- Double-check that entity IDs were updated correctly
- Verify the new entities are receiving data (check State history)
- Review automation traces for errors
- Test automations manually

### Issue: Missing sensors or switches

**Solution:**
- Ensure the official integration supports your device model
- Check if sensors are disabled (Settings → Entities → Show disabled entities)
- Reload the integration
- Check logs for any error messages

---

## Feature Comparison

| Feature | Old (ecowitt_iot) | Official (ha_ecowitt_iot) |
|---------|-------------------|---------------------------|
| WFC01 Water Timer | ✅ | ✅ |
| AC1100 Smart Plug | ✅ (untested) | ✅ |
| Local HTTP API | ✅ | ✅ |
| No cloud dependency | ✅ | ✅ |
| Company support | ❌ | ✅ |
| Python library | Custom | wittiot==1.0.30 |
| Update interval | Configurable | 10 seconds |

---

## Getting Help

### Official Integration Support

- **GitHub Issues**: https://github.com/Ecowitt/ha-ecowitt-iot/issues
- **Documentation**: https://github.com/Ecowitt/ha-ecowitt-iot

### Home Assistant Community

- **Community Forum**: https://community.home-assistant.io/
- Search for "Ecowitt" topics

### Ecowitt Support

- **Ecowitt Website**: https://www.ecowitt.com/
- **Support Email**: Check your device documentation

---

## Timeline

- **Now**: Migration guide available, both integrations work
- **Recommended**: Migrate within the next 3 months
- **Future**: This repository will be archived (read-only)

---

## Rollback (If Needed)

If you need to rollback to the old integration:

1. Remove the official integration
2. Reinstall `ecowitt_iot` from this repository via HACS
3. Reconfigure with your gateway IP
4. Restore entity IDs in automations/dashboards

**Note**: This repository will be archived soon, so migration is recommended.

---

## Questions?

If you encounter issues during migration:

1. Check the troubleshooting section above
2. Review logs: Settings → System → Logs
3. Open an issue on the official integration: https://github.com/Ecowitt/ha-ecowitt-iot/issues

---

**Thank you for using ecowitt_iot!** The official integration will serve you better going forward.

*Last Updated: 2025-11-05*
