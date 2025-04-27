# 📸 Timelapse Instagram Reels 🐱

Automated tool for creating and uploading timelapse videos to Instagram Reels with music. 

## About

A pet project (pun intended!) for turning boring home-surveillance cat vids into engaging social media content.

Vibe coded from:
- 📚 8 credits of Python courses
- 👨🏾‍💻 GitHub Copilot (Claude 3.5)
- 🧠 Google Gemini (2.5 Pro)
- 🤖 OpenAI ChatGPT (GPT-4o)
- ☕ Lots of coffee

## Features

- Automatically processes 24 hours of MP4 files into a 60-second video
- Adds random mood-watching music from Instagram's library
- Uploads the video to Instagram Reels
- Provides daily updates on the cat's activities 
- Automatic cleanup of temporary files
- Configurable via environment variables
- Easy to set up and use

## Prerequisites

- Python 3.8 or higher
- Instagram account credentials
- Source video footage directory
- MoviePy 1.x (instagrapi requires MoviePy < 2.0.0)
- FFmpeg (for video processing)
  ```bash
  # macOS (using Homebrew)
  brew install ffmpeg
  
  # Linux
  sudo apt-get install ffmpeg
  
  # Windows
  # Download from https://ffmpeg.org/download.html
  ```

## Installation & Development

1. Clone and setup environment:
```bash
# Clone repository
git clone https://github.com/timo-barker/timelapse_ig_reels.git
cd timelapse_ig_reels

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e '.[dev]'
```

2. Run tests (optional):
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage reports
python -m pytest tests/ --cov=timelapse_ig_reels --cov-report=term-missing
```

3. Clean up:
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv
```

## Configuration

Create a `.env` file with:
```env
INSTAGRAM_USERNAME='your_username'
INSTAGRAM_PASSWORD='your_password'
SESSION_FILE_PATH='/path/to/session.json'
VIDEO_SOURCE_PATH='/path/to/source/videos'
VIDEO_TARGET_PATH='/path/to/output/videos'
```

## Usage

Run the main script daily in your task/job scheduler:

```bash
python main.py
```

Or use the installed console script:

```bash
timelapse-ig
```

## Project Structure

```
timelapse_ig_reels/
├── resources/
│   └── music_genres.json   # Music genre configurations
├── utils/
│   ├── config.py           # Configuration loading
│   └── cleanup.py          # Temporary file cleanup
├── time_lapse.py           # Timelapse generation
├── music_reel.py           # Music selection and reel creation
├── ig_upload.py            # Instagram upload handling
├── main.py                 # Main execution script
├── tests/
├── setup.py
├── requirements.txt
└── .env
```

## Known Issues

- Instagrapi requires MoviePy < 2.0.0 due to dependency constraints
- Using MoviePy 2.x or higher will break functionality
- Keep MoviePy at version 1.x for compatibility

## License

This project is licensed under the MIT [License](LICENSE)

## Support

- None. You're on your own
- This program is a bot and VERY against Meta's TOS. **You risk your account being banned!** 
- Use a dummy account for testing
- *We have detected automated activities on your account* (HTTP 403) means Stop
- Take a break. Don't abuse the API. Stay under 30 uploads within 24 hours
- Good luck!