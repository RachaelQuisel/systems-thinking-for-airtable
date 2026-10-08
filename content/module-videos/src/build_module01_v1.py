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
.wrap{{position:absolute;left:90px;right:90px;top:230px;bottom:640px;display:flex;flex-direction:column}}
.eyebrow{{font-family:'Manrope';font-weight:700;font-size:32px;letter-spacing:.14em;text-transform:uppercase;color:{AQUA};margin-bottom:44px}}
h1{{font-family:'Manrope';font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-.03em}}
h2{{font-family:'Manrope';font-weight:800;font-size:84px;line-height:1.06;letter-spacing:-.02em}}
.sub{{font-size:50px;line-height:1.3;color:#4D5B66;margin-top:40px}}
.aqua{{color:{AQUA}}}
.foot{{position:absolute;left:90px;right:90px;bottom:250px;display:flex;justify-content:space-between;align-items:center;font-family:'Manrope';font-weight:600;font-size:30px;color:#596874}}
.dots{{display:flex;gap:12px}}.dots i{{width:14px;height:14px;border-radius:50%;background:#CCD5DD;display:block}}.dots i.on{{background:{AQUA}}}
.dark{{background:{DEEP};color:#fff}}.dark .eyebrow{{color:{SAND}}}.dark .sub{{color:#d5e3e7}}.dark .foot{{color:#bcd2d8}}.dark .dots i{{background:#3d6f7c}}.dark .dots i.on{{background:{SAND}}}
.hide{{opacity:0}}
.card{{background:#fff;border:2px solid #E2E8EE;border-radius:26px;padding:30px 36px}}
.dark .card{{background:#24596a;border-color:#2f6a7b;color:#fff}}
.sym{{font-family:'Manrope';font-weight:800;font-size:76px;margin-top:40px;display:flex;align-items:center;gap:26px}}
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
def foot(i): return f'<div class="foot"><span>Rachael Quisel · airbnbai.rent</span>{dots(i)}</div>'

def tbl(name, fields):
    rows = ''.join(f'<div class="f {c}"><span>{a}</span><code>{b}</code></div>' for a, b, c in fields)
    return f'<div class="tbl"><div class="hd">{name}</div>{rows}</div>'

# Each scene: vo text, body class, html (elements with class s1..sK reveal in order), reveal word indexes
SCENES = [
 dict(vo="A total that read zero. A customer ID printed three times on one contract. Fourteen thousand duplicate rows.",
      cls='dark', reveal=[0, 5, 13],
      html=lambda: f'''<div class="wrap"><div class="eyebrow">Systems Thinking for Airtable · 01</div>
<h2>Three bugs I shipped.</h2>
<div class="sym s1"><span class="x">1</span>Total = $0</div>
<div class="sym s2"><span class="x">2</span>QuickBooks ID ×3</div>
<div class="sym s3"><span class="x">3</span>14,000 duplicate rows</div></div>{foot(1)}'''),
 dict(vo="None of those were automation bugs. They were table decisions I made too early, on a magazine advertising build in Airtable.",
      cls='', reveal=[0, 6, 16],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">What they had in common</div>
<h1 class="s1">Not automation bugs.</h1>
<div class="sub s2"><b class="aqua">Schema decisions</b>, made too early.</div>
<div class="s3" style="margin-top:56px"><span class="pill">Magazine advertising · Airtable + Fillout + QuickBooks</span></div></div>{foot(2)}'''),
 dict(vo="Here's the rule I use now. Every value has one level where it's actually true.",
      cls='', reveal=[0, 6],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow s1">The rule I use now</div>
<h1 class="s2">Every value has <span class="aqua">one level</span> where it's actually true.</h1></div>{foot(3)}'''),
 dict(vo="The line total lives on the line item, where quantity and unit cost live. The contract just adds up the lines.",
      cls='', reveal=[0, 7, 15],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">Example 1 · the total that read zero</div>
<div class="s3">{tbl('Contracts', [('Contract Total', 'SUM(Line Total)', 'hl')])}</div>
<div class="arrow s3">↑ rolls up</div>
<div class="s1">{tbl('Contract Line Items', [('Quantity', '4', ''), ('Per Unit Cost', '$1,200', ''), ('Line Total', 'Quantity × Per Unit Cost', 'hl s2')])}</div></div>{foot(4)}'''),
 dict(vo="The QuickBooks customer ID lives on the advertiser, because QuickBooks assigns one ID to the customer, not to each contact.",
      cls='', reveal=[0, 3, 10],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">Example 2 · the ID printed three times</div>
<div class="s2">{tbl('Advertisers', [('QuickBooks Customer ID', '✓ one value', 'hl')])}</div>
<div class="arrow s2">↓ has many</div>
<div class="s1">{tbl('Contacts', [('Contact 1 · QB ID', '1042', 'bad'), ('Contact 2 · QB ID', '1042', 'bad'), ('Contact 3 · QB ID', '1042', 'bad')])}</div>
<div class="s3" style="margin-top:30px;text-align:center"><span class="pill">Store the key where the other system assigns it</span></div></div>{foot(5)}'''),
 dict(vo="Store a value one level too high, and it can't compute. One level too low, and you get duplicates.",
      cls='', reveal=[0, 1, 11],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">How to spot it</div>
<h2 class="s1">Where a value lives decides what breaks.</h2>
<div class="lad"><div class="card s2"><b>Too high</b><span>can't compute · total = $0</span></div>
<div class="card ok s1"><b>Right level</b><span>one true value</span></div>
<div class="card s3"><b>Too low</b><span>duplicates · ID ×3</span></div></div></div>{foot(6)}'''),
 dict(vo="And when two tables are always one-to-one, with no real reason to split them, it's the same table twice. So I deleted one.",
      cls='', reveal=[0, 8, 20],
      html=lambda: f'''<div class="bar"></div><div class="wrap"><div class="eyebrow">Example 3 · the 14,000 rows</div>
<div class="s1">{tbl('Contracts', [])}</div><div class="arrow s1">↓</div>
<div class="s1">{tbl('Contract Line Items', [])}</div><div class="arrow s2">↓ 1 : 1</div>
<div class="s2"><div class="s3wrap">{tbl('Insertion Orders', [('~14,000 rows', 'lookups only', 'bad')])}</div></div>
<div class="s3" style="margin-top:30px;text-align:center"><span class="pill">No real reason to split → same table twice → deleted</span></div></div>{foot(7)}'''),
 dict(vo="Before you build a single field, draw the model on one screen, and mark the level where each value is first singular. That's module one of my course, Systems Thinking for Airtable.",
      cls='dark', reveal=[0, 12, 22],
      html=lambda: f'''<div class="wrap"><div class="eyebrow">What I'd do differently now</div>
<h1 class="s1">Draw the model on one screen.</h1>
<div class="sub s2">Mark the level where each value is first singular.</div>
<div class="s3" style="margin-top:70px"><div class="card"><div style="font-family:Manrope;font-weight:800;font-size:46px">Systems Thinking for Airtable</div>
<div style="font-size:36px;margin-top:10px;color:{SAND}">Module 1 · Schema Design · free on GitHub</div></div></div></div>
<div class="foot"><span>Rachael Quisel · airbnbai.rent</span>{dots(8)}</div>'''),
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

def tts():
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(str(SRC / 'models/kokoro-v1.0.onnx'), str(SRC / 'models/voices-v1.0.bin'))
    clips = []
    for si, sc in enumerate(SCENES, 1):
        s, sr = k.create(sc['vo'], voice=VOICE, speed=SPEED, lang='en-us')
        # trim leading/trailing silence
        a = np.abs(s); thr = 0.01 * a.max(); idx = np.where(a > thr)[0]
        s = s[max(idx[0] - int(.03 * sr), 0): idx[-1] + int(.08 * sr)]
        sf.write(WORK / f'vo{si:02d}.wav', s, sr)
        clips.append((s, sr))
    return clips

def chunks(text, maxc=32):
    words = text.split(); out = []; cur = []
    for w in words:
        if cur and (len(' '.join(cur + [w])) > maxc or cur[-1][-1] in '.?' or (cur[-1][-1] == ',' and len(' '.join(cur)) > 12)):
            out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    return out

FONT = '/usr/share/fonts/truetype/sand-box/google/Manrope/Manrope-VariableFont_wght.ttf'
def caption_img(text):
    f = ImageFont.truetype(FONT, 58); f.set_variation_by_name('ExtraBold')
    d = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    pw, ph = 40, 24
    im = Image.new('RGBA', (r - l + 2 * pw, 96), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=22, fill=(16, 40, 48, 235))
    dd.text((pw - l, (96 - (b - t)) // 2 - t), text, font=f, fill=(255, 255, 255, 255))
    return im

def main():
    states = render_states()
    clips = tts()
    sr = clips[0][1]
    LEAD, TAIL = 0.25, 0.55
    timeline = []; t = 0.0; audio = []
    for si, (sc, (s, _)) in enumerate(zip(SCENES, clips)):
        sp = len(s) / sr
        dur = LEAD + sp + TAIL
        timeline.append(dict(start=t, dur=dur, speech=sp))
        audio += [np.zeros(int(LEAD * sr)), s, np.zeros(int(TAIL * sr))]
        t += dur
    total = t
    import soundfile as sf
    aud = np.concatenate(audio).astype(np.float32)
    aud = aud / max(1e-6, np.abs(aud).max()) * 0.89
    sf.write(WORK / 'voiceover.wav', aud, sr)
    print('total seconds', round(total, 2))

    # captions + reveal times (by character proportion of speech)
    caps = []; reveals = []
    for sc, tl in zip(SCENES, timeline):
        words = sc['vo'].split(); totc = sum(len(w) + 1 for w in words)
        def wtime(i):
            return tl['start'] + LEAD + tl['speech'] * (sum(len(w) + 1 for w in words[:i]) / totc)
        reveals.append([max(tl['start'], wtime(i) - 0.15) for i in sc['reveal']])
        i0 = 0
        for ch in chunks(sc['vo']):
            a = wtime(i0); b = wtime(i0 + len(ch)); i0 += len(ch)
            caps.append(dict(a=a, b=b + 0.05, img=caption_img(' '.join(ch))))
    json.dump(dict(timeline=timeline, total=total), open(WORK / 'timeline.json', 'w'), indent=1)

    imgs = [[Image.open(p).convert('RGB') for p in st] for st in states]
    out = ROOT / 'module-01.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', str(WORK / 'voiceover.wav'), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(out)], stdin=subprocess.PIPE)
    XF, SF = 0.35, 0.30  # state crossfade, scene crossfade
    def scene_frame(si, tt):
        tl = timeline[si]; rv = reveals[si]; st = imgs[si]
        k = 0
        for j, r in enumerate(rv):
            if tt >= r: k = j
        cur = st[k]
        if k > 0 and tt - rv[k] < XF:
            cur = Image.blend(st[k - 1], st[k], (tt - rv[k]) / XF)
        # gentle push-in
        p = (tt - tl['start']) / tl['dur']; sc = 1.0 + 0.02 * p
        if sc > 1.0005:
            nw, nh = int(W * sc), int(H * sc)
            big = cur.resize((nw, nh), Image.BILINEAR)
            x, y = (nw - W) // 2, (nh - H) // 2
            cur = big.crop((x, y, x + W, y + H))
        return cur
    nframes = int(math.ceil(total * FPS))
    for fi in range(nframes):
        tt = fi / FPS
        si = max(i for i, tl in enumerate(timeline) if tt >= tl['start'] - 1e-9)
        frame = scene_frame(si, tt)
        if si > 0 and tt - timeline[si]['start'] < SF:
            prev = scene_frame(si - 1, timeline[si]['start'] - 1 / FPS)
            frame = Image.blend(prev, frame, (tt - timeline[si]['start']) / SF)
        fr = frame.convert('RGBA')
        for c in caps:
            if c['a'] <= tt < c['b']:
                a = min(1, (tt - c['a']) / 0.1, (c['b'] - tt) / 0.1)
                im = c['img']
                if a < 1:
                    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
                fr.alpha_composite(im, ((W - im.width) // 2, 1360))
        ff.stdin.write(fr.convert('RGB').tobytes())
        if fi == int(timeline[0]['start'] + 0) and False: pass
    ff.stdin.close(); ff.wait()
    # poster: last state of scene 1 with first caption-free frame
    imgs[0][-1].save(ROOT / 'module-01-poster.png')
    print('wrote', out)

if __name__ == '__main__':
    main()
