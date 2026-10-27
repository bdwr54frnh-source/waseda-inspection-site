/**
 * WORLD TIME 折り返し（社長 2026-10-26 確定）
 * ① 国名＋時刻は分割しない ② 各国 ▪×8 ③ 行末▪は最大4・次行は5個目から
 * ④ 改行で▪を最初から出し直さない ⑤ ▪の欠落・重複・追加禁止
 * 時刻計算は呼び出し側（formatWorldTime）のまま。本モジュールはレイアウトのみ。
 */
(function (global) {
  "use strict";

  var DOT = "\u25AA";
  var DOTS_PER_COUNTRY = 8;
  var MAX_DOTS_END_LINE = 4;

  function measureFactory(font) {
    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext("2d");
    if (!ctx) {
      return function (text) {
        return String(text).length * 7;
      };
    }
    ctx.font = font;
    return function (text) {
      return ctx.measureText(String(text)).width;
    };
  }

  /**
   * @param {{ name: string, timeText: string }[]} entries
   * @param {number} containerWidth px
   * @param {function(string): number} measure
   * @returns {{ lines: { kind: "entry"|"dots", text: string, key?: string }[][], valid: boolean }}
   */
  function layoutWorldTimeStream(entries, containerWidth, measure) {
    var lines = [];
    var line = [];
    var lineWidth = 0;

    function flushLine() {
      if (line.length) lines.push(line);
      line = [];
      lineWidth = 0;
    }

    function gapWidth() {
      return line.length ? measure(" ") : 0;
    }

    function pushToken(token) {
      var g = gapWidth();
      line.push(token);
      lineWidth += g + measure(token.text);
    }

    function placeDotRun(count, key) {
      if (count <= 0) return;
      pushToken({ kind: "dots", text: DOT.repeat(count), key: key });
    }

    entries.forEach(function (entry, entryIndex) {
      var entryText = entry.name + " " + entry.timeText;
      var entryToken = { kind: "entry", text: entryText, key: "e" + entryIndex };
      var entryW = measure(entryText);
      var need = gapWidth() + entryW;
      if (line.length && lineWidth + need > containerWidth) flushLine();
      if (!line.length && entryW > containerWidth) {
        pushToken(entryToken);
      } else {
        if (line.length && lineWidth + need > containerWidth) flushLine();
        pushToken(entryToken);
      }

      var dotsLeft = DOTS_PER_COUNTRY;
      var dotKey = "d" + entryIndex;
      while (dotsLeft > 0) {
        var space = gapWidth();
        var wAll = measure(DOT.repeat(dotsLeft));
        if (lineWidth + space + wAll <= containerWidth) {
          placeDotRun(dotsLeft, dotKey);
          dotsLeft = 0;
          continue;
        }
        var chunk =
          dotsLeft > MAX_DOTS_END_LINE ? MAX_DOTS_END_LINE : dotsLeft;
        var wChunk = measure(DOT.repeat(chunk));
        if (lineWidth + space + wChunk <= containerWidth) {
          placeDotRun(chunk, dotKey);
          dotsLeft -= chunk;
          continue;
        }
        if (line.length) {
          flushLine();
          continue;
        }
        chunk = dotsLeft;
        while (chunk > MAX_DOTS_END_LINE) chunk--;
        while (chunk >= 1) {
          wChunk = measure(DOT.repeat(chunk));
          if (wChunk <= containerWidth) {
            placeDotRun(chunk, dotKey);
            dotsLeft -= chunk;
            break;
          }
          chunk--;
        }
        if (chunk < 1) {
          placeDotRun(1, dotKey);
          dotsLeft -= 1;
        }
      }
    });
    flushLine();
    return { lines: lines, valid: validateLayout(entries, lines) };
  }

  function validateLayout(entries, lines) {
    var dotCounts = entries.map(function () {
      return 0;
    });
    lines.forEach(function (row) {
      row.forEach(function (token) {
        if (token.kind !== "dots" || !token.key) return;
        var idx = parseInt(token.key.slice(1), 10);
        if (isNaN(idx) || idx < 0 || idx >= dotCounts.length) return;
        for (var i = 0; i < token.text.length; i++) {
          if (token.text.charAt(i) === DOT) dotCounts[idx]++;
        }
      });
    });
    return dotCounts.every(function (n) {
      return n === DOTS_PER_COUNTRY;
    });
  }

  function renderStream(container, layout) {
    if (!container) return;
    container.innerHTML = "";
    layout.lines.forEach(function (row) {
      var lineEl = document.createElement("div");
      lineEl.className = "wt-line";
      row.forEach(function (token, i) {
        if (i > 0) lineEl.appendChild(document.createTextNode(" "));
        var span = document.createElement("span");
        span.className = token.kind === "entry" ? "wt-entry" : "wt-dots";
        span.textContent = token.text;
        if (token.key) span.dataset.wtKey = token.key;
        lineEl.appendChild(span);
      });
      container.appendChild(lineEl);
    });
    container.dataset.wtValid = layout.valid ? "1" : "0";
  }

  /**
   * @param {HTMLElement} container
   * @param {{ name: string, tz: string }[]} rows
   * @param {function(string): string} formatWorldTime unchanged caller formatter
   */
  function paintWorldTimeStream(container, rows, formatWorldTime) {
    if (!container || !rows || !rows.length) return { valid: false };
    var cs = global.getComputedStyle(container);
    var font =
      cs.fontWeight +
      " " +
      cs.fontSize +
      " " +
      (cs.fontFamily || "sans-serif");
    var measure = measureFactory(font);
    var width = container.clientWidth || container.getBoundingClientRect().width;
    if (width < 40) width = 320;
    var entries = rows.map(function (row) {
      return {
        name: row.name,
        timeText: formatWorldTime(row.tz),
      };
    });
    var layout = layoutWorldTimeStream(entries, width, measure);
    renderStream(container, layout);
    return layout;
  }

  function updateStreamTimes(container, rows, formatWorldTime) {
    if (!container) return;
    var byKey = {};
    rows.forEach(function (row, i) {
      byKey["e" + i] = row.name + " " + formatWorldTime(row.tz);
    });
    container.querySelectorAll(".wt-entry[data-wt-key]").forEach(function (el) {
      var key = el.getAttribute("data-wt-key");
      if (key && byKey[key]) el.textContent = byKey[key];
    });
  }

  global.ECWorldTimeWrap = {
    DOT: DOT,
    DOTS_PER_COUNTRY: DOTS_PER_COUNTRY,
    layoutWorldTimeStream: layoutWorldTimeStream,
    paintWorldTimeStream: paintWorldTimeStream,
    updateStreamTimes: updateStreamTimes,
    validateLayout: validateLayout,
  };
})(typeof window !== "undefined" ? window : globalThis);
