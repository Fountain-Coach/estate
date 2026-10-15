# Public estate: bounded route and asset census

Read-only HTTPS GET discovery from all nine known currently public estate host roots, their Git-owned HTML route candidates, and known archival publication assets. This is **not** an exhaustive public filesystem inventory. Unlinked routes, dynamic services and resources larger than the size cap may not appear.

| Public hostname | Fetched | HTTP 200 | Other HTTP | HTML 200 | Request errors |
|---|---:|---:|---:|---:|---:|
| benedikt-eickhoff.de | 24 | 23 | 1 | 7 | 0 |
| book.fountain.coach | 54 | 54 | 0 | 22 | 0 |
| fountain.coach | 40 | 26 | 14 | 8 | 0 |
| governance.fountain.coach | 277 | 277 | 0 | 165 | 0 |
| instruments.fountain.coach | 14 | 14 | 0 | 4 | 0 |
| midi2.fountain.coach | 37 | 37 | 0 | 19 | 0 |
| status.fountain.coach | 22 | 22 | 0 | 12 | 0 |
| teatro.fountain.coach | 9 | 5 | 4 | 1 | 0 |
| works.benedikt-eickhoff.de | 144 | 142 | 2 | 62 | 0 |

**Across all hosts:** 621 fetched URLs; 0 URLs still queued when bounded crawl ended.

Every fetched URL has a status, response content hash where available, and discovered on-estate links/assets in [public-route-census.json](public-route-census.json).

## Coverage limits

- A URL returning 200 does not prove identical content exists in the canonical owner source. Independent blob provenance and full release receipts are required.
- Only nine live hostnames are followed; planned Solstice and archived Tennis are excluded.
- Canonical ownership and delegated Solstice route identity remain unchanged.
- Relative URLs, scripts, images and CSS url() references are followed, subject to fixed host/size/count restrictions. Redirects are recorded.
- URLs with query strings are collapsed to the same path. Interactive API, signed/private endpoints, JavaScript-generated requests, and nonlinked documents may not be discovered.
- No GitHub branch, Ubuntu service, public DNS, tunnel or Caddy deployment is changed.

Run: npm run recovery:crawl:probe to refresh; npm run recovery:crawl:verify checks the frozen witness structure offline (not the present live site).
