// ==UserScript==
// @name         Language Reactor PRO Unlocked
// @namespace    http://tampermonkey.net/
// @version      3.0
// @description  Bypass Premium/PRO features by forcing licenseStatus to FULL
// @author       ASTRO
// @match        https://www.languagereactor.com/*
// @match        https://dev.languagereactor.com/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    console.log("%c[ASTRO] VIGILANTE PROTOCOL: PATCHING LICENSE LOGIC...", "color: #ff00ff; font-weight: bold;");

    // 1. Emulate Extension Presence
    window.__LANGUAGE_REACTOR_EXTENSION__ = true;

    // 2. Intercept Object Property
    // Intercepts data as it's assigned to React/MobX state objects
    const originalObjectAssign = Object.assign;
    Object.assign = function(target, ...sources) {
        for (let source of sources) {
            if (source && (source.licenseStatus || source.proFeaturesEnabled)) {
                console.log("[ASTRO] license data detected in Object.assign, patching...");
                if (source.licenseStatus) source.licenseStatus = "FULL";
                if (typeof source.proFeaturesEnabled !== 'undefined') source.proFeaturesEnabled = true;
            }
        }
        return originalObjectAssign.apply(this, [target, ...sources]);
    };

    // 3. Persistent State Watcher
    // Scans memory every second to override any server-side updates
    setInterval(() => {
        for (let key in window) {
            try {
                if (window[key] && window[key].data && typeof window[key].data.licenseStatus !== 'undefined') {
                    if (window[key].data.licenseStatus !== "FULL") {
                        console.log(`[ASTRO] Force patching window.${key}.data.licenseStatus to FULL`);
                        window[key].data.licenseStatus = "FULL";
                    }
                }
            } catch (e) {}
        }
        
        // 4. LocalStorage Poisoning
        try {
            const storeKeys = ["userStore", "dioco_user_data", "settings"];
            storeKeys.forEach(k => {
                let data = localStorage.getItem(k);
                if (data && (data.includes("licenseStatus") || data.includes("proFeaturesEnabled"))) {
                    let obj = JSON.parse(data);
                    let changed = false;
                    if (obj.licenseStatus && obj.licenseStatus !== "FULL") {
                        obj.licenseStatus = "FULL";
                        changed = true;
                    }
                    if (obj.proFeaturesEnabled === false) {
                        obj.proFeaturesEnabled = true;
                        changed = true;
                    }
                    if (changed) {
                        localStorage.setItem(k, JSON.stringify(obj));
                        console.log(`[ASTRO] LocalStorage '${k}' patched.`);
                    }
                }
            });
        } catch (e) {}
    }, 1000);

})();
