import logging
from pathlib import Path

def cleanup_temp_video(temp_video_path):
    if not temp_video_path:
        return True
        
    try:
        temp_path = Path(temp_video_path)
        thumbnail_path = Path(f"{temp_video_path}.jpg")
        audio_path = temp_path.parent / f"{temp_path.stem}TEMP_MPY_wvf_snd.mp3"
        
        files_cleaned = 0
        if temp_path.exists():
            temp_path.unlink()
            logging.info(f"Cleaned up temporary video: {temp_path}")
            files_cleaned += 1
            
        if thumbnail_path.exists():
            thumbnail_path.unlink()
            logging.info(f"Cleaned up thumbnail: {thumbnail_path}")
            files_cleaned += 1
            
        if audio_path.exists():
            audio_path.unlink()
            logging.info(f"Cleaned up audio file: {audio_path}")
            files_cleaned += 1
            
        if files_cleaned > 0:
            logging.info(f"Cleaned up {files_cleaned} temporary files")
        return True
        
    except Exception as e:
        logging.error(f"Failed to clean up temporary files for {temp_video_path}: {str(e)}")
        return False