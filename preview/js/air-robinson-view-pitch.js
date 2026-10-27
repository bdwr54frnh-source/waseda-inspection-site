/**
 * AIR ROBINSON — ロビンソンからの視線（確認用 · HP プレビュー）
 * 250m 未満: 40° 下向き · 250m 以上: 巡航高度へ向けて滑らかに水平（正面）へ。
 * iOS 正本 `AirshipAltitudeVisualPolicy`（300m 境界）は変更しない · 本 JS は確認ページ専用。
 */
(function (global) {
  "use strict";

  var BOUNDARY_M = 250;
  var DOWN_DEG = 40;
  var CRUISE_M = 920;

  function smoothstep(t) {
    var x = Math.min(1, Math.max(0, t));
    return x * x * (3 - 2 * x);
  }

  function pitchDegreesFromAltitudeMeters(altM) {
    var alt = Math.max(24, Number(altM) || 0);
    if (alt < BOUNDARY_M) return DOWN_DEG;
    var t = smoothstep((alt - BOUNDARY_M) / Math.max(1, CRUISE_M - BOUNDARY_M));
    return DOWN_DEG * (1 - t);
  }

  function applyPitchToElement(el, altM, options) {
    if (!el) return;
    var deg = pitchDegreesFromAltitudeMeters(altM);
    var transition = options && options.animate !== false;
    if (transition) {
      el.style.transition = "transform 0.85s cubic-bezier(0.4, 0, 0.2, 1)";
    } else {
      el.style.transition = "none";
    }
    el.style.transform =
      "perspective(900px) rotateX(" + (-deg).toFixed(2) + "deg) scale(1.08)";
    el.dataset.pitchDeg = String(deg.toFixed(1));
    el.dataset.altitudeM = String(Math.round(alt));
  }

  global.AirRobinsonViewPitch = {
    boundaryMeters: BOUNDARY_M,
    downPitchDegrees: DOWN_DEG,
    pitchDegreesFromAltitudeMeters: pitchDegreesFromAltitudeMeters,
    applyPitchToElement: applyPitchToElement,
  };
})(typeof window !== "undefined" ? window : globalThis);
