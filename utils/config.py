import os
import logging
from dotenv import find_dotenv, load_dotenv
from pathlib import Path

def setup_logging():
    log_path = Path(__file__).parent.parent / 'timelapse_ig_reels.log'
    logging.basicConfig(
        filename=str(log_path),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info(f"Logging initialized. Writing to: {log_path}")

def load_instagram_config():
    load_dotenv(dotenv_path=find_dotenv())
    config = {
        'instagram_username': os.getenv('INSTAGRAM_USERNAME'),
        'instagram_password': os.getenv('INSTAGRAM_PASSWORD'),
        'session_file_path': os.getenv('SESSION_FILE_PATH'),
    }
    return config

def load_video_paths_config():
    load_dotenv(dotenv_path=find_dotenv())
    config = {
        'source_directory': os.getenv('VIDEO_SOURCE_PATH'),
        'target_directory': os.getenv('VIDEO_TARGET_PATH'),
    }
    return config