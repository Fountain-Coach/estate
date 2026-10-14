
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const m = JSON.parse(readFileSync(new URL('../manifest.json', import.meta.url)));
assert.equal(m.schema, 'fountain.estate.domain-ownership.v2');
assert.deepEqual(m.primaryNavigationIds, ['fountain-coach','first-reading','teatro']);
assert.deepEqual(m.frontDoors.map(x => x.rank), [1,2,3]);
assert.equal(m.frontDoors.length,3);
assert.equal(m.supportingDomains.length,7);
const repos=[...m.frontDoors,...m.supportingDomains].map(x=>x.sourceRepo);
assert(repos.every(r=>r.startsWith('Fountain-Coach/')));
assert.equal(new Set(repos).size,repos.length);
assert.equal(m.supportingDomains.find(x=>x.host==='status.fountain.coach').role,'mandatory-legal-footer-and-transparency');
assert.equal(m.supportingDomains.find(x=>x.host==='book.fountain.coach').status,'live-receded');
assert(m.rules.publishing.includes('HTTPS readback'));
console.log('ESTATE_VERIFIED',m.frontDoors.map(x=>x.name).join(', '),'Git owners',repos.length);
