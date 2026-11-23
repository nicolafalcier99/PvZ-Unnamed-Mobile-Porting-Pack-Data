# Sources: music (`data/rules-music.json`, feature `unnamedMusic`)

Evidence: the research notes (modes-ui-shop) section 8 and Final table C, re-read with radare2 on
Unnamed 1.3beta2 `PlantsVsZombies.exe` and `gdi42.dll` (read only, nothing was run). App code:
`app/src/Mod/Unnamed/Music.*` (rules), `app/src/Mod/Engine/UnnamedMusic.*` (engine sites). A missing key plays the
vanilla tune.

The music files are the mod's own `lawnbgm(1).mp3`, `lawnbgm(4).mp3` .. `lawnbgm(14).mp3` (12 files, ~100 MB). Both
importers already copy them into the ignored `assets/` folder (`app/tools/pvzu_import_unnamed.py` and Android
`UnnamedImport.java`: top-level `.mp3`/`.ogg` of the zip's `[1.3beta2]` folder). They are never in git.

| key | Unnamed | vanilla | exe / dll evidence |
|---|---|---|---|
| music.tracks | `[1, 5, 4, 7, 12, 6, 8, 14, 11, 10, 13, 9]` (index = MusicTune - 1) | none (layered mainmusic.mo3) | gdi42 .rdata 0x103dbdf0 (12 pairs, study 8.2); PlayMusic detour exe 0x45adeb -> 0x10018800 looks the tune up, accepts only N == 1, 4, 5..14 (0x10018848), tune index > 12 -> vanilla (0x100188ab, so credits stay vanilla) |
| music.cerebrawlLevelMin / music.cerebrawlLevelMax | 71 / 80 | none | hook 258: exe 0x45b81b `jmp 0x95c1f0` with eax = PlayerInfo+0x24 (level) in the Adventure branch of StartGameMusic; 0x95c1f0 `cmp eax, 0x46 / jle`, `cmp eax, 0x50 / jg`, `mov edi, 9 / call 0x45b750` (MakeSureMusicIsPlaying(PUZZLE_CEREBRAWL)), else level 10 -> conveyor, else the vanilla 20/30 checks |

Playback (gdi42 0x100185a0, called by the PlayMusic detour): `StopAllMusic` (exe 0x45abb0), mCurMusicFileMain
(Music+0xc) = the mp3, `PlayFromOffset(file, 0, volume)` (exe 0x45ac70) with volume = double at 0x65b8f8 = **1.0**
(bytes `00 00 00 00 00 00 f0 3f`), then return to 0x45b080 past the drum/hihat set-up. Vanilla PlayFromOffset loops
every file except the credits song, so the mp3s loop (study U7 answered from this path). The game's music volume
setting scales every song (SDLMusicInterface global gain), as for the vanilla tunes.

## Engine notes and rulings

- Lazy load: only the playing mp3 is loaded (unloaded when another file starts); gdi42 loads all 12 at MusicInit.
  Same tunes, less memory on the phone.
- `mCurMusicTune` keeps the tune after an mp3 starts. In the exe the mod's `StopAllMusic` call leaves it -1
  (0x45abf1 `mov [esi+8], edi` with edi = -1, after PlayMusic stored it at 0x45adce), which would restart the mp3 on
  every MakeSureMusicIsPlaying, skip FadeOut and skip GameMusicPause. Kept as vanilla instead.
- No burst/drum layers while an mp3 plays (`UpdateMusicBurst` returns), as gdi42 skips the drum set-up.
- Decoder: SDL_mixer's MPG123 decoder, asked for by name (Android's vcpkg `sdl3-mixer[mpg123]`, app `vcpkg.json`;
  Homebrew's SDL3_mixer on the Mac has it too), else SDL_mixer's own choice. Since the loop fix the mp3 is decoded
  once to 16-bit PCM at the mixer rate and played from memory (see "Loop point").
- Not ported: gdi42's third detour (exe 0x433761 -> 0x100188d0) that replays the current mp3 on a screen the study
  could not name (U6).

## Checked on the Mac (silent, `SDL_AUDIO_DRIVER=dummy`, `-pvzu-log-music`)

Run: `pvz-portable -pvzu-mode unnamed -pvzu-pack <pack> -pvzu-width 1300 -pvzu-seed 7 -pvzu-level N -pvzu-dev-night log
-pvzu-log-music -pvzu-quit-frame 3500 -pvzu-hidden`. Lengths from the decoder (ffprobe in brackets).

| level / screen | tune | file | decoder length |
|---|---|---|---|
| title, Dave | 7 | lawnbgm(8).mp3 | 167.81 s (167.67) |
| seed chooser | 6 | lawnbgm(6).mp3 | 21.34 s (21.32) |
| 1 | 1 | lawnbgm(1).mp3 | 213.50 s (213.32) |
| 10 | 11 | lawnbgm(13).mp3 | 205.24 s (205.07) |
| 11 | 2 | lawnbgm(5).mp3 | 194.04 s (193.87) |
| 21 | 3 | lawnbgm(4).mp3 | 256.89 s (256.67) |
| 31 | 4 | lawnbgm(7).mp3 | 237.90 s (237.70) |
| 41 | 5 | lawnbgm(12).mp3 | 176.04 s (175.89) |
| 50 | 12 | lawnbgm(9).mp3 | 291.76 s (291.51) |
| 71 | 9 | lawnbgm(11).mp3 | 179.86 s (179.86) |

Every run logs the decoded play position every 300 updates (about 2.8 s of audio per 3 s), so the files are decoded,
not only opened. Loop (before the loop-point fix): the title screen left for 19000 updates logged `lawnbgm(8).mp3
decoded to 165.02 s of 167.81 s` then `0.12 s of 167.81 s, playing yes`. After it (2026-11-23): `166.78 s` then
`3.60 s` (lines 2.92 s apart: 166.78 + 2.92 runs 2.75 s past the loop end 166.946 s, + loop start 0.870 s = 3.62 s;
the whole-file loop would have shown 1.89 s). Vanilla mode runs of the same levels log `-> vanilla` for every tune and play `mainmusic.mo3`
through libopenmpt.

## Loop point (2026-11-23: "it feels like it stops and starts")

Cause: the files, not the mixer. Each mp3 is a whole song: it starts after silence and ends with its last chord
ringing out, then digital silence. The old path streamed the file and looped it whole (MIX_PlayTrack loops -1), so
every loop played the silent end, the silent start and the quiet ring-out in between. SDL_mixer's own jump is
seamless (an offline render of the old path, `tools/music_seam.py`, wraps at exactly the decoded length; no extra
frames, no click). Encoder delay/padding: only `lawnbgm(14)` has an Xing/Info header (Lavc57.10, delay 576, padding
1263); libmpg123 removes both itself (8224128 - 1839 = 8222289 decoded frames, the same in mpg123 and SDL_mixer). The
other 11 files have no header, so their decoder delay is part of the leading silence the trim skips.

Fix (app `src/Mod/MusicLoop.*`, `SexyAppFramework/sound/SDLMusicInterface.cpp`, mp3 only, vanilla tunes untouched):
decode the mp3 once to 16-bit PCM at the mixer rate (MIX_AudioDecoder, MPG123), find the first and last frame louder
than **-45 dBFS** peak, skip at most **10 s** at each end, bake a **30 ms** equal-power crossfade (tail fading out,
the frames before the loop start fading in) and play it as raw audio with MIX_PROP_PLAY_START_FRAME (first sound),
LOOP_START_FRAME and MAX_FRAME (loop end): the jump is sample-accurate.

- -45 dBFS: the end of a ring-out, 30+ dB under the songs' body (-11 to -23 dBFS RMS). At -60 dBFS (digital silence
  only) 0.6 to 4.2 s of quiet ring-out stayed at the seam (lawnbgm(4), (7), (9)); at -45 dBFS 0.2 to 1.1 s.
- 10 s bound: lawnbgm(9) (boss) has 3.9 s of silence before its intro and 8.8 s of quiet tail; a 1.5 s bound would
  have left 9+ s of silence there. Anything this quiet is inaudible in the game, so the bound only guards a broken file.
- 30 ms crossfade, the same for every song: both sides of each seam are near-silent (tail under -45 dBFS, then the
  intro's pre-roll), so no song needs a long musical crossfade; 30 ms only removes the step between the two edges.
- Memory: 4 bytes a frame, 3.8 MB (seed chooser) to 51.5 MB (lawnbgm(9)); one mp3 loaded at a time. Decode and scan
  took 0.01 to 0.14 s per song on the Mac (log timestamps), once per tune change.

Per song (44.1 kHz except (11) at 48 kHz, decoded to 44.1 kHz). Silence = frames under -60 dBFS peak at the end +
start of the file; quiet = under -40 dBFS. "Seam now" = the quiet runs touching the loop point in the game's own
render (`-pvzu-music-seams <dir>`, measured with `tools/music_seam.py`; "before" is the whole file's edges):

| file (tune) | length | skipped start / end | silence before -> now | quiet before -> now | song shape, choice |
|---|---|---|---|---|---|
| (1) day | 213.50 s | 0.79 s / 1.20 s | 1.23 s -> 7 ms | 2.57 s -> 0.59 s | ending ring-out; trim + 30 ms |
| (4) pool | 256.89 s | 0.08 s / 1.62 s | 0.56 s -> 4 ms | 2.56 s -> 0.86 s | long ring-out; trim + 30 ms |
| (5) night | 194.04 s | 0.29 s / 0.96 s | 0.81 s -> 1 ms | 1.78 s -> 0.53 s | ending ring-out; trim + 30 ms |
| (6) seed chooser | 21.34 s | 0.02 s / 0.05 s | 72 ms -> 0 ms | 80 ms -> 9 ms | loop-shaped (full level to the end); now seamless |
| (7) fog | 237.90 s | 0.29 s / 3.74 s | 2.54 s -> 3 ms | 4.61 s -> 0.57 s | long ring-out; trim + 30 ms |
| (8) title | 167.81 s | 0.87 s / 0.87 s | 1.26 s -> 3 ms | 1.90 s -> 0.17 s | ending ring-out; trim + 30 ms |
| (9) boss | 291.76 s | 3.91 s / 8.78 s | 9.56 s -> 0 ms | 13.74 s -> 1.06 s | silent intro + fade-out; trim + 30 ms |
| (10) minigame | 205.24 s | 0.16 s / 1.03 s | 0.57 s -> 6 ms | 1.66 s -> 0.47 s | ending ring-out; trim + 30 ms |
| (11) Cerebrawl | 179.86 s | 0.02 s / 0.09 s | 0.10 s -> 0 ms | 0.12 s -> 1 ms | loop-shaped; now seamless |
| (12) roof | 176.04 s | 0.65 s / 4.54 s | 4.39 s -> 4 ms | 5.65 s -> 0.46 s | long ring-out; trim + 30 ms |
| (13) conveyor | 205.24 s | 0.16 s / 1.03 s | 0.60 s -> 6 ms | 1.66 s -> 0.47 s | as (10) (same length and edges, other file); trim + 30 ms |
| (14) Zen garden | 186.45 s | 0.13 s / 1.41 s | 0.69 s -> 9 ms | 1.99 s -> 0.46 s | ending ring-out (Info header); trim + 30 ms |

The "quiet now" left on the ring-out songs is the quiet end of the last chord plus the intro's first soft notes:
the song now ends and starts again at once, without the dead air. The seam step is 0.0001 to 0.0042 (full scale 1)
against 0.023 to 0.136 for the 99.9th percentile sample step elsewhere in the same render: no click.

Not done (open): a musical loop that skips each song's ending (loop the body back to a matching bar, never play the
ring-out). A beat/chroma search (librosa, beat-synchronous chroma + MFCC over 16 beats before and 4 after the jump)
found strong matches only for (1) 32.50-192.84 s, (5) 14.02-149.68 s and (12) 63.59-156.18 s (similarity 0.96-0.97;
the other songs 0.81-0.92), and each drops 20-44 s of the song. Left to judge by ear.
