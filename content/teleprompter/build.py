#!/usr/bin/env python3
"""Build teleprompter.html from template.html + read-aloud-scripts.md.
Each '## ' heading is one module; each paragraph under it is one scene (verbatim)."""
import json, re, pathlib
here = pathlib.Path(__file__).parent
src = (here.parent / 'module-videos' / 'read-aloud-scripts.md').read_text(encoding='utf-8')
modules = []
for block in re.split(r'^## ', src, flags=re.M)[1:]:
    title, _, body = block.partition('\n')
    paras = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
    modules.append({
        'id': 'm%02d' % (len(modules) + 1),
        'title': title.strip(),
        'scenes': [{'label': 'Scene %d' % (i + 1), 'text': p} for i, p in enumerate(paras)],
    })
assert len(modules) == 8, len(modules)
data = json.dumps(modules, ensure_ascii=False).replace('</', '<\\/')
html = (here / 'template.html').read_text(encoding='utf-8').replace('/*__SCRIPTS__*/[]', data)
(here / 'teleprompter.html').write_text(html, encoding='utf-8')
for m in modules:
    print(m['id'], m['title'], len(m['scenes']), 'scenes', sum(len(s['text'].split()) for s in m['scenes']), 'words')
