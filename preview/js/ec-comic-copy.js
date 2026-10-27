/**
 * 8コマ漫画 · 第1・第3コマ説明（確認用のみ）
 * 公開用表示デモ：▪ を境に数字の前後を逆配置（WORLD TIME 公開表示と同型）。
 * 双子コード認証・内部計算には接続しない。
 */
(function (global) {
  "use strict";

  function reverseDigitRun(text) {
    var chars = String(text).split("");
    var i = 0;
    while (i < chars.length) {
      if (chars[i] >= "0" && chars[i] <= "9") {
        var j = i;
        while (j < chars.length && chars[j] >= "0" && chars[j] <= "9") j++;
        var block = chars.slice(i, j);
        block.reverse();
        for (var k = i; k < j; k++) chars[k] = block[k - i];
        i = j;
      } else {
        i++;
      }
    }
    return chars.join("");
  }

  /** 確認用の公開表示例（▪前後を逆配置）。認証値ではない。 */
  function publicDisplayDemoLine(date, timeZone) {
    timeZone = timeZone || "Asia/Tokyo";
    var parts = { h: 0, m: 0, s: 0, cs: "00" };
    try {
      new Intl.DateTimeFormat("en-US", {
        timeZone: timeZone,
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        fractionalSecondDigits: 2,
      })
        .formatToParts(date)
        .forEach(function (p) {
          if (p.type === "hour") parts.h = p.value;
          if (p.type === "minute") parts.m = p.value;
          if (p.type === "second") parts.s = p.value;
          if (p.type === "fractionalSecond") {
            parts.cs =
              p.value.length >= 2 ? p.value.slice(0, 2) : p.value.padStart(2, "0");
          }
        });
    } catch (e) {
      /* fallback */
    }
    var before = parts.h + parts.m;
    var after = parts.s + parts.cs;
    return reverseDigitRun(before) + "▪" + reverseDigitRun(after);
  }

  function startPublicDisplayDemo(el, options) {
    if (!el) return;
    var tz = (options && options.timeZone) || "Asia/Tokyo";
    function tick() {
      el.textContent = publicDisplayDemoLine(new Date(), tz);
    }
    tick();
    return global.setInterval(tick, 1000);
  }

  function bootDocument() {
    document.querySelectorAll("[data-ec-public-demo]").forEach(function (el) {
      var tz = el.getAttribute("data-ec-tz") || "Asia/Tokyo";
      startPublicDisplayDemo(el, { timeZone: tz });
    });
  }

  global.ECComicCopy = {
    reverseDigitRun: reverseDigitRun,
    publicDisplayDemoLine: publicDisplayDemoLine,
    startPublicDisplayDemo: startPublicDisplayDemo,
    bootDocument: bootDocument,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bootDocument);
  } else {
    bootDocument();
  }
})(typeof window !== "undefined" ? window : globalThis);
