#!/usr/bin/env python3
"""Complete the public First Reading dependency graph in a local WLAN candidate.

No host mutation. Preserve the source-owned full-viewport edition and restore only
public source routes/resources, with independently fetched SHA-256 evidence.
"""
import argparse, hashlib, json, re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

PUBLIC='https://works.benedikt-eickhoff.de'
EDITION='/solstice/editions/first-reading/'
def sha(b):return hashlib.sha256(b).hexdigest()

def verify(root):
    root=Path(root)
    lock=json.loads((root/'source-lock.json').read_text())
    witness=lock['firstReadingDependencyWitness']
    for item in witness['files']:
        if 'sha256' in item and item['candidateSHA256']!=item['sha256']:
            raise ValueError('source reading bytes changed: '+item['path'])
        path=root/item['path']
        if not path.is_file() or sha(path.read_bytes())!=item['candidateSHA256']:
            raise ValueError('missing or changed reading dependency: '+item['path'])
    return len(witness['files'])

def complete(root):
    root=Path(root)
    lock=json.loads((root/'source-lock.json').read_text())
    edition=root/(EDITION.lstrip('/')+'index.html')

    queue=[PUBLIC+EDITION];seen=set();records=[];htmls=[]
    while queue:
        url=queue.pop(0)
        bits=urlsplit(url)
        url=bits._replace(query='',fragment='').geturl()
        if url in seen:continue
        seen.add(url)
        if bits.netloc!='works.benedikt-eickhoff.de' or not bits.path.startswith('/solstice/'):
            continue
        path=unquote(bits.path)
        if '..' in Path(path).parts:raise ValueError('unsafe source path')
        print('FETCH',path,flush=True)
        req=Request(url,headers={'Cache-Control':'no-cache','User-Agent':'FirstReadingSourceWitness/1.0'})
        with urlopen(req,timeout=30) as response:
            if response.status!=200:raise ValueError('source unavailable '+url)
            data=response.read()
            mime=response.headers.get_content_type()
        relative=path.lstrip('/')+('index.html' if path.endswith('/') else '')
        dest=root/relative
        if mime=='text/html':
            soup=BeautifulSoup(data,'html.parser');htmls.append(relative)
            # Only traverse edition-owned reading routes; no unrelated archive.
            for anchor in soup.select('a[href]'):
                linked=urljoin(url,anchor['href'])
                if urlsplit(linked).path.startswith(EDITION) and not anchor['href'].startswith('#'):
                    queue.append(linked)
            for tag in soup.select('script[src],link[href],img[src],source[src],video[poster]'):
                attr='src' if tag.has_attr('src') else ('poster' if tag.has_attr('poster') else 'href')
                if tag.name=='link' and not set(tag.get('rel',[])) & {'stylesheet','icon','preload','modulepreload'}:
                    continue
                queue.append(urljoin(url,tag[attr]))
            for tag in soup.select('[srcset]'):
                queue.extend(urljoin(url,p.strip().split()[0]) for p in tag['srcset'].split(',') if p.strip())
        elif mime=='text/css':
            text=data.decode()
            for token in re.findall(r'url\(\s*["\x27]?([^)"\x27]+)',text):
                if not token.startswith(('data:','#')):queue.append(urljoin(url,token.strip()))
        elif 'javascript' in mime or path.endswith('.js'):
            for token in re.findall(r'(?:from\s*|import\s*)["\x27](\./[^"\x27]+)["\x27]',data.decode()):
                queue.append(urljoin(url,token))
        # A book keeps its full viewport and source-owned toolbar.
        # Do not inject the domain masthead into its measured reader.
        retain=False
        if not retain:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
        records.append({'url':url,'path':relative,'sha256':sha(data),'bytes':len(data),
                        'candidateSHA256':sha(dest.read_bytes()),'retainedShellProjection':retain})
    lock['sites']['solstice']['projectionSHA256']=sha(edition.read_bytes())
    lock['stagedPageReceipts'][EDITION.lstrip('/')+'index.html']['digest']=sha(edition.read_bytes())
    lock['stagedPageReceipts'][EDITION.lstrip('/')+'index.html']['projectionKind']='source-owned-full-viewport-reader'
    old=lock['sites']['solstice']['assetReceipts']
    for item in old:
        assert sha((root/'solstice'/item['path']).read_bytes())==item['sha256'],item['path']
    lock['firstReadingDependencyWitness']={'publicSource':PUBLIC+EDITION,
        'publicReleaseChanged':False,'editionSourceBytesPreserved':True,
        'htmlPaths':htmls,'files':records}
    lock['sites']['solstice']['missingAssets']=[]
    lock['editorialRouteCounts']['solstice']=len(list((root/'solstice').rglob('*.html')))
    (root/'source-lock.json').write_text(json.dumps(lock,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'publicFiles':len(records),'htmlRoutes':len(htmls),'originalAssetsVerified':len(old)}))
    verify(root)
    return records
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True)
    complete(p.parse_args().root)
