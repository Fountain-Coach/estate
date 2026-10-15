#!/usr/bin/env python3
"""Negative-space and ownership assertions for the complete estate contract."""
import gzip
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'inventory'
load=lambda n:json.loads((DIR/n).read_text())
owners=load('domain-ownership.json')
routes=load('source-routes.json')
relationships=load('estate-relations.json')
witness=load('public-readback.json')
with gzip.open(DIR/'navigation-edges.json.gz','rb') as stream:
    edges=json.load(stream)
hosts={x['host']:x for x in owners['domains']}
repos={x['repository']:x for x in owners['sources']}
assert len(hosts)==owners['counts']['hosts']==11
assert len(repos)==owners['counts']['sourceRepositories']==11
assert len(routes)==owners['counts']['gitHTMLRoutes']>=300
assert len(edges)==owners['counts']['gitNavigationEdges']>30000
assert 'fountain.coach' in hosts and 'governance.fountain.coach' in hosts
assert hosts['teatro.fountain.coach']['role']=='authoring-and-performance-instrument-not-publication'
assert hosts['solstice.fountain.coach']['lifecycle']=='planned'
assert hosts['tennis.fountain.coach']['lifecycle']=='archived'
assert hosts['works.benedikt-eickhoff.de']['sourceRepo']=='Fountain-Coach/works-benedikt-eickhoff'
assert hosts['works.benedikt-eickhoff.de']['delegations'][0]['sourceRepo']=='Fountain-Coach/solstice.fountain.coach'
assert repos['Fountain-Coach/midi2']['sourceRoot'] is None
assert len([x for x in routes if x['host']=='governance.fountain.coach'])>=150
assert len([x for x in routes if x['host']=='fountain.coach' and x['route']=='/'])==1
assert any(x for x in routes if x['host']=='works.benedikt-eickhoff.de'
           and x['route']=='/solstice/editions/first-reading/'
           and x['owner']=='Fountain-Coach/solstice.fountain.coach')
assert any(x for x in routes if x['host']=='works.benedikt-eickhoff.de'
           and x['route']=='/' and x['owner']=='Fountain-Coach/works-benedikt-eickhoff')
assert any(x for x in edges if x['host']=='works.benedikt-eickhoff.de'
           and x['fromRoute'].startswith('/solstice/'))
assert len(set((x['host'],x['route']) for x in routes))==len(routes)
assert all(x['repository'].startswith('Fountain-Coach/') for x in owners['sources'])
assert all(x['sourceInventoryStatus']!='mismatch' for x in owners['sources'])
assert any(x['fromHost']=='fountain.coach' for x in relationships)
assert witness['schema']=='fountain.estate.public-readback.v1'
byhost={x['host']:x for x in witness['domains']}
assert set(byhost)==set(hosts)
assert not byhost['tennis.fountain.coach']['checks']
assert len(byhost['fountain.coach']['checks'])>=1
fountain=byhost['fountain.coach']['checks'][0]
assert fountain['route']=='/' and fountain['sourceSHA256']
assert isinstance(fountain.get('sameBytesAsCurrentSource'),bool)
assert isinstance(fountain.get('publicEstateLinksMissingFromSource'),list)
# A successful HTTP code alone cannot prove source/publication equivalence.
for row in witness['domains']:
    for checked in row['checks']:
        if checked.get('sameBytesAsCurrentSource') is True:
            assert checked.get('sourceSHA256')==checked.get('sha256')
print('ESTATE_CONTRACT_VERIFIED',len(hosts),'hosts',len(repos),'owners',len(routes),'routes',len(edges),'edges')
