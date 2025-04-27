import logging
from pathlib import Path
from utils.config import setup_logging
from time_lapse import generate_timelapse
from music_reel import create_music_reel
from ig_upload import upload_ig_video
from utils.cleanup import cleanup_temp_video

def process_daily_timelapse():
    try:
        # Step 1: Generate timelapse
        timelapse_path = generate_timelapse()
        if not timelapse_path or not Path(timelapse_path).exists():
            logging.error("Timelapse generation failed")
            return False

        # Step 2: Try creating and uploading reel with music
        success, temp_video, caption = create_music_reel(timelapse_path)
        if success:
            logging.info("Successfully uploaded reel with music")
            return True

        # Step 3: Video upload if music reel fails
        if temp_video:
            success = upload_ig_video(video_path=temp_video, caption=caption)
            if success:
                cleanup_temp_video(temp_video)
        else:
            success = upload_ig_video(video_path=timelapse_path)
            
        if success:
            logging.info("Successfully uploaded video")
            return True
        
        logging.error("All upload attempts failed")
        return False

    except Exception as e:
        logging.error(f"Daily timelapse process failed: {str(e)}")
        return False

if __name__ == "__main__":
    setup_logging()
    process_daily_timelapse()