/**
 * ELEMENTARY CODE — LIVE 稼働時計（東京基準）
 * 逆回転角度は iOS `ElementaryTwelveHourClockModule.reverseRotationDegrees` と同型。
 * 100分の1秒表示は `ElementaryCentisecondModule` と同型（端末 ms → 0…99）。
 * 本番 elementarycode.tokyo では ?ecConfirmLive=1 または localhost / preview のみ連続更新。
 */
(function (global) {
  "use strict";

  var DEFAULT_TZ = "Asia/Tokyo";
  var COMIC_TICK_MS = 10;

  function isConfirmEnvironment() {
    var host = global.location && global.location.hostname;
    if (host === "localhost" || host === "127.0.0.1") return true;
    var params = new URLSearchParams(global.location.search || "");
    if (params.get("ecConfirmLive") === "1") return true;
    if ((global.location.pathname || "").indexOf("/preview/") !== -1) return true;
    return false;
  }

  function partsInTimeZone(date, timeZone) {
    var fmt = new Intl.DateTimeFormat("en-US", {
      timeZone: timeZone,
      hour12: false,
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
    });
    var map = { hour: 0, minute: 0, second: 0 };
    fmt.formatToParts(date).forEach(function (p) {
      if (p.type in map) map[p.type] = parseInt(p.value, 10) || 0;
    });
    return map;
  }

  /** 東京（任意 TZ）· HH:MM:SS.XX（100分の1秒・2桁） */
  function digitalCentisecondInTimeZone(date, timeZone) {
    timeZone = timeZone || DEFAULT_TZ;
    try {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: timeZone,
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        fractionalSecondDigits: 2,
      }).formatToParts(date);
      var h;
      var m;
      var s;
      var frac = "00";
      parts.forEach(function (p) {
        if (p.type === "hour") h = p.value;
        if (p.type === "minute") m = p.value;
        if (p.type === "second") s = p.value;
        if (p.type === "fractionalSecond") {
          frac = p.value.length >= 2 ? p.value.slice(0, 2) : p.value.padStart(2, "0");
        }
      });
      if (h !== undefined && m !== undefined && s !== undefined) {
        return h + ":" + m + ":" + s + "." + frac;
      }
    } catch (e) {
      /* fractionalSecondDigits 未対応 */
    }
    var p = partsInTimeZone(date, timeZone);
    var h2 = String(p.hour).padStart(2, "0");
    var m2 = String(p.minute).padStart(2, "0");
    var s2 = String(p.second).padStart(2, "0");
    var fractional = date.getTime() % 1000;
    if (fractional < 0) fractional += 1000;
    var cs = String(Math.min(99, Math.floor(fractional / 10))).padStart(2, "0");
    return h2 + ":" + m2 + ":" + s2 + "." + cs;
  }

  /** @returns {{ hour12:number, minute:number, second:number, reverseHourDeg:number, reverseMinuteDeg:number, digital:string }} */
  function tokyoLiveReading(date) {
    return readingForTimeZone(date, DEFAULT_TZ);
  }

  function readingForTimeZone(date, timeZone) {
    var p = partsInTimeZone(date, timeZone);
    var hour24 = p.hour;
    var minute = p.minute;
    var second = p.second;
    var hour12 = hour24 % 12;
    if (hour12 === 0) hour12 = 12;

    var hourOnDial = hour12 % 12;
    var forwardHour =
      (hourOnDial / 12) * 360 +
      (minute / 60) * 30 +
      (second / 60) * 0.5;
    var reverseHour = normalizeDeg(360 - forwardHour);

    var forwardMinute = (minute / 60) * 360 + (second / 60) * 6;
    var reverseMinute = normalizeDeg(360 - forwardMinute);

    var digital = new Intl.DateTimeFormat("ja-JP", {
      timeZone: timeZone,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    }).format(date);

    return {
      hour12: hour12,
      minute: minute,
      second: second,
      reverseHourDeg: reverseHour,
      reverseMinuteDeg: reverseMinute,
      digital: digital,
    };
  }

  function normalizeDeg(deg) {
    var r = deg % 360;
    return r < 0 ? r + 360 : r;
  }

  function applyHands(clockEl, reading) {
    if (!clockEl) return;
    var hour = clockEl.querySelector(".hand-hour");
    var minute = clockEl.querySelector(".hand-minute");
    if (hour) {
      hour.style.animation = "none";
      hour.style.transform = "rotate(" + (180 + reading.reverseHourDeg) + "deg)";
    }
    if (minute) {
      minute.style.animation = "none";
      minute.style.transform = "rotate(" + (180 + reading.reverseMinuteDeg) + "deg)";
    }
    clockEl.classList.add("is-live");
  }

  function mountDigitalLabel(clockEl, text) {
    if (!clockEl) return;
    var wrap = clockEl.closest(".clock-wrap") || clockEl.parentElement;
    if (!wrap) return;
    var el = wrap.querySelector(".ec-live-digital");
    if (!el) {
      el = document.createElement("p");
      el.className = "ec-live-digital";
      el.setAttribute("aria-live", "polite");
      wrap.appendChild(el);
    }
    el.textContent = "LIVE · 東京 " + text;
  }

  function applyComicDigital(el, text) {
    if (!el) return;
    var dot = text.lastIndexOf(".");
    if (dot < 0) {
      el.textContent = text;
      return;
    }
    el.innerHTML =
      '<span class="ec-comic-digital-main">' +
      text.slice(0, dot + 1) +
      '</span><span class="ec-comic-digital-frac">' +
      text.slice(dot + 1) +
      "</span>";
    el.classList.add("is-live");
  }

  var timers = [];

  function startLiveClock(clockEl, options) {
    if (!clockEl) return function () {};
    var timeZone = (options && options.timeZone) || DEFAULT_TZ;
    var showDigital = !options || options.showDigital !== false;

    function tick() {
      var reading = readingForTimeZone(new Date(), timeZone);
      applyHands(clockEl, reading);
      if (showDigital) mountDigitalLabel(clockEl, reading.digital);
    }

    tick();
    var id = global.setInterval(tick, 1000);
    timers.push(id);
    return function stop() {
      global.clearInterval(id);
    };
  }

  /** 8コマ第2コマ PC 内デジタル（100分の1秒 · 10ms 更新） */
  function startLiveComicDigital(el, options) {
    if (!el) return function () {};
    var timeZone = (options && options.timeZone) || DEFAULT_TZ;

    function tick() {
      applyComicDigital(
        el,
        digitalCentisecondInTimeZone(new Date(), timeZone)
      );
    }

    tick();
    var id = global.setInterval(tick, COMIC_TICK_MS);
    timers.push(id);
    return function stop() {
      global.clearInterval(id);
    };
  }

  function bootDocument(options) {
    if (!isConfirmEnvironment()) return;
    var selector = (options && options.clockSelector) || "#status-clock";
    document.querySelectorAll(selector).forEach(function (el) {
      startLiveClock(el, options);
    });
    document.querySelectorAll("[data-ec-live-clock]").forEach(function (el) {
      var tz = el.getAttribute("data-ec-tz") || DEFAULT_TZ;
      startLiveClock(el, { timeZone: tz, showDigital: el.getAttribute("data-ec-digital") !== "0" });
    });
    document.querySelectorAll("[data-ec-comic-digital]").forEach(function (el) {
      var tz = el.getAttribute("data-ec-tz") || DEFAULT_TZ;
      startLiveComicDigital(el, { timeZone: tz });
    });
  }

  global.ECLiveClock = {
    isConfirmEnvironment: isConfirmEnvironment,
    tokyoLiveReading: tokyoLiveReading,
    digitalCentisecondInTimeZone: digitalCentisecondInTimeZone,
    startLiveClock: startLiveClock,
    startLiveComicDigital: startLiveComicDigital,
    bootDocument: bootDocument,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      bootDocument();
    });
  } else {
    bootDocument();
  }
})(typeof window !== "undefined" ? window : globalThis);
