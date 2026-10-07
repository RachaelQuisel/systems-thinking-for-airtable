# Module videos (draft)

This folder holds draft work for short vertical videos, one for each of the 8 course modules. They are meant for Instagram Reels and LinkedIn.

This is a draft in progress. As of Oct 7, 2026, the plan tracker shows about 58% done. Nothing here is final.

## What's here

- `plan.md`: the plan tracker, with decisions and the task list.
- `read-aloud-scripts.md`: the voiceover scripts for all 8 modules. Rachael plans to record these in her own voice.
- `scripts.md`: scripts, scene lists, LinkedIn captions, and the shot list.
- `recording-runbook.md`: steps for recording Airtable screen footage in sandbox bases with dummy data.
- `module-01.mp4` and `module-01-poster.png`: a prototype of the Module 1 video. It uses slides and a placeholder computer voice. It is not the final video.
- `src/build_module01.py`: the script that built the Module 1 prototype.
- `src/build_module01_v1.py`: an earlier version of that script, kept for reference.

## Notes

- The Airtable IDs in these docs are placeholders, like `<DEMO_BASE_ID_1>`, `<DEMO_BASE_ID_2>`, `<DEMOS_WORKSPACE_ID>`, and `<TABLE_ID>`. The real IDs are in Rachael's Airtable Demos workspace. Those bases hold dummy data only.
- The Module 2 example ID number is a placeholder, `<EXAMPLE_AAPC_NUMBER>`. Rachael still needs to choose the number to use.
- The build scripts need things that are not in this repo: a Python setup with the Kokoro text-to-speech package, its voice model files in `src/models/`, Google Chrome, ffmpeg, and the Manrope font. They were not run from this folder, so they may need small fixes before they work here.
