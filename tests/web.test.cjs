const test = require('node:test');
const assert = require('node:assert/strict');
const {parseBits, extractBits, MAX_BITS} = require('../web/extractor.js');
test('known-answer vectors and bias statistic', () => {
  const r = extractBits('01 10 00 11 01');
  assert.equal(r.output_bits, '010');
  assert.equal(r.pairs_discarded, 2);
  assert.equal(r.pairs_examined, 5);
  assert.equal(r.output.fraction_ones, 1 / 3);
  assert.equal(r.input.length, 10);
});
test('odd and degenerate inputs have no invented entropy', () => {
  const r = extractBits('00001');
  assert.equal(r.trailing_bits_unused, 1);
  assert.equal(r.output.length, 0);
  assert.equal(r.output.empirical_min_entropy_bits_per_symbol, null);
});
test('strict parsing, no accidental normalization', () => {
  assert.equal(parseBits('0,1;1|0\n'), '0110');
  for (const bad of ['', '1', '0102', '0x10', 'true', '01\u200b']) {
    assert.throws(() => extractBits(bad));
  }
  assert.throws(() => extractBits('01'.repeat(Math.floor(MAX_BITS / 2) + 1)));
});
