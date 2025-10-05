
export async function loadYAML(text) {
  if (window.jsyaml) { return window.jsyaml.load(text); }
  const lines = text.split(/\r?\n/);
  const out = {};
  let stack = [{ indent: -1, obj: out }];
  for (const raw of lines) {
    const line = raw.replace(/\t/g, '  ');
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const indent = (line.match(/^ */)[0] || '').length;
    while (stack.length && indent <= stack[stack.length-1].indent) stack.pop();
    const parent = stack[stack.length-1].obj;
    const m = line.trim().match(/^([^:]+):\s*(.*)$/);
    if (m) {
      const key = m[1].trim();
      const val = m[2].trim();
      if (val === '') {
        parent[key] = {};
        stack.push({ indent, obj: parent[key] });
      } else {
        parent[key] = (/^(true|false|\d+(\.\d+)?)$/i.test(val)) ? JSON.parse(val) : val;
      }
    }
  }
  return out;
}
