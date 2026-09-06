import { it, expect } from 'vitest';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { randomBytes } from 'node:crypto';
import { auditBudget } from '../../scripts/check_memoria_gobernada_assets.mjs';

it('counts dynamic imports and CSS instead of rewarding a small entry', () => {
  const dir = mkdtempSync(join(tmpdir(), 'bundle-budget-'));
  try {
    const manifest = { main: { isEntry: true, file: 'main.js', css: ['style.css'], dynamicImports: ['chunk'] }, chunk: { file: 'chunk.js' } };
    writeFileSync(join(dir, 'manifest.json'), JSON.stringify(manifest));
    writeFileSync(join(dir, 'main.js'), 'export const value=1;');
    writeFileSync(join(dir, 'style.css'), 'body{color:white}');
    writeFileSync(join(dir, 'chunk.js'), 'small');
    expect(auditBudget(dir, 1000).files).toBe(3);
    writeFileSync(join(dir, 'chunk.js'), randomBytes(2000));
    expect(() => auditBudget(dir, 1000)).toThrow(/presupuesto/);
    writeFileSync(join(dir, 'chunk.js'), 'small');
    expect(auditBudget(dir, 1000).files).toBe(3);
    writeFileSync(join(dir, 'manifest.json'), '{}');
    expect(() => auditBudget(dir, 1000)).toThrow(/entrada/);
    writeFileSync(join(dir, 'manifest.json'), JSON.stringify({ main: manifest.main }));
    expect(() => auditBudget(dir, 1000)).toThrow(/Import ausente/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
