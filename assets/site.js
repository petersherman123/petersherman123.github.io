'use strict';

// All content and navigation remain usable without JavaScript.
document.documentElement.classList.add('js');
// Preserve old mixed-case React routes on GitHub Pages' case-sensitive host.
if (document.querySelector('.not-found')) {
  const legacyPaths = {'/projects': '/publications/', '/resume': '/images/Peter_Sherman_CV.pdf', '/about': '/'};
  const target = legacyPaths[location.pathname.replace(/\/+$/, '').toLowerCase()];
  if (target) location.replace(target);
}
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#site-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});

const copyEmail = document.querySelector('#copy-email');
if (copyEmail) {
  const email = document.querySelector('#contact-email-text');
  const copyStatus = document.querySelector('#copy-email-status');
  let resetCopyLabel;
  copyEmail.hidden = false;
  copyEmail.addEventListener('click', async () => {
    clearTimeout(resetCopyLabel);
    copyEmail.disabled = true;
    copyStatus.textContent = '';
    try {
      await navigator.clipboard.writeText(email.textContent.trim());
      copyEmail.textContent = 'Copied';
      copyStatus.textContent = 'Email address copied.';
      resetCopyLabel = setTimeout(() => { copyEmail.textContent = 'Copy email'; }, 2500);
    } catch {
      copyEmail.textContent = 'Copy email';
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(email);
      selection.removeAllRanges();
      selection.addRange(range);
      copyStatus.textContent = 'Email selected. Use your keyboard or selection menu to copy it.';
    } finally {
      copyEmail.disabled = false;
    }
  });
}

const search = document.querySelector('#publication-search');
if (search) {
  const controls = document.querySelector('.publication-controls');
  const topic = document.querySelector('#publication-topic');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const rows = [...document.querySelectorAll('.publication-row')];
  const status = document.querySelector('.publication-count');
  const empty = document.querySelector('.no-results');
  let selectedType = '';
  const normalize = text => text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[’‘]/g, "'");
  function filterPublications() {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    const matchingRows = rows.filter(row => (!topic.value || row.dataset.topic === topic.value)
      && words.every(word => normalize(row.dataset.search).includes(word)));
    const matchingSet = new Set(matchingRows);
    for (const button of filters) {
      const total = matchingRows.filter(row => !button.dataset.filter || row.dataset.type === button.dataset.filter).length;
      button.querySelector('[data-filter-count]').textContent = total;
      button.setAttribute('aria-label', `${button.dataset.filterLabel}, ${total} ${total === 1 ? 'publication' : 'publications'}`);
    }
    let count = 0;
    for (const row of rows) {
      const matches = (!selectedType || row.dataset.type === selectedType)
        && matchingSet.has(row);
      row.hidden = !matches;
      if (matches) count += 1;
    }
    status.textContent = `${count} ${count === 1 ? 'publication' : 'publications'}${count === rows.length ? '' : ` of ${rows.length}`}`;
    empty.hidden = count !== 0;
  }
  controls.hidden = false;
  filterPublications();
  search.addEventListener('input', filterPublications);
  topic.addEventListener('change', filterPublications);
  filters.forEach(button => button.addEventListener('click', () => {
    selectedType = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterPublications();
  }));
  document.querySelector('#reset-filters').addEventListener('click', () => {
    search.value = '';
    topic.value = '';
    selectedType = '';
    filters.forEach(item => item.setAttribute('aria-pressed', String(!item.dataset.filter)));
    filterPublications();
    search.focus();
  });
}
