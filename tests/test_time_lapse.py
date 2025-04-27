import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil
from time_lapse import process_timelapse_clip, generate_timelapse
from utils.config import load_video_paths_config

class TestTimeLapse(unittest.TestCase):
    def setUp(self):
        self.temp_base = tempfile.mkdtemp()
        self.test_dir = Path(self.temp_base) / "test_timelapse"
        self.test_dir.mkdir(exist_ok=True)
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        
    def tearDown(self):
        if Path(self.temp_base).exists():
            shutil.rmtree(self.temp_base)

    @patch('moviepy.editor.VideoFileClip')
    def test_process_timelapse_clip(self, mock_video_clip):
        mock_instance = MagicMock()
        mock_video_clip.return_value = mock_instance
        mock_instance.speedx.return_value = mock_instance
        mock_instance.set_fps.return_value = mock_instance
        mock_instance.without_audio.return_value = mock_instance

        test_file = self.test_dir / "test.mp4"
        test_file.touch()
        result = process_timelapse_clip(test_file)
        
        self.assertIsNotNone(result)
        mock_video_clip.assert_called_once_with(str(test_file))
        mock_instance.speedx.assert_called_once_with(factor=1440)
        mock_instance.set_fps.assert_called_once_with(30)
        mock_instance.without_audio.assert_called_once()

    @patch('time_lapse.process_timelapse_clip')
    def test_generate_timelapse(self, mock_process):
        mock_clip = MagicMock()
        mock_clip.duration = 10.0  
        mock_process.return_value = mock_clip
        
        source_dir = self.test_dir / "source"
        target_dir = self.test_dir / "target"
        source_dir.mkdir(exist_ok=True)
        target_dir.mkdir(exist_ok=True)
        
        date_dir = source_dir / self.yesterday
        date_dir.mkdir(exist_ok=True)
        test_file = date_dir / "test.mp4"
        test_file.touch()
        
        with patch('moviepy.editor.concatenate_videoclips') as mock_concat:
            mock_concat.return_value = mock_clip
            result = generate_timelapse(source_dir, target_dir)
            
        self.assertIsNotNone(result)
        mock_process.assert_called_once()

    def test_generate_timelapse_no_files(self):
        result = generate_timelapse(self.test_dir, self.test_dir)
        self.assertIsNone(result)