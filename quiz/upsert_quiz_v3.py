#!/usr/bin/env python3
"""Upsert v3 quiz files into draft theme 190037622851, verify each."""
import json, subprocess, sys, time

THEME = "gid://shopify/OnlineStoreTheme/190037622851"
CLI = "/opt/hatch/bin/shopify"
FILES = [
    ("sections/quiz-amaran.liquid", "sections", "Amaran product finder"),
    ("sections/quiz-godox.liquid", "sections", "Godox product finder"),
    ("sections/quiz-entry.liquid", "sections", "Quiz entry banner"),
    ("sections/quiz-home.liquid", "sections", "Product finder - homepage"),
    ("templates/index.json", "json", None),
]
MUT = """mutation($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { field message }
  }
}"""
READ = """{ node(id: "%s") { ... on OnlineStoreTheme { files(first: 1, filenames: ["%s"]) { nodes { body { ... on OnlineStoreThemeFileBodyText { content } } } } } } }"""

def cli(args):
    r = subprocess.run([CLI, "call-tool", "--name", args[0], "--arguments-json", args[1]],
                       capture_output=True, text=True, timeout=120)
    return json.loads(r.stdout)

for filename, kind, marker in FILES:
    content = open(f"/home/hatch/workspace/quiz_build/{filename.split('/')[-1]}").read()
    args = json.dumps({"query": MUT, "variables": {"themeId": THEME, "files": [
        {"filename": filename, "body": {"type": "TEXT", "value": content}}]}})
    res = cli(("graphql_mutation", args))
    sc = res.get("result", {}).get("structuredContent", {})
    data = sc.get("data", {})
    errs = data.get("themeFilesUpsert", {}).get("userErrors", [])
    up = data.get("themeFilesUpsert", {}).get("upsertedThemeFiles", [])
    print(filename, "-> upserted:", up, "errors:", errs)
    if errs or not up:
        print("FAILED", json.dumps(res)[:1500]); sys.exit(1)
    time.sleep(12)
    res2 = cli(("graphql_query", json.dumps({"query": READ % (THEME, filename)})))
    back = res2["result"]["structuredContent"]["data"]["node"]["files"]["nodes"][0]["body"]["content"]
    if kind == "sections":
        ok = len(back) == len(content) and marker in back
        print(f"  verify: {len(back)} bytes (expected {len(content)}), marker {'OK' if marker in back else 'MISSING'} -> {'PASS' if ok else 'FAIL'}")
    else:
        body = back[back.index("{"):]
        ok = json.loads(body) == json.loads(content)
        print(f"  verify: JSON equal -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        sys.exit(1)
print("ALL FILES UPserted AND VERIFIED")
