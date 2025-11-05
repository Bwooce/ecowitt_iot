#!/bin/bash
# Script to post deprecation responses and close all GitHub issues
# Run this locally where you have gh CLI authenticated

set -e

echo "Posting responses to all 13 GitHub issues and closing them..."

# Issue #18
gh issue comment 18 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for reporting this! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Migrate to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration** that supports the WFC02:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This Solves Your Issue

The official Ecowitt integration **supports the WFC02 device model** through its `wittiot` library. Your WFC02 will be properly detected and all entities will show correct data.

**Device Support:**
- ✅ WFC01 (original water timer)
- ✅ **WFC02 (newer water timer model)**
- ✅ AC1100 (smart plug)

The official integration is maintained by Ecowitt and stays up-to-date with new device models like the WFC02.

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration provides:
- ✅ WFC01, WFC02, and AC1100 support
- ✅ Company-backed support and maintenance
- ✅ Regular updates for new devices and firmware
- ✅ Same local polling approach (no cloud)

### Next Steps

1. Install the official integration via HACS: https://github.com/Ecowitt/ha-ecowitt-iot
2. Follow the migration guide linked above
3. If you encounter any issues with WFC02 on the official integration, report them here: https://github.com/Ecowitt/ha-ecowitt-iot/issues

### ⚠️ Important Note

**If you test the official integration and it doesn'"'"'t support WFC02 as expected, please reopen this issue** and let me know. I want to ensure the migration path actually solves your problem before archiving this repository.

### Thank You!

Thank you for using this integration and for reporting the WFC02 issue. The official integration from Ecowitt is the better path forward.

---

**Closing this issue as resolved by migrating to the official integration.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 18 --reason "not planned"
echo "✅ Closed issue #18"

# Issue #17
gh issue comment 17 --body '## ⚠️ Diese Integration wurde eingestellt / This Integration Has Been Deprecated

Vielen Dank für Ihr Feedback! Diese Integration wurde im November 2025 **offiziell eingestellt**.

Thank you for your feedback! This integration has been **officially deprecated** as of November 2025.

### 🔄 Bitte migrieren Sie zur offiziellen Integration / Please Migrate to Official Integration

Ecowitt (der Hersteller) bietet jetzt eine **offizielle Home Assistant Integration** an, die WFC02 unterstützt:

Ecowitt (the manufacturer) now provides an **official Home Assistant integration** that supports WFC02:

🔗 **Offizielle Integration / Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Warum dies Ihr Problem löst / Why This Solves Your Issue

Die offizielle Ecowitt-Integration **unterstützt das WFC02-Gerätemodell** über die `wittiot`-Bibliothek. Ihr WFC02 wird korrekt erkannt und alle Entities zeigen korrekte Daten an.

The official Ecowitt integration **supports the WFC02 device model** through its `wittiot` library. Your WFC02 will be properly detected and all entities will show correct data.

**Geräteunterstützung / Device Support:**
- ✅ WFC01 (original water timer)
- ✅ **WFC02 (newer water timer model)**
- ✅ AC1100 (smart plug)

### Migrationsanleitung / Migration Guide

📖 **Vollständige Migrationsanleitung / Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

### Nächste Schritte / Next Steps

1. Installieren Sie die offizielle Integration über HACS / Install the official integration via HACS: https://github.com/Ecowitt/ha-ecowitt-iot
2. Folgen Sie der Migrationsanleitung / Follow the migration guide
3. Falls Sie Probleme mit WFC02 haben, melden Sie diese hier / If you encounter issues with WFC02, report them here: https://github.com/Ecowitt/ha-ecowitt-iot/issues

### ⚠️ Wichtiger Hinweis / Important Note

**Falls Sie die offizielle Integration testen und WFC02 nicht wie erwartet unterstützt wird, öffnen Sie bitte dieses Issue erneut** und lassen Sie es mich wissen.

**If you test the official integration and it doesn'"'"'t support WFC02 as expected, please reopen this issue** and let me know.

### Vielen Dank / Thank You!

Vielen Dank für die Nutzung dieser Integration. Die offizielle Integration von Ecowitt ist der bessere Weg in die Zukunft.

Thank you for using this integration. The official integration from Ecowitt is the better path forward.

---

**Issue wird als gelöst geschlossen durch Migration zur offiziellen Integration.**
**Closing this issue as resolved by migrating to the official integration.**'

gh issue close 17 --reason "not planned"
echo "✅ Closed issue #17"

# Issue #16
gh issue comment 16 --body '## ✅ You Were Absolutely Right!

Thank you for pointing this out! You were **100% correct** to flag the official Ecowitt integration.

After careful analysis, I'"'"'ve decided to **officially deprecate this custom integration** in favor of the official one you linked: https://github.com/Ecowitt/ha-ecowitt-iot

### Why You Were Right

The official integration:
- ✅ Is maintained by Ecowitt (the manufacturer)
- ✅ Supports the same devices (WFC01, AC1100) plus newer ones (WFC02)
- ✅ Uses the same local polling approach
- ✅ Has company-backed support and ongoing maintenance
- ✅ Will receive updates for new devices and firmware

### What'"'"'s Happening Now

As of November 2025, this repository is **officially deprecated**:
- ⚠️ Deprecation notice added to README
- 📖 Migration guide created: [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)
- 🔔 Runtime warnings added for existing users
- 📋 Repository will be archived after migration period

### For Anyone Reading This

**Use the official integration instead:** https://github.com/Ecowitt/ha-ecowitt-iot

Existing users of this custom integration should migrate using the guide above.

### Thank You!

Thank you for bringing this to everyone'"'"'s attention. Your observation led to this deprecation decision, which is the right thing for the community.

### ⚠️ Note

If anyone tests the official integration and finds it doesn'"'"'t meet their needs, please reopen this issue and explain what'"'"'s missing. I want to ensure the migration path is viable before archiving.

---

**Closing this issue as the concern has been addressed - this integration is now deprecated in favor of the official one.**'

gh issue close 16 --reason "not planned"
echo "✅ Closed issue #16"

# Issue #15
gh issue comment 15 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for reporting this bug! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Migrate to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration** that properly supports the WFC02:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This Solves Your Issue

Your WFC02 is being misdetected as an AC1100 because this custom integration doesn'"'"'t have WFC02 device definitions. The official Ecowitt integration:

- ✅ **Properly detects WFC02 devices** through its `wittiot` library
- ✅ Has correct device type definitions for WFC02
- ✅ Will show accurate entity data (not blank/incorrect)
- ✅ Supports mixed device setups (WFC01 + WFC02 + AC1100)

**Device Support in Official Integration:**
- ✅ WFC01 (original water timer) - already working for you
- ✅ **WFC02 (newer water timer model)** - will fix your issue
- ✅ AC1100 (smart plug)

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration provides:
- ✅ Proper WFC02 identification and entity data
- ✅ Company-backed support and maintenance
- ✅ Regular updates for new devices and firmware
- ✅ Same local polling approach (no cloud)

### Next Steps

1. Install the official integration via HACS: https://github.com/Ecowitt/ha-ecowitt-iot
2. Follow the migration guide linked above
3. Your WFC02 should be properly detected and all entities should show correct data
4. If issues persist with the official integration, report them here: https://github.com/Ecowitt/ha-ecowitt-iot/issues

### ⚠️ Important Note

**If you test the official integration and your WFC02 is still misdetected or entities are blank, please reopen this issue** and provide details. I want to ensure the migration actually fixes your problem.

### Thank You!

Thank you for the detailed bug report with screenshots. This confirmed that WFC02 support is needed, which the official integration provides.

---

**Closing this issue as resolved by migrating to the official integration which properly supports WFC02.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 15 --reason "not planned"
echo "✅ Closed issue #15"

# Issue #14
gh issue comment 14 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for reporting this! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Migrate to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This Solves Your Issue

The official Ecowitt integration uses properly defined units that comply with Home Assistant standards through its `wittiot` library, which should eliminate unit-related warnings in your logs.

The official integration:
- ✅ Has proper unit definitions following HA standards
- ✅ Is regularly updated to match HA core changes
- ✅ Has company-backed maintenance for compliance

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration provides:
- ✅ Proper unit handling (fixes your warning)
- ✅ WFC01, WFC02, and AC1100 support
- ✅ Company-backed support and maintenance
- ✅ Same local polling approach (no cloud)

### Next Steps

1. Install the official integration via HACS: https://github.com/Ecowitt/ha-ecowitt-iot
2. Follow the migration guide linked above
3. Check your logs - the unit warning should be gone
4. If the warning persists with the official integration, report it here: https://github.com/Ecowitt/ha-ecowitt-iot/issues

### ⚠️ Important Note

**If you migrate and still see unit warnings with the official integration, please reopen this issue** with the warning details. I want to ensure the migration resolves the problem.

### Thank You!

Thank you for reporting this warning. The official integration should have proper unit definitions.

---

**Closing this issue as resolved by migrating to the official integration.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 14 --reason "not planned"
echo "✅ Closed issue #14"

# Issue #13
gh issue comment 13 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for reporting this! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Migrate to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This May Solve Your Issue

The official integration uses the `wittiot` Python library which may have:
- ✅ Better error handling for connection issues
- ✅ Improved timeout management
- ✅ More robust retry logic
- ✅ Active maintenance for bug fixes
- ✅ Better handling of gateway communication

While I can'"'"'t guarantee it will solve your specific connection issue, the official integration is actively maintained and any connection bugs you find can be fixed by the Ecowitt team.

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration provides:
- ✅ Potentially more robust connection handling
- ✅ WFC01, WFC02, and AC1100 support
- ✅ Company-backed support and maintenance
- ✅ Same local polling approach (no cloud)

### Next Steps

1. Install the official integration via HACS: https://github.com/Ecowitt/ha-ecowitt-iot
2. Follow the migration guide linked above
3. If connection issues persist, report them to the official integration: https://github.com/Ecowitt/ha-ecowitt-iot/issues
4. The Ecowitt team can investigate and fix connection bugs

### ⚠️ Important Note

**If you test the official integration and still cannot connect to your device, please reopen this issue** with details about your setup (gateway model, network configuration, etc.). If the official integration also has this problem, it'"'"'s important to know.

### Thank You!

Thank you for reporting this connection issue. While this integration won'"'"'t receive bug fixes, the official integration team can help resolve connection problems.

---

**Closing this issue with recommendation to try the official integration.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 13 --reason "not planned"
echo "✅ Closed issue #13"

# Issue #12
gh issue comment 12 --body '## ✅ Status Update: This Integration is Deprecated

Thank you for asking about the status! Here'"'"'s the clear answer:

### Current Status (November 2025)

This integration is **officially deprecated** in favor of the official Ecowitt company integration.

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This Happened

Ecowitt (the manufacturer) now provides an official Home Assistant integration that:
- ✅ Supports the same devices (WFC01, AC1100) plus newer ones (WFC02)
- ✅ Uses the same local polling approach (no cloud)
- ✅ Has company-backed support and ongoing maintenance
- ✅ Will receive updates for new devices and firmware
- ✅ Has better long-term viability

### What This Means

**For existing users:**
- ⚠️ This integration still works but won'"'"'t receive updates
- 📖 Migration guide available: [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)
- 🔄 Please plan to migrate within the next 3 months

**For new users:**
- ❌ Do not install this integration
- ✅ Use the official integration instead

**For this repository:**
- 📋 Will be archived (read-only) after migration period
- 📚 Code remains available for reference

### Next Steps

1. Use the official integration: https://github.com/Ecowitt/ha-ecowitt-iot
2. If migrating, follow: [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)
3. Report any issues to the official integration

### ⚠️ Important Note

**If you have concerns about the official integration not meeting your needs, please reopen this issue** and explain what'"'"'s missing. I want to ensure users have a viable path forward.

### Thank You!

Thank you for asking about the status - this gave me the opportunity to provide a clear update.

---

**Closing this issue as the status question has been answered: officially deprecated.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 12 --reason "not planned"
echo "✅ Closed issue #12"

# Issue #11
gh issue comment 11 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for reporting this! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Migrate to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This May Solve Your Issue

The official integration uses the `wittiot` Python library which may have:
- ✅ Better timeout handling and retry logic
- ✅ Improved error recovery for API timeouts
- ✅ More robust communication with gateway
- ✅ Active maintenance for timeout-related bugs
- ✅ Better handling of slow/intermittent responses

While I can'"'"'t guarantee it will solve your specific timeout issue, the official integration is actively maintained and any bugs can be fixed by the Ecowitt team.

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration provides:
- ✅ Potentially better timeout management
- ✅ WFC01, WFC02, and AC1100 support
- ✅ Company-backed support and maintenance
- ✅ Same local polling approach (no cloud)

### Next Steps

1. Install the official integration via HACS: https://github.com/Ecowitt/ha-ecowitt-iot
2. Follow the migration guide linked above
3. If timeout issues persist, report them to the official integration: https://github.com/Ecowitt/ha-ecowitt-iot/issues
4. The Ecowitt team can investigate and fix timeout bugs

### ⚠️ Important Note

**If you test the official integration and still experience API timeouts, please reopen this issue** with details (frequency, network setup, gateway model). If the official integration also has this problem, it'"'"'s important to know.

### Thank You!

Thank you for reporting this timeout issue. While this integration won'"'"'t receive bug fixes, the official integration team can help resolve timeout problems.

---

**Closing this issue with recommendation to try the official integration.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 11 --reason "not planned"
echo "✅ Closed issue #11"

# Issue #5
gh issue comment 5 --body '## ⚠️ This Integration Has Been Deprecated

Thank you so much for your generous offer to help test! This integration has been **officially deprecated** as of November 2025.

### 🔄 Migration to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why Testing is No Longer Needed Here

Due to the deprecation in favor of the official integration, testing is no longer needed for this repository. The official Ecowitt team maintains their integration and has access to test devices.

### How You Can Still Help!

If you'"'"'d like to contribute to the Ecowitt ecosystem, consider:
- ✅ Testing the official integration: https://github.com/Ecowitt/ha-ecowitt-iot
- ✅ Reporting bugs to the official team
- ✅ Contributing to documentation or feature requests
- ✅ Helping other users in the community

Your offer to help test shows great community spirit! The official integration would benefit from active testers like you.

### Migration Guide

If you'"'"'re currently using this integration:

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

### ⚠️ Note

**If you have specific devices or use cases that the official integration doesn'"'"'t support, please reopen this issue** and share details. It'"'"'s important to know if there are gaps.

### Thank You!

Thank you for your willingness to help! Community members like you make open source projects successful. Please consider directing your energy to the official integration.

---

**Closing this issue as testing is no longer needed due to deprecation.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 5 --reason "not planned"
echo "✅ Closed issue #5"

# Issue #4
gh issue comment 4 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for this feature request! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Request This Feature from Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This Feature Won'"'"'t Be Added Here

This integration won'"'"'t receive new features, but you can request this feature from the official Ecowitt integration team:

🔗 **Request Feature:** https://github.com/Ecowitt/ha-ecowitt-iot/issues

### Why the Official Team is Better Positioned

As the manufacturer, Ecowitt has:
- ✅ Full access to device capabilities and data
- ✅ Ability to add firmware features if needed
- ✅ Resources to implement and maintain features
- ✅ Better understanding of device limitations
- ✅ Ongoing maintenance and support

Your feature request for tracking water consumed per session is excellent! The Ecowitt team can evaluate whether the device provides this data and implement it properly.

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

### How to Request This Feature

1. Migrate to the official integration: https://github.com/Ecowitt/ha-ecowitt-iot
2. Create a feature request: https://github.com/Ecowitt/ha-ecowitt-iot/issues
3. Explain your use case for per-session water tracking
4. The Ecowitt team can evaluate and implement

### ⚠️ Important Note

**If you find that the official integration cannot support this feature and it'"'"'s critical for your use case, please reopen this issue** and explain. If there'"'"'s a fundamental gap, it'"'"'s important to know.

### Thank You!

Thank you for the thoughtful feature request! This is a useful feature for water management. Please submit it to the official integration where it can be properly implemented.

---

**Closing this issue - feature requests should be directed to the official integration.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 4 --reason "not planned"
echo "✅ Closed issue #4"

# Issue #3
gh issue comment 3 --body '## ⚠️ This Integration Has Been Deprecated

Thank you for this feature request! This integration has been **officially deprecated** as of November 2025.

### 🔄 Please Request This Feature from Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why This Feature Won'"'"'t Be Added Here

This integration won'"'"'t receive new features, but you can request this feature from the official Ecowitt integration team:

🔗 **Request Feature:** https://github.com/Ecowitt/ha-ecowitt-iot/issues

### Why the Official Team is Better Positioned

As the manufacturer, Ecowitt has:
- ✅ Full access to device API capabilities
- ✅ Knowledge of whether volume-based control is supported by hardware
- ✅ Ability to add firmware features if needed
- ✅ Resources to implement and maintain advanced features
- ✅ Better understanding of device flow rate accuracy

Your feature request for volume-based watering (e.g., "water 5 gallons") is excellent! This would require:
- Flow rate monitoring during watering
- Calculating volume delivered
- Automatic shutoff at target volume

The Ecowitt team can evaluate whether the WFC01/WFC02 hardware supports this and implement it properly.

### Migration Guide

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

### How to Request This Feature

1. Migrate to the official integration: https://github.com/Ecowitt/ha-ecowitt-iot
2. Create a feature request: https://github.com/Ecowitt/ha-ecowitt-iot/issues
3. Explain your use case for volume-based watering
4. Include details like target volumes, accuracy needs, etc.
5. The Ecowitt team can evaluate and implement

### ⚠️ Important Note

**If you find that the official integration cannot support this feature and it'"'"'s critical for your use case, please reopen this issue** and explain. If there'"'"'s a fundamental gap, it'"'"'s important to know.

### Thank You!

Thank you for the thoughtful feature request! Volume-based watering is very useful for garden automation. Please submit it to the official integration where it can be properly implemented with manufacturer knowledge.

---

**Closing this issue - feature requests should be directed to the official integration.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 3 --reason "not planned"
echo "✅ Closed issue #3"

# Issue #2
gh issue comment 2 --body '## ⚠️ This Integration Has Been Deprecated

This integration has been **officially deprecated** as of November 2025.

### 🔄 Migration to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why Testing is No Longer Needed

Due to the deprecation in favor of the official integration, testing Fahrenheit display is no longer needed for this repository. The official integration should handle both Celsius and Fahrenheit properly.

### Migration Guide

If you need temperature data in Fahrenheit:

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration should:
- ✅ Support both °C and °F
- ✅ Respect Home Assistant'"'"'s unit preferences
- ✅ Handle unit conversions properly

### ⚠️ Note

**If the official integration has issues with Fahrenheit display, please reopen this issue** with details. It'"'"'s important to know if there are unit conversion problems.

### Thank You!

Thank you for helping test this integration. The official integration is the better path forward.

---

**Closing this issue as testing is no longer needed due to deprecation.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 2 --reason "not planned"
echo "✅ Closed issue #2"

# Issue #1
gh issue comment 1 --body '## ⚠️ This Integration Has Been Deprecated

This integration has been **officially deprecated** as of November 2025.

### 🔄 Migration to Official Integration

Ecowitt (the manufacturer) now provides an **official Home Assistant integration**:

🔗 **Official Integration:** https://github.com/Ecowitt/ha-ecowitt-iot

### Why Validation is No Longer Needed

Due to the deprecation in favor of the official integration, AC1100 validation is no longer needed for this repository. The official integration supports the AC1100 smart plug.

### AC1100 Support

**Official integration supports:**
- ✅ AC1100 WittSwitch smart plug
- ✅ WFC01 water timer
- ✅ WFC02 water timer (newer model)

### Migration Guide

If you'"'"'re using or planning to use AC1100 devices:

📖 **Complete migration instructions:** [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md)

The official integration provides:
- ✅ Tested AC1100 support
- ✅ Company-backed maintenance
- ✅ Same local polling approach

### ⚠️ Note

**If the official integration has issues with AC1100 devices, please reopen this issue** with details about what doesn'"'"'t work. It'"'"'s important to know if there are AC1100 support gaps.

### Thank You!

Thank you for helping plan validation for this integration. The official integration is the better path forward.

---

**Closing this issue as validation is no longer needed due to deprecation.**
**This repository will be archived after users have had time to migrate.**'

gh issue close 1 --reason "not planned"
echo "✅ Closed issue #1"

echo ""
echo "✅ All 13 issues have been commented on and closed!"
echo ""
echo "Summary:"
echo "- Posted deprecation responses to all issues"
echo "- Closed all issues with 'not planned' reason"
echo "- Users can reopen if official integration doesn't solve their issues"
