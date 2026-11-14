#!/usr/bin/env python3
"""Upload the new 17 Nov 11.11 poster to Shopify Files and verify the CDN URL.
Flow: stagedUploadsCreate -> PUT raw bytes -> fileCreate -> poll node(id:).
Saves result to uploaded_url.json next to this script.
Adapted from ~/workspace/a2-video/compare/upload_compare.py."""
import json, os, subprocess, time
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
LOCAL = 'rynow-1111-poster-17nov.png'
REMOTE = 'rynow-1111-poster-17nov.png'
ALT = 'RYNOW 11.11 poster, 1-17 November 2026: 11.11 ended. RYNOW hasn\'t.'


def call(name, payload):
    for _ in range(3):
        out = subprocess.run(['/opt/hatch/bin/shopify', 'call-tool', '--name', name,
                              '--arguments-json', json.dumps(payload)],
                             capture_output=True, text=True, timeout=180)
        if out.stdout.strip():
            return json.loads(out.stdout)
        time.sleep(3)
    raise RuntimeError('empty response from ' + name)


def main():
    path = os.path.join(BASE, LOCAL)
    size = os.path.getsize(path)
    print('UPLOAD %s -> %s (%d bytes)' % (LOCAL, REMOTE, size), flush=True)
    m = ('mutation { stagedUploadsCreate(input: [{filename: %s, mimeType: "image/png", '
         'resource: FILE, fileSize: "%d"}]) { stagedTargets { url resourceUrl parameters { name value } } '
         'userErrors { field message } } }' % (json.dumps(REMOTE), size))
    r = call('graphql_mutation', {'query': m})
    sc = r['result']['structuredContent']
    tgt = sc['data']['stagedUploadsCreate']['stagedTargets'][0]
    errs = sc['data']['stagedUploadsCreate']['userErrors']
    assert not errs, 'stagedUploadsCreate errors: %s' % errs
    with open(path, 'rb') as f:
        resp = requests.put(tgt['url'], data=f,
                            headers={'Content-Type': 'image/png'}, timeout=120)
    assert resp.status_code in (200, 201, 204), 'staged PUT %s: %s' % (resp.status_code, resp.text[:300])
    resource_url = tgt['resourceUrl']
    print('  resourceUrl: %s' % resource_url, flush=True)

    m = ('mutation { fileCreate(files: [{originalSource: %s, alt: %s, contentType: IMAGE}]) '
         '{ files { ... on MediaImage { id } } userErrors { field message } } }'
         % (json.dumps(resource_url), json.dumps(ALT)))
    r = call('graphql_mutation', {'query': m})
    sc = r['result']['structuredContent']
    files = sc['data']['fileCreate']['files']
    errs = sc['data']['fileCreate']['userErrors']
    assert files and not errs, 'fileCreate failed: %s %s' % (files, errs)
    gid = files[0]['id']
    print('  file gid: %s' % gid, flush=True)

    q = '{ node(id: %s) { ... on MediaImage { id status image { url } } } }' % json.dumps(gid)
    url = None
    for i in range(12):
        r = call('graphql_query', {'query': q})
        node = r['result']['structuredContent']['data']['node']
        status = node.get('status')
        url = (node.get('image') or {}).get('url')
        print('  poll %d: status=%s url=%s' % (i + 1, status, bool(url)), flush=True)
        if status == 'READY' and url:
            break
        if status == 'FAILED':
            raise RuntimeError('file processing FAILED for ' + gid)
        time.sleep(3)
    assert url, 'file not ready after polling: %s' % gid
    print('  CDN: %s' % url, flush=True)

    resp = requests.head(url, timeout=30, allow_redirects=True)
    print('VERIFY %s -> HTTP %s' % (REMOTE, resp.status_code), flush=True)
    assert resp.status_code == 200, 'CDN URL not 200: %s' % url

    result = {REMOTE: {'gid': gid, 'url': url, 'alt': ALT, 'http_status': resp.status_code}}
    out_path = os.path.join(BASE, 'uploaded_url.json')
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print('Saved ' + out_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
