
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
const fc=m.frontDoors.find(x=>x.id==='fountain-coach');
assert.equal(fc.landing.path,'/editions/');
assert.equal(fc.entryEditionPath,'/editions/essays/');
assert.equal(fc.nestedEditions.length,3);
for(const edition of fc.nestedEditions){
 assert(edition.url.startsWith('https://fountain.coach/editions/essays/'));
 assert(edition.url.endsWith('/'));
}
assert.equal(fc.sourceCommit,'e8d34eb0e6317586a293052d46fcbc005efc7fd7');
assert(m.frontDoors.every(x=>typeof x.entryEditionUrl==='string'&&x.entryEditionUrl.startsWith('https://')));
assert(m.rules.rail.includes('rail points into'));
assert(m.rules.subEditions.includes('independent reading position'));
console.log('ESTATE_VERIFIED',m.frontDoors.map(x=>x.name).join(', '),'Git owners',repos.length);
