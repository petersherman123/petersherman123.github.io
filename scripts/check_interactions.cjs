#!/usr/bin/env node
// Exercise UI behavior in a small DOM harness; does not access a browser or clipboard.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/site.js'), 'utf8');
const papers = JSON.parse(fs.readFileSync(path.join(root, 'data/publications.json'), 'utf8'));

class Element {
  constructor(dataset = {}) {
    this.dataset = dataset;
    this.value = '';
    this.textContent = '';
    this.hidden = false;
    this.attributes = {};
    this.listeners = {};
    this.classList = {add() {}, remove() {}, toggle() {}};
  }
  addEventListener(event, fn) { this.listeners[event] = fn; }
  setAttribute(name, value) { this.attributes[name] = value; }
  getAttribute(name) { return this.attributes[name]; }
  focus() { this.focused = true; }
  querySelector() { return this.count; }
  async fire(event) { await this.listeners[event]({}); }
}

function loadPage({library = false, clipboard} = {}) {
  const selectors = new Map();
  const add = (key, value = new Element()) => (selectors.set(key, value), value);
  add('.menu-toggle'); add('#site-nav');
  const rows = papers.map(p => new Element({
    type: p.type, topic: p.topic,
    search: [p.title, p.authors, p.venue, p.year, p.topic, p.type].join(' ').toLowerCase()
  }));
  const filters = ['', 'Journal article', 'Conference abstract', 'Preprint'].map(type => {
    const button = new Element({filter: type, filterLabel: type || 'All'});
    button.count = new Element();
    return button;
  });
  if (library) {
    ['#publication-search', '.publication-controls', '#publication-topic', '.publication-count', '.no-results', '#reset-filters'].forEach(key => add(key));
  } else {
    add('#copy-email'); add('#copy-email-status');
    add('#contact-email-text').textContent = 'petersherman@g.harvard.edu';
  }
  let selected;
  const selection = {removeAllRanges() {}, addRange(range) { selected = range.target; }};
  const timers = [];
  const document = {
    documentElement: new Element(),
    querySelector: key => selectors.get(key) || null,
    querySelectorAll: key => key === '[data-filter]' ? filters : rows,
    addEventListener() {},
    createRange: () => ({selectNodeContents(target) { this.target = target; }})
  };
  vm.runInNewContext(source, {
    document, navigator: {clipboard},
    window: {matchMedia: () => ({addEventListener() {}}), getSelection: () => selection},
    setTimeout: fn => timers.push(fn), clearTimeout() {}
  });
  return {get: key => selectors.get(key), rows, filters, timers, selected: () => selected};
}

(async () => {
  const page = loadPage({library: true});
  const counts = () => page.filters.map(f => Number(f.count.textContent));
  const visible = () => page.rows.filter(r => !r.hidden).length;
  assert.deepEqual(counts(), [20, 17, 2, 1]);
  await page.filters[1].fire('click');
  assert.equal(visible(), 17);
  assert.deepEqual(counts(), [20, 17, 2, 1], 'Counts show available alternatives, not just the selected type');
  page.get('#publication-search').value = '2025';
  await page.get('#publication-search').fire('input');
  assert.deepEqual(counts(), [2, 1, 1, 0]);
  assert.equal(visible(), 1);
  page.get('#publication-topic').value = 'Geospatial ML';
  await page.get('#publication-topic').fire('change');
  assert.deepEqual(counts(), [1, 0, 1, 0]);
  assert.equal(visible(), 0);
  assert.equal(page.get('.no-results').hidden, false);
  await page.filters[2].fire('click');
  assert.equal(visible(), 1);
  await page.get('#reset-filters').fire('click');
  assert.equal(visible(), 20);
  assert.deepEqual(counts(), [20, 17, 2, 1]);
  assert.equal(page.get('#publication-search').focused, true);

  let copied;
  const success = loadPage({clipboard: {writeText: async text => { copied = text; }}});
  await success.get('#copy-email').fire('click');
  assert.equal(copied, 'petersherman@g.harvard.edu');
  assert.equal(success.get('#copy-email').textContent, 'Copied');
  assert.equal(success.get('#copy-email-status').textContent, 'Email address copied.');
  assert.equal(success.get('#copy-email').disabled, false);
  success.timers[0]();
  assert.equal(success.get('#copy-email').textContent, 'Copy email');
  for (const clipboard of [undefined, {writeText: async () => { throw new Error('Permission denied'); }}]) {
    const failure = loadPage({clipboard});
    await failure.get('#copy-email').fire('click');
    assert.equal(failure.selected(), failure.get('#contact-email-text'));
    assert.match(failure.get('#copy-email-status').textContent, /Email selected/);
    assert.equal(failure.get('#copy-email').disabled, false);
  }
  console.log('PASS: filter counts, combined filters, reset, and copy-email success/denial/unavailable behavior.');
})().catch(error => { console.error(error); process.exitCode = 1; });
