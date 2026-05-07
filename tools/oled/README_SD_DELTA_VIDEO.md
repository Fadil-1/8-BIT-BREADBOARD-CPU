# OLED SD Delta Video Tool

`video_to_oled_sd_delta.py` converts an image, GIF, or video into an SD-backed OLED video stream for F8-BB. The generated assembly player stays small. Frame data lives on the SD card and is read one compact frame slot at a time.

The baseline mode is black-and-white threshold output. Grayscale output is also supported. `--threshold` always selects threshold mode, even when `--grayscale` is also used.

## Output files

The tool writes three main files:

```text
video_delta_frames.bin
    SD video data. Write to the SD card starting at --video-block.

VIDEO_PLAYER.asm
    Stage-2 player loaded by the normal BT1 boot flow.

video_delta_manifest.txt
    Build details, frame count, slot size, frame sizes, and run counts.
```

The generated player reads frame slots from SD into RAM at `0x6000`, then applies changed horizontal byte-runs to OLED GDDRAM. The display area uses raw rows `0..62` and avoids raw row `63`.

## Black-and-white threshold mode

Threshold mode converts each source pixel to off or on. Pixels at or above the threshold become the foreground grayscale nibble. Pixels below the threshold become `0x0`.

### Example:

**On Linux:**

```bash
python3 tools/oled/video_to_oled_sd_delta.py \
  ./ASM/programs/oled_video_test/input_media/stick_fight_resized.gif \
  --out-dir build/oled_video_sd_delta \
  --out-asm ASM/programs/oled_video_sd_delta_player/VIDEO_PLAYER.asm \
  --video-block 2200 \
  --max-frames 24 \
  --frame-step 2 \
  --threshold 220 \
  --invert \
  --fit contain \
  --inset-x 2 \
  --delay-calls 0 \
  --device /dev/sdX
```

Run `sync` after writes complete, and replace `/dev/sdX` with your actual SD device.

**On Windows:**

```powershell
python tools\oled\video_to_oled_sd_delta.py .\ASM\programs\oled_video_test\input_media\stick_fight_resized.gif --out-dir build\oled_video_sd_delta --out-asm ASM\programs\oled_video_sd_delta_player\VIDEO_PLAYER.asm --video-block 2200 --max-frames 24 --frame-step 2 --threshold 220 --invert --fit contain --inset-x 2 --delay-calls 0 --device "\\.\PhysicalDrivex" --windows-lock-volume "\\?\Volume{volume_GUID}\"
```

Replace `PhysicalDrivex ` and `volume_GUID` with your actual SD device.

Threshold mode is best for high-contrast animations, and anything with a clear subject/background split.

## Grayscale mode

Grayscale mode quantizes each source pixel into a small number of OLED gray levels. It preserves mid-tone detail better than threshold mode, but frame slots are usually larger and playback may be slower.

### Example:

**On Linux:**

```bash
python3 tools/oled/video_to_oled_sd_delta.py \
  ./ASM/programs/oled_video_test/input_media/meme_clip.gif \
  --out-dir build/oled_video_sd_delta_gray \
  --out-asm ASM/programs/oled_video_sd_delta_player/VIDEO_PLAYER.asm \
  --video-block 2300 \
  --max-frames 12 \
  --frame-step 3 \
  --grayscale \
  --gray-levels 4 \
  --fit contain \
  --inset-x 2 \
  --delay-calls 0 \
  --device /dev/sdX
```

Run `sync` after writes complete, and replace `/dev/sdX` with your actual SD device.

**On Windows:**


```powershell
python tools\oled\video_to_oled_sd_delta.py .\ASM\programs\oled_video_test\input_media\meme_clip.gif --out-dir build\oled_video_sd_delta_gray --out-asm ASM\programs\oled_video_sd_delta_player\VIDEO_PLAYER.asm --video-block 2300 --max-frames 12 --frame-step 3 --grayscale --gray-levels 4 --fit contain --inset-x 2 --delay-calls 0 --device "\\.\PhysicalDrive5" --windows-lock-volume "\\?\Volume{volume_GUID}\"
```

Replace `PhysicalDrivex ` and `volume_GUID` with your actual SD device.

Use `--gray-levels 4` first. More levels can preserve more detail, but they can also increase SD data size and OLED update time.

## Option behavior

```text
--threshold N
    Selects black-and-white mode. N must be 0..255. A supplied threshold overrides grayscale mode.

--grayscale
    Selects grayscale mode only when --threshold is absent.

--gray-levels N
    Number of levels used in grayscale mode. Valid range is 2..16.

--fg N
    Foreground OLED grayscale nibble for threshold mode. Default is 0x0F.

--invert
    Inverts source brightness before conversion. Useful for dark drawings on a bright background.

--fit contain
    Preserves aspect ratio and adds padding.

--fit crop
    Fills the OLED area and crops edges.

--fit stretch
    Forces the source into 128x63.

--inset-x N
    Clears N pixels on the left and right edges. Useful for avoiding edge artifacts.

--inset-y N
    Clears N pixels at the top and bottom of the safe area.

--slot-sectors N
    Fixed SD sector count per frame slot. 0 selects the smallest slot size that fits every frame.
```

## Player deployment

After the tool writes the SD video data, deploy the generated player through the normal stage-2 path:

**On Linux:**

```bash
sudo env "PATH=$PATH" python3 tools/deployment/deploy_asm.py sd \
  ./ASM/programs/oled_video_sd_delta_player/VIDEO_PLAYER.asm \
  --origin 0x0200 \
  --device /dev/sdX \
  --block 1003 \
  --descriptor-block 1002 \
  --dump-annotated \
  --out-dir build/oled_video_sd_delta_player
```

Run `sync` after writes complete, and replace `/dev/sdX` with your actual SD device.

**On Windows:**

```powershell
python tools\deployment\deploy_asm.py sd .\ASM\programs\oled_video_sd_delta_player\VIDEO_PLAYER.asm --origin 0x0200 --device "\\.\PhysicalDrivex" --windows-lock-volume "\\?\Volume{volume_GUID}\" --block 1003 --descriptor-block 1002 --dump-annotated --out-dir build\oled_video_sd_delta_player
```

Replace `PhysicalDrivex ` and `volume_GUID` with your actual SD device.

The generated player is the RAM payload. The video binary starts at `--video-block` and must not overlap the player payload blocks.

## Practical tuning

For faster playback, reduce changed pixels per frame. Increase `--threshold`, use `--invert` when needed, use `--inset-x 2`, increase `--frame-step`, or reduce `--max-frames`.

For better image detail, use grayscale mode with `--gray-levels 4`. If playback becomes too slow, reduce frame count or raise `--frame-step`.

For high-contrast clips, threshold mode usually looks better and plays faster. For faces, grayscale mode usually keeps more of the subject visible.
