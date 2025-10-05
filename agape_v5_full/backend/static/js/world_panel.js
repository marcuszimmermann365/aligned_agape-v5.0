
import { loadYAML } from './yaml_loader.js';

async function fetchJSON(url) {
  const r = await fetch(url, { cache: 'no-store' });
  if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
  return r.json();
}

async function fetchCatalog() {
  try {
    const text = await fetch('/api/world/catalog', { cache:'no-store' }).then(r => r.text());
    return loadYAML(text);
  } catch {
    return {};
  }
}

function classifyFreshness(asof, freshnessDays=365) {
  try {
    const t = new Date(asof + 'T00:00:00Z').getTime();
    const ageDays = (Date.now() - t) / (1000*3600*24);
    if (ageDays <= freshnessDays * 1.2) return { cls:'fresh', label:`~${Math.round(ageDays)}d alt` };
    if (ageDays <= freshnessDays * 2.5) return { cls:'stale', label:`~${Math.round(ageDays)}d alt` };
    return { cls:'ancient', label:`~${Math.round(ageDays)}d alt` };
  } catch {
    return { cls:'stale', label:'n/a' };
  }
}

function renderGWS(gws) {
  const el = document.getElementById('gws-badge');
  el.className = 'badge';
  el.textContent = `GWS: ${Number(gws).toFixed(3)}`;
}

function renderTable(state, catalog) {
  const tbody = document.querySelector('#proxy-table tbody');
  tbody.innerHTML = '';

  const sources = catalog?.sources || {};
  const alpha = catalog?.smoothing?.alpha_daily;
  const updatedEvery = catalog?.updated_every || 'daily';

  for (const J of Object.keys(state.proxies).sort()) {
    const group = state.proxies[J];
    for (const proxyName of Object.keys(group)) {
      const p = group[proxyName];
      const catGroup = catalog?.[J] || {};
      const catProxy = catGroup[proxyName] || {};
      const ui = catProxy?.ui || {};
      const sourceRef = catProxy?.source_ref;
      const srcMeta = sourceRef ? sources[sourceRef] : null;

      const freshnessDays = srcMeta?.freshness_expectation_days ?? 365;
      const fres = classifyFreshness(p.asof || state.asof, freshnessDays);

      const tip = [
        ui.description || '',
        srcMeta ? `Quelle: ${srcMeta.title} — ${srcMeta.publisher}` : '',
        srcMeta?.license_name ? `Lizenz: ${srcMeta.license_name}` : '',
        srcMeta?.update_cycle ? `Update-Zyklus: ${srcMeta.update_cycle}` : '',
        `Smoothing α: ${alpha ?? '0.10'}`,
        `Katalog-Update: ${updatedEvery}`
      ].filter(Boolean).join('\n');

      const sourceLinks = [];
      if (srcMeta?.url) sourceLinks.push(`<a href="${srcMeta.url}" target="_blank" rel="noopener">Source</a>`);
      if (srcMeta?.license_url) sourceLinks.push(`<a href="${srcMeta.license_url}" target="_blank" rel="noopener">License</a>`);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${J}</td>
        <td><span class="tooltip" data-tip="${tip}">${ui.display_name || proxyName}</span></td>
        <td>${(p.norm ?? p.normalized ?? 0).toFixed(3)}</td>
        <td>${(p.value ?? p.raw?.value ?? 0)}</td>
        <td class="${fres.cls}">${p.asof || state.asof} <span class="badge">${fres.label}</span></td>
        <td><span class="source-chip">
            ${srcMeta?.publisher ? `<strong>${srcMeta.publisher}</strong>` : ''}
            ${sourceLinks.length ? '· ' + sourceLinks.join(' · ') : ''}
        </span></td>
      `;
      tbody.appendChild(tr);
    }
  }
}

function renderRadar(j) {
  const el = document.getElementById('j-radar');
  el.innerHTML = `
    <div class="badge">J1 ${j.J1.toFixed(2)}</div>
    <div class="badge">J2 ${j.J2.toFixed(2)}</div>
    <div class="badge">J3 ${j.J3.toFixed(2)}</div>
    <div class="badge">J4 ${j.J4.toFixed(2)}</div>
    <div class="badge">J5 ${j.J5.toFixed(2)}</div>
  `;
}

(async function initWorldPanel(){
  try {
    const [stateResp, catalog] = await Promise.all([
      fetchJSON('/api/world/state'),
      fetchCatalog()
    ]);
    if (!stateResp.ok) throw new Error(stateResp.error || 'world_state not ok');
    const S = stateResp.state;
    renderGWS(S.GWS);
    renderRadar(S.J);
    renderTable(S, catalog);
  } catch (e) {
    console.error('World panel init error:', e);
    const tbody = document.querySelector('#proxy-table tbody');
    if (tbody) tbody.innerHTML = `<tr><td colspan="6">Fehler beim Laden der Daten: ${String(e)}</td></tr>`;
  }
})();
