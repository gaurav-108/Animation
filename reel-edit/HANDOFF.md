# Reel edit — handoff for the local DaVinci Resolve session

Song: "Tu hai humdum" reel audio (screen recording, 27.07 s, ~123 BPM).
Output: 1080×1920, 60 fps, no text overlays, simple soft dissolves (0.5 s), no flashy VFX.

## Clip → lyric map (her 7 clips mirror the reference reel's 7 scenes)

| # | WhatsApp file | Shot | Song window (s) | Lyric | Source in → speed | Notes |
|---|---|---|---|---|---|---|
| 1 | VID-20260626-WA0135 | Golden temple + bell | 0.00 – 2.95 | Tu hai toh khaas hai | 1.4 s → 70% | Normal (not Log). Warm gold highlights, teal shadows |
| 2 | VID-20260527-WA0055 | Pagoda, walking | 2.95 – 7.07 | …khwabon jaise din | 0.2 s → 50% | **Stabilize strongly**. Rich daylight |
| 3 | VID-20260527-WA0017 | Girl under carved eaves | 7.07 – 10.83 | …raat afsana | 0.9 s → 50% | **Samsung Log**. Cool "night tale" grade. Dip-to-black transition in |
| 4 | VID-20260527-WA0019 | Turns from behind and smiles | 10.83 – 14.75 | Ke har lamha karun haske | 0.15 s → 65% | Partly Log. Smile lands on "haske" (~13.4 s). Soft golden glow |
| 5 | VID-20260626-WA0136 | Foggy temple and steps | 14.75 – 18.60 | Mere rab ka main shukrana | 0.0 s → 65% | **Heavy Log**: dehaze into golden morning haze |
| 6 | VID-20260527-WA0052 | Pagoda + flying pigeons | 18.60 – 22.60 | Tu hai humdum, humdum hai jaana | 0.0 s → 50% | **Stabilize**. Vivid sky |
| 7 | VID-20260527-WA0015 | Sitting by the brick wall | 22.60 – 27.07 | Mere dil ka… | 0.3 s → 75% | **Samsung Log**. Warm, soft. Fade to black 26.35–27.07 |

Slow motion: source is 60 fps, so use Optical Flow retiming (Speed Warp if available) to keep 60 fps.

## Log → Rec.709 normalisation (measured 0.3% / 99.7% RGB percentiles, 0–1)

| Clip | Black R/G/B | White R/G/B | Then |
|---|---|---|---|
| 3 | .165/.157/.157 | .89/.88/.90 | S-curve, sat ×1.35, cool shadows/mids |
| 4 | .03/.01/.01 | .86/.85/.88 | gentle S, sat ×1.1, slight warm highlights |
| 5 | .23/.227/.227 | .86/.86/.86 | strong S, sat ×1.9, golden mids/highlights |
| 7 | .149/.145/.122 | .87/.86/.90 | S-curve, sat ×1.3, warm |

In Resolve: Lift/Gain (or Custom curves) to those black/white points first, then the creative grade.
Light glow on all clips (Glow OFX, low), subtle vignette. Exact ffmpeg filter values are in `edit.py`.

## Scripts (cloud prototype, ffmpeg)
- `edit.py`: per-clip grade, slow-mo and interpolation, segment render
- `assemble.py`: dissolves, optional lyric captions, song, fades
- `lvl.py`: black/white point measurement
Stabilisation used vidstab (smoothing 40 on clips 2 and 6, 20 on the rest).
