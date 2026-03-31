# LittleHirishima Discord Music Bot

LittleHirishima is a Discord bot (Pycord-based) focused on voice/music playback from YouTube.
It supports slash commands for queue management, loop modes, pause/resume, seek, shuffle, and now-playing embeds.

## Features

- Slash-command based music controls
- YouTube search by keyword or direct YouTube URL
- Per-guild queue persistence under `lib/Guild/<guild_id>/voice.json`
- Loop modes: normal, repeat queue, repeat current song
- Auto-disconnect when the bot is left alone in a voice channel
- Recent-play tracking per guild in `lib/Guild/<guild_id>/recent.json`

## Music Commands

All commands below are slash commands.

- `/connect` - Connect bot to your current voice channel
- `/disconnect` - Disconnect bot from the channel
- `/play [query]` - If `query` is set, play/search a song; if omitted, resume
- `/queue [query] [remove]` - Add/list/remove queued songs (`remove: all` supported)
- `/pause` - Pause current playback
- `/loop` - Cycle loop mode
- `/next [index]` - Skip to next queued track or a specific queue index
- `/playing` - Show currently playing song
- `/seek <timestamp>` - Seek track position (`SS`, `MM:SS`, `HH:MM:SS`)
- `/shuffle` - Shuffle queue order
- `/replay` - Restart current song from the beginning

## Requirements

- Python 3.10+
- FFmpeg available in PATH
- Discord library (Pycord API usage)
- `aiohttp`
- `mutagen`
- `yt-dlp`

The project already includes a bundled `lib/lib` folder with several dependencies and helper modules.

## Setup

1. Create a Discord application and bot token.
2. Create `Little_Hirishima Secrets.json` in the project root:

```json
{
  "TOKEN": "YOUR_BOT_TOKEN"
}
```

3. Verify paths in `botPath.py`:
- `YTDLPEXECUTABLE` defaults to `lib/yt-dlp_linux`
- `ANIMEDIRECTORY`, `REQUESTSDIRECTORY`, `PIPESDIRECTORY` are environment-specific

4. Ensure `ffmpeg` is installed and accessible.

5. Install missing Python packages if your environment does not already have them:

```bash
pip install py-cord aiohttp mutagen yt-dlp
```

## Run

Run directly:

```bash
python little_hirishima.pyw
```

Or use the included `run.bash` (Linux/tmux workflow).

## Notes

- This repository contains legacy/admin/extra automation logic (anime buffer utilities, host control commands) in `botControl.py`, but the primary active functionality is the Discord music bot.
- The default downloader executable path is Linux-oriented. If running on Windows, update `YTDLPEXECUTABLE` in `botPath.py` to a valid Windows `yt-dlp` executable.
- Guild voice queue state is persisted automatically and reloaded on restart.

## Roadmap

- A Next.js web app in `hirishima-web` is planned to provide a browser-based control panel for managing the Discord bot (music queue, playback controls, and bot status) without using Discord commands directly.

