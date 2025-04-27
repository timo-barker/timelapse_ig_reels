import logging
from pathlib import Path
import tempfile
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from utils.config import load_instagram_config

config = load_instagram_config()

def get_instagram_client(config):
    cl = Client()
    session_file = Path(config['session_file_path'])
    if session_file.exists():
        try:
            session = cl.load_settings(str(session_file))
            cl.set_settings(session)
            cl.login(config['instagram_username'], config['instagram_password'])
            try:
                cl.get_timeline_feed()
                logging.info("Successfully logged in using saved session")
                return cl
            except LoginRequired:
                logging.info("Session expired, creating new login")
                old_session = cl.get_settings()
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
        except Exception as e:
            logging.error(f"Session login failed: {str(e)}")
    try:
        cl.login(config['instagram_username'], config['instagram_password'])
        cl.dump_settings(str(session_file))
        logging.info("Created new session and saved to file")
        return cl
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        raise

def upload_ig_video(video_path=None, caption="Daily Cat Cam Timelapse"):
    try:
        cl = get_instagram_client(config)
        if video_path and Path(video_path).exists():
            logging.info(f"Using provided video file: {video_path}")
            path_to_upload = str(video_path)
        else:
            tmp_files = sorted(
                [f for f in Path(tempfile.gettempdir()).glob('*.mp4')],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            if not tmp_files:
                logging.error("No video file found to upload")
                return False
            path_to_upload = str(tmp_files[0])
            logging.info(f"Using latest temp video file: {path_to_upload}")

        response = cl.video_upload(
            path=path_to_upload,
            caption=caption,
            extra_data={
                "custom_accessibility_caption": "Cat Cam Timelapse",
                "like_and_view_counts_disabled": 0,
                "disable_comments": 0
            }
        )
        if response:
            logging.info("Video upload successful")
            return True
        return False
    except Exception as e:
        logging.error(f"Error in video upload: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = upload_ig_video()
        if not success:
            logging.error("Video upload failed")
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        raise