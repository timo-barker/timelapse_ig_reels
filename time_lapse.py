import logging
from datetime import datetime, timedelta
import moviepy.editor as mpy
from pathlib import Path
from utils.config import load_video_paths_config

def process_timelapse_clip(mp4_file):
    try:
        video_clip = mpy.VideoFileClip(str(mp4_file))
        sped_up = video_clip.speedx(factor=1440)
        return sped_up.set_fps(30).without_audio()
    except Exception as e:
        logging.error(f'Error processing {mp4_file}: {str(e)}')
        return None

def generate_timelapse(source_directory=None, target_directory=None):
    if source_directory is None or target_directory is None:
        config = load_video_paths_config()
        source_directory = Path(config['source_directory'])
        target_directory = Path(config['target_directory'])
    else:
        source_directory = Path(source_directory)
        target_directory = Path(target_directory)
    
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    output_filename = target_directory / f'Cat Cam-{yesterday_date}.mp4'
    
    if output_filename.exists():
        logging.info(f'Timelapse already exists for {yesterday_date}: {output_filename}')
        return output_filename
        
    logging.info(f'Generating timelapse for date: {yesterday_date}')
    
    timelapse_clips = []
    for subdir in source_directory.iterdir():
        if subdir.is_dir() and subdir.name.startswith(yesterday_date):
            logging.info(f'Processing directory: {subdir}')
            mp4_files = list(subdir.glob('*.mp4'))
            logging.info(f'Found {len(mp4_files)} MP4 files')
            processed_clips = [process_timelapse_clip(file) for file in mp4_files]
            timelapse_clips.extend([clip for clip in processed_clips if clip is not None])
    
    try:
        if not timelapse_clips:
            logging.error('No valid clips found to process')
            return None
            
        logging.info('Concatenating video clips...')
        concatenated_clips = mpy.concatenate_videoclips(timelapse_clips, method="compose")
        final_timelapse = concatenated_clips.subclip(0, min(concatenated_clips.duration, 60))
        
        logging.info(f'Writing final timelapse to: {output_filename}')
        final_timelapse.write_videofile(str(output_filename), codec="libx264")
        logging.info('Timelapse generation completed successfully')
        return output_filename
        
    except Exception as e:
        logging.error(f'Error creating final timelapse: {str(e)}')
        raise
    
if __name__ == "__main__":
    generate_timelapse()