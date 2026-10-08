# Teleprompter (draft)

This folder holds a simple teleprompter for recording the module videos. Rachael reads from it while she records each module in Loom.

This is a draft. As of Oct 7, 2026, it was tested in headless Chrome but not yet on Rachael's Mac.

## What's here

- `teleprompter.html`: the teleprompter. It is one offline file. Open it in a browser by double-clicking it. It holds all 8 module scripts, one paragraph per scene, plus a box to paste any other script. It has a compact mode for a narrow window next to a webcam.
- `template.html`: the page layout, without the scripts.
- `build.py`: rebuilds `teleprompter.html` from `template.html` and `../module-videos/read-aloud-scripts.md`. Each `## ` heading becomes one module, and each paragraph under it becomes one scene.
- `preview.png` and `preview-compact.png`: screenshots of the normal and compact views.

## How to rebuild

After any change to `../module-videos/read-aloud-scripts.md`, run this from the repo root:

```sh
python3 content/teleprompter/build.py
```

It needs Python 3 and nothing else.

## Notes

- The Module 2 example number shows as a placeholder, `<EXAMPLE_AAPC_NUMBER, read digit by digit>`, because the scripts in this repo use a placeholder. Rachael still needs to choose the number to read aloud. Her own copy of the teleprompter may show a different number.
- The screenshots were taken before the placeholder was added, so they may not match the current file exactly.
