"""Build Module 1 prototype: 1080x1920 MP4, animated slide scenes, Kokoro TTS voiceover, burned-in captions.
Run with the tts-venv python:  src/tts-venv/bin/python src/build_module01.py
"""
import subprocess, pathlib, json, re, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent  # this folder (content/module-videos)
SRC = ROOT / 'src'; WORK = SRC / 'm1'; WORK.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
VOICE, SPEED = 'af_heart', 1.0

AQUA, DEEP, INK, CREAM, SAND, RED = '#286575', '#1D4E5B', '#202B33', '#FBF8F3', '#F3D9A4', '#B5483B'

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px}}
body{{font-family:'Source Sans 3',sans-serif;color:{INK};background:{CREAM};position:relative;overflow:hidden}}
.bar{{position:absolute;left:0;top:0;width:100%;height:18px;background:{AQUA}}}
.wrap{{position:absolute;left:120px;right:150px;top:340px;bottom:770px;display:flex;flex-direction:column}}
.brand{{position:absolute;left:120px;top:250px;font-family:'Manrope';font-weight:700;font-size:30px;color:#596874}}
.dark .brand{{color:#bcd2d8}}
.eyebrow{{font-family:'Manrope';font-weight:700;font-size:32px;letter-spacing:.14em;text-transform:uppercase;color:{AQUA};margin-bottom:34px}}
h1{{font-family:'Manrope';font-weight:800;font-size:100px;line-height:1.02;letter-spacing:-.03em}}
h2{{font-family:'Manrope';font-weight:800;font-size:78px;line-height:1.06;letter-spacing:-.02em}}
.sub{{font-size:50px;line-height:1.3;color:#4D5B66;margin-top:40px}}
.aqua{{color:{AQUA}}}
.foot{{position:absolute;left:90px;right:90px;bottom:250px;display:flex;justify-content:space-between;align-items:center;font-family:'Manrope';font-weight:600;font-size:30px;color:#596874}}
.dots{{display:flex;gap:12px}}.dots i{{width:14px;height:14px;border-radius:50%;background:#CCD5DD;display:block}}.dots i.on{{background:{AQUA}}}
.dark{{background:{DEEP};color:#fff}}.dark .eyebrow{{color:{SAND}}}.dark .sub{{color:#d5e3e7}}.dark .foot{{color:#bcd2d8}}.dark .dots i{{background:#3d6f7c}}.dark .dots i.on{{background:{SAND}}}
.hide{{opacity:0}}
.compact .tbl .hd{{font-size:40px;padding:14px 28px}}.compact .tbl .f{{font-size:36px;padding:11px 28px}}.compact .tbl .f code{{font-size:31px}}.compact .arrow{{font-size:46px;margin:8px 0}}
.card{{background:#fff;border:2px solid #E2E8EE;border-radius:26px;padding:30px 36px}}
.dark .card{{background:#24596a;border-color:#2f6a7b;color:#fff}}
.sym{{font-family:'Manrope';font-weight:800;font-size:66px;margin-top:34px;display:flex;align-items:center;gap:26px}}
.sym .x{{width:56px;height:56px;border-radius:50%;background:{SAND};color:{DEEP};font-size:36px;display:flex;align-items:center;justify-content:center;flex:none}}
.tbl{{border:3px solid {AQUA};border-radius:24px;background:#fff;overflow:hidden}}
.tbl .hd{{background:{AQUA};color:#fff;font-family:'Manrope';font-weight:800;font-size:48px;padding:22px 32px}}
.tbl .f{{font-size:42px;padding:18px 32px;border-top:2px solid #E2E8EE;display:flex;justify-content:space-between}}
.tbl .f code{{font-family:'Manrope';font-weight:700;font-size:36px;color:{AQUA}}}
.tbl .f.hl{{background:#E6F0F2}}
.tbl .f.bad{{background:#F8E3DF;color:{RED}}}
.arrow{{font-family:'Manrope';font-weight:800;font-size:56px;color:{AQUA};text-align:center;margin:14px 0}}
.lad{{display:flex;flex-direction:column;gap:22px;margin-top:40px}}
.lad .card{{display:flex;justify-content:space-between;align-items:center;font-size:42px}}
.lad b{{font-family:'Manrope';font-weight:800;font-size:44px}}
.lad .ok{{background:{AQUA};border-color:{AQUA};color:#fff}}
.pill{{display:inline-block;font-family:'Manrope';font-weight:700;font-size:34px;padding:10px 24px;border-radius:999px;background:{SAND};color:{INK}}}
.strike{{position:relative;opacity:.55}}
.strike:after{{content:'';position:absolute;left:-10px;right:-10px;top:50%;height:8px;background:{RED};transform:rotate(-6deg);border-radius:4px}}
"""

N = 8
def dots(i): return '<div class="dots">' + ''.join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(1, N + 1)) + '</div>'
def foot(i): return '<div class="brand">Rachael Quisel · airbnbai.rent</div>'

def tbl(name, fields):
    rows = ''.join(f'<div class="f {c}"><span>{a}</span><code>{b}</code></div>' for a, b, c in fields)
    return f'<div class="tbl"><div class="hd">{name}</div>{rows}</div>'

# Each scene: vo text, body class, html (elements with class s1..sK reveal in order), reveal word indexes
SCENES = [
 dict(vo="Three table decisions I got wrong. A total that read zero. A customer ID printed three times on one contract. About fourteen thousand duplicate rows.",
      cls='dark', reveal=[0, 6, 11, 20],
      html=lambda: f'''<div class="wrap"><div class="eyebrow">Systems Thinking for Airtable · 01</div>
<h2 class="s1">Three table decisions I got wrong.</h2>
<div class="sym s2"><span class="x">1</span>Total = $0</div>
<div class="sym s3"><span class="x">2</span>QuickBooks ID ×3</div>
<div class="sym s4"><span class="x">3</span>~14,000 duplicate rows</div></div>{foot(1)}'''),
 dict(vo="None of those were automation bugs. They were schema decisions I made too early and had to take back. This was a magazine advertising build in Airtable.",
      cls='', reveal=[0, 6, 18],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">What they had in common</div>
<h1 class="s1">Not automation bugs.</h1>
<div class="sub s2"><b class="aqua">Schema decisions</b> I made too early and had to take back.</div>
<div class="s3" style="margin-top:56px"><span class="pill">Magazine advertising · Airtable + Fillout + QuickBooks</span></div></div>{foot(2)}'''),
 dict(vo="Here's the rule I use now. Every value has one level where it's actually true.",
      cls='', reveal=[0, 6],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow s1">The rule I use now</div>
<h1 class="s2">Every value has <span class="aqua">one level</span> where it's actually true.</h1></div>{foot(3)}'''),
 dict(vo="The line total lives on the line item, where quantity and unit cost live. The contract just adds up the lines.",
      cls='', reveal=[0, 1, 14],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">Example 1 · the total that read zero</div>
<div class="s3">{tbl('Contracts', [('Contract Total', 'SUM(Line Total)', 'hl')])}</div>
<div class="arrow s3">↑ rolls up</div>
<div class="s1">{tbl('Contract Line Items', [('Quantity', 'number', ''), ('Per Unit Cost', 'currency', ''), ('Line Total', 'Quantity × Per Unit Cost', 'hl s2')])}</div></div>{foot(4)}'''),
 dict(vo="The QuickBooks customer ID lives on the advertiser, because QuickBooks assigns one ID to the customer, not to each contact.",
      cls='', reveal=[0, 3, 10],
      html=lambda: f'''<div class="bar"></div><div class="wrap compact"><div class="eyebrow">Example 2 · the ID printed 3×</div>
<div class="s2">{tbl('Advertisers', [('QuickBooks Customer ID', '✓ one value', 'hl')])}</div>
<div class="arrow s2">↓ has many</div>
<div class="s1">{tbl('Contacts', [('Contact 1 · QB ID', 'same ID', 'bad'), ('Contact 2 · QB ID', 'same ID', 'bad'), ('Contact 3 · QB ID', 'same ID', 'bad')])}</div>
<div class="s3" style="margin-top:30px;text-align:center"><span class="pill">Store it where QuickBooks assigns it</span></div></div>{foot(5)}'''),
 dict(vo="Store a value one level too high, and it can't compute. One level too low, and you get duplicates.",
      cls='', reveal=[0, 1, 11],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">How to spot it</div>
<h2 class="s1">Where a value lives decides what breaks.</h2>
<div class="lad"><div class="card s2"><b>Too high</b><span>can't compute · total = $0</span></div>
<div class="card ok s1"><b>Right level</b><span>one true value</span></div>
<div class="card s3"><b>Too low</b><span>duplicates · ID ×3</span></div></div></div>{foot(6)}'''),
 dict(vo="And when two tables are one-to-one, with no concrete reason to split them, it's the same table twice. So I deleted one.",
      cls='', reveal=[0, 2, 18],
      html=lambda: f'''<div class="bar"></div><div class="wrap compact"><div class="eyebrow">Example 3 · the 14,000 rows</div>
<div class="s1">{tbl('Contracts', [])}</div><div class="arrow s1">↓</div>
<div class="s1">{tbl('Contract Line Items', [])}</div><div class="arrow s2">↓ 1 : 1</div>
<div class="s2"><div class="s3wrap">{tbl('Insertion Orders', [('~14,000 rows', 'lookup fields only', 'bad')])}</div></div>
<div class="s3" style="margin-top:30px;text-align:center"><span class="pill">No concrete reason to split → same table twice → deleted</span></div></div>{foot(7)}'''),
 dict(vo="Before you build a single field, draw the model on one screen, and mark the level where each value is first singular. That's module one of my course, Systems Thinking for Airtable.",
      cls='dark', reveal=[0, 12, 22],
      html=lambda: f'''<div class="wrap"><div class="eyebrow">What I'd do differently now</div>
<h1 class="s1">Draw the model on one screen.</h1>
<div class="sub s2">Mark the level where each value is first singular.</div>
<div class="s3" style="margin-top:70px"><div class="card"><div style="font-family:Manrope;font-weight:800;font-size:46px">Systems Thinking for Airtable</div>
<div style="font-size:36px;margin-top:10px;color:{SAND}">Module 1 · Schema Design · on GitHub</div></div></div></div>
{foot(8)}'''),
]

def render_states():
    out = []
    for si, sc in enumerate(SCENES, 1):
        html = sc['html']()
        k = len(sc['reveal'])
        states = []
        for st in range(1, k + 1):
            # hide elements whose reveal index > st
            hide_css = ''.join(f'.s{j}{{opacity:0}}' for j in range(st + 1, k + 1))
            # strike-through on Insertion Orders appears at state 3 of scene 7
            extra = ('.s3wrap{position:relative}.s3wrap:after{content:"";position:absolute;left:-14px;right:-14px;top:50%;height:10px;background:' + RED + ';transform:rotate(-5deg);border-radius:5px}') if (si == 7 and st == 3) else ''
            doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{hide_css}{extra}</style></head><body class="{sc["cls"]}">{html}</body></html>'
            p = WORK / f's{si:02d}_{st}.html'; p.write_text(doc)
            png = WORK / f's{si:02d}_{st}.png'
            subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', f'--window-size={W},{H}', f'--screenshot={png}', f'file://{p}'],
                           check=True, capture_output=True)
            states.append(png)
        out.append(states)
    return out

def compress_silence(s, sr, max_gap=0.32, keep=0.26):
    """Trim edges and shorten any internal silence longer than max_gap to `keep` seconds."""
    win = int(0.02 * sr)
    n = len(s) // win
    rms = np.sqrt(np.mean(s[:n * win].reshape(n, win) ** 2, axis=1) + 1e-12)
    thr = rms.max() * 10 ** (-38 / 20)
    voiced = rms > thr
    idx = np.where(voiced)[0]
    s = s[:n * win]
    first, last = idx[0], idx[-1]
    out = [s[max(first - 2, 0) * win:(first) * win]]
    i = first
    while i <= last:
        if voiced[i]:
            out.append(s[i * win:(i + 1) * win]); i += 1
        else:
            j = i
            while j <= last and not voiced[j]: j += 1
            gap = (j - i) * 0.02
            seg = s[i * win:j * win]
            if gap > max_gap:
                k = int(keep / 0.02); h = k // 2
                seg = np.concatenate([seg[:h * win], seg[-(k - h) * win:]])
            out.append(seg); i = j
    out.append(s[(last + 1) * win:min(n, last + 5) * win])
    return np.concatenate(out)

def tts():
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(str(SRC / 'models/kokoro-v1.0.onnx'), str(SRC / 'models/voices-v1.0.bin'))
    clips = []
    for si, sc in enumerate(SCENES, 1):
        s, sr = k.create(sc['vo'], voice=VOICE, speed=SPEED, lang='en-us')
        s = compress_silence(np.asarray(s, dtype=np.float32), sr)
        sf.write(WORK / f'vo{si:02d}.wav', s, sr)
        clips.append((s, sr))
    return clips

FONT = '/usr/share/fonts/truetype/sand-box/google/Manrope/Manrope-VariableFont_wght.ttf'
CAP_FONT = ImageFont.truetype(FONT, 54); CAP_FONT.set_variation_by_name('ExtraBold')
CAP_MAXW = 780 - 2 * 34          # box must fit between x=150 and x=930 when centered at 540
CAP_TOP = 1180                   # ~61% of frame height; box bottom stays above ~72%

def text_w(t):
    l, _, r, _ = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textbbox((0, 0), t, font=CAP_FONT); return r - l

def chunks(text):
    """Caption cards: split per sentence, balance words across cards (max 2 lines each), balance the two lines."""
    import re as _re
    sents = [x.split() for x in _re.split(r'(?<=[.?])\s+', text.strip()) if x]
    cards = []
    def split2(g):
        if text_w(' '.join(g)) <= CAP_MAXW: return [g]
        k = min(range(1, len(g)), key=lambda k: max(text_w(' '.join(g[:k])), text_w(' '.join(g[k:]))))
        return [g[:k], g[k:]]
    for sw in sents:
        tot = sum(len(w) + 1 for w in sw)
        for nc in range(1, len(sw) + 1):
            groups = [[] for _ in range(nc)]; acc = 0
            for w in sw:
                gi = min(nc - 1, int(acc / tot * nc)); groups[gi].append(w); acc += len(w) + 1
            res = [split2(g) for g in groups if g]
            if all(text_w(' '.join(l)) <= CAP_MAXW for c in res for l in c): break
        cards += res
    return cards

def caption_img(lines):
    pw, ph, lh = 34, 22, 66
    widths = [text_w(' '.join(l)) for l in lines]
    bw = max(widths) + 2 * pw; bh = lh * len(lines) + 2 * ph
    im = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=22, fill=(16, 40, 48, 238))
    for i, l in enumerate(lines):
        t = ' '.join(l); w = widths[i]
        _, top, _, bot = d.textbbox((0, 0), t, font=CAP_FONT)
        d.text(((bw - w) // 2, ph + i * lh + (lh - (bot - top)) // 2 - top), t, font=CAP_FONT, fill=(255, 255, 255, 255))
    return im

def main():
    import soundfile as sf
    states = render_states()
    clips = tts()
    sr = clips[0][1]
    LEAD, TAIL = 0.18, 0.40
    timeline = []; t = 0.0; audio = []
    for sc, (s, _) in zip(SCENES, clips):
        sp = len(s) / sr; dur = LEAD + sp + TAIL
        timeline.append(dict(start=t, dur=dur, speech=sp))
        audio += [np.zeros(int(round(LEAD * sr))), s, np.zeros(int(round(TAIL * sr)))]
        t += dur
    total = t
    aud = np.concatenate(audio).astype(np.float32)
    aud = aud / max(1e-6, np.abs(aud).max()) * 0.89
    sf.write(WORK / 'voiceover.wav', aud, sr)
    print('total seconds', round(total, 2))

    caps = []; reveals = []
    for sc, tl in zip(SCENES, timeline):
        words = sc['vo'].split(); totc = sum(len(w) + 1 for w in words)
        def wtime(i, tl=tl, words=words, totc=totc):
            return tl['start'] + LEAD + tl['speech'] * (sum(len(w) + 1 for w in words[:i]) / totc)
        reveals.append([max(tl['start'], wtime(i) - 0.15) for i in sc['reveal']])
        i0 = 0
        for card in chunks(sc['vo']):
            n = sum(len(l) for l in card)
            caps.append(dict(a=wtime(i0), b=min(wtime(i0 + n) + 0.25, tl['start'] + tl['dur'] - 0.16), img=caption_img(card), text=' / '.join(' '.join(l) for l in card)))
            i0 += n
    # one caption at a time: each ends no later than the next one starts (hard cuts, no crossfade)
    for c, nxt in zip(caps, caps[1:]):
        c['b'] = min(c['b'], nxt['a'])
    json.dump(dict(timeline=timeline, total=total, captions=[(round(c['a'], 2), round(c['b'], 2), c['text']) for c in caps]),
              open(WORK / 'timeline.json', 'w'), indent=1)

    imgs = [[Image.open(p).convert('RGB') for p in st] for st in states]
    bgs = [Image.new('RGB', (W, H), DEEP if sc['cls'] == 'dark' else CREAM) for sc in SCENES]
    out = ROOT / 'module-01.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', str(WORK / 'voiceover.wav'), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(out)], stdin=subprocess.PIPE)
    XF, DIP = 0.35, 0.16  # element reveal fade; scene fade-out then fade-in (dip to the scene's own background)
    def scene_frame(si, tt):
        tl = timeline[si]; rv = reveals[si]; st = imgs[si]
        k = 0
        for j, r in enumerate(rv):
            if tt >= r: k = j
        cur = st[k]
        if k > 0 and tt - rv[k] < XF:
            cur = Image.blend(st[k - 1], st[k], (tt - rv[k]) / XF)
        p = (tt - tl['start']) / tl['dur']; scl = 1.0 + 0.015 * p
        if scl > 1.0005:
            nw, nh = int(W * scl), int(H * scl)
            big = cur.resize((nw, nh), Image.BILINEAR); x, y = (nw - W) // 2, (nh - H) // 2
            cur = big.crop((x, y, x + W, y + H))
        into = tt - tl['start']; left = tl['start'] + tl['dur'] - tt
        if si > 0 and into < DIP:
            cur = Image.blend(bgs[si], cur, into / DIP)
        elif si < len(timeline) - 1 and left < DIP:
            cur = Image.blend(bgs[si], cur, max(0.0, left / DIP))
        return cur
    nframes = int(math.ceil(total * FPS))
    for fi in range(nframes):
        tt = fi / FPS
        si = max(i for i, tl in enumerate(timeline) if tt >= tl['start'] - 1e-9)
        fr = scene_frame(si, tt).convert('RGBA')
        live = [c for c in caps if c['a'] <= tt < c['b']]
        if live:
            im = live[-1]['img']
            fr.alpha_composite(im, ((W - im.width) // 2, CAP_TOP))
        ff.stdin.write(fr.convert('RGB').tobytes())
    ff.stdin.close(); ff.wait()
    imgs[0][-1].save(ROOT / 'module-01-poster.png')
    print('wrote', out)

if __name__ == '__main__':
    main()
