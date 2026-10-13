/* Browser/Node implementation of the educational Von Neumann extractor. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.QRNG = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const MAX_BITS = 1000000;
  function parseBits(text) {
    if (typeof text !== "string") throw new Error("Input must be text containing binary outcomes.");
    if (text.length > MAX_BITS * 4) throw new Error("Input exceeds the supported file size.");
    if (/[^01\s,;|]/u.test(text)) throw new Error("Only 0, 1 and optional separators (whitespace, comma, semicolon, |) are accepted.");
    const bits = text.replace(/[\s,;|]/gu, "");
    if (bits.length < 2) throw new Error("Enter at least two binary observations.");
    if (bits.length > MAX_BITS) throw new Error("Maximum: 1,000,000 binary observations.");
    return bits;
  }
  function stats(bits) {
    const n = bits.length;
    if (!n) return { length: 0, ones: 0, fraction_ones: null, empirical_min_entropy_bits_per_symbol: null };
    let ones = 0;
    for (let i = 0; i < n; i++) if (bits[i] === "1") ones++;
    const p = ones / n;
    return { length: n, ones, fraction_ones: p, empirical_min_entropy_bits_per_symbol: -Math.log2(Math.max(p, 1 - p)) };
  }
  function extractBits(text) {
    const bits = parseBits(text);
    const output = [];
    let discarded = 0;
    for (let i = 0; i + 1 < bits.length; i += 2) {
      if (bits[i] === "0" && bits[i + 1] === "1") output.push("0");
      else if (bits[i] === "1" && bits[i + 1] === "0") output.push("1");
      else discarded++;
    }
    const out = output.join("");
    return {
      method: "von_neumann",
      input: stats(bits),
      output: stats(out),
      output_bits: out,
      pairs_examined: Math.floor(bits.length / 2),
      pairs_discarded: discarded,
      trailing_bits_unused: bits.length % 2,
      assumptions: "Independent and identically distributed Bernoulli input bits; bias correction is not source certification."
    };
  }
  return { MAX_BITS, parseBits, extractBits };
});
