import logging
from pathlib import Path
from datetime import datetime, timedelta
from instagrapi import Client
from instagrapi.types import Track
from instagrapi.exceptions import LoginRequired
from utils.config import load_video_paths_config, load_instagram_config
import random
from instagrapi.extractors import extract_track
import tempfile
import json
from pathlib import Path

def load_music_genres():
    try:
        json_path = Path(__file__).parent / 'resources' / 'music_genres.json'
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading music genres: {str(e)}")
        raise

MUSIC_GENRES = load_music_genres()

def get_filename():
    config = load_video_paths_config()
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    input_path = Path(config['target_directory']) / f'Cat Cam-{yesterday_date}.mp4'
    return str(input_path)

config = load_instagram_config()

def get_random_track(cl, max_attempts=3, min_duration=60, max_duration=3600):
    logging.info(f"Searching for music (duration {min_duration}-{max_duration}s)...")
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        try:
            category = random.choice(list(MUSIC_GENRES.keys()))
            logging.info(f"Attempt {attempts}/{max_attempts} - Selected category: {category}")

            subgenre = random.choice(list(MUSIC_GENRES[category].keys()))
            query = random.choice(MUSIC_GENRES[category][subgenre])
            logging.info(f"Selected query: {query} (from {subgenre})")
            
            params = {
                "query": query,
                "browse_session_id": cl.generate_uuid(),
            }
            result = cl.private_request("music/audio_global_search/", params=params)
            
            if result.get('items'):
                for item in result['items']:
                    item['track']['territory_validity_periods'] = {}
                tracks = [extract_track(item["track"]) for item in result["items"]]
                
                suitable_tracks = [
                    t for t in tracks 
                    if min_duration <= (t.duration_in_ms / 1000) <= max_duration
                ]
                
                track_count = len(suitable_tracks)
                logging.info(f"Found {track_count} tracks within duration limits")
                
                if suitable_tracks:
                    track = random.choice(suitable_tracks)
                    duration_seconds = track.duration_in_ms / 1000
                    logging.info(f"Selected track: {track.display_artist} - {track.title} ({duration_seconds:.1f}s)")
                    return track
                else:
                    logging.warning(f"No tracks with suitable duration found for query: {query}")
            else:
                logging.warning(f"No results found for query: {query}")
                
        except Exception as e:
            logging.error(f"Error getting music tracks: {str(e)}")
            logging.error(f"Exception type: {type(e)}")
            
        if attempts < max_attempts:
            logging.info("Retrying with different genre...")
    
    logging.error(f"Failed to find tracks after {max_attempts} attempts")
    return None

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

def create_music_reel(timelapse_path):
    timelapse_path = Path(timelapse_path)
    temp_video_path = None
    reel_caption = None
    
    if not timelapse_path.exists():
        logging.error(f'Timelapse file not found: {timelapse_path}')
        return False, None, None

    try:
        cl = get_instagram_client(config)
        video_path = timelapse_path
        if not video_path.exists():
            logging.error(f"Video file not found: {video_path}")
            return False, None, None

        track = get_random_track(cl)
        if track:
            reel_caption = f"🎵 {track.display_artist} - {track.title}"
            logging.info(f"Using caption: {reel_caption}")
            
            temp_dir = Path(tempfile.gettempdir())
            logging.info(f"Monitoring temporary directory: {temp_dir}")
            before_files = set(temp_dir.glob('*.mp4'))
            logging.info(f"Found {len(before_files)} existing MP4 files")
            
            try:
                response = cl.clip_upload_as_reel_with_music(
                    path=str(video_path),
                    caption=reel_caption,
                    track=track
                )
            except Exception as upload_error:
                logging.error(f"Error during reel upload: {str(upload_error)}")
                response = False
            finally:
                after_files = set(temp_dir.glob('*.mp4'))
                new_files = after_files - before_files
                temp_video_path = next(iter(new_files)) if new_files else None
                
                if temp_video_path:
                    logging.info(f"Found new temporary video: {temp_video_path}")
                else:
                    logging.warning("No new temporary video file was created")
            
            if response:
                logging.info(f"Successfully uploaded reel with music: {track.title}")
                return True, temp_video_path, reel_caption
            
            if temp_video_path:
                logging.info(f"Upload failed but captured temp file: {temp_video_path}")
            return False, temp_video_path, reel_caption
            
    except Exception as e:
        logging.error(f"Error in create_music_reel: {str(e)}")
        return False, temp_video_path, reel_caption

if __name__ == "__main__":
    try:
        timelapse_path = Path(get_filename())
        if timelapse_path.exists():
            success, temp_video, caption = create_music_reel(timelapse_path)
            if not success:
                logging.error("Failed to upload as reel, try upload as video")
        else:
            logging.error("No timelapse video generated to upload")
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        raise