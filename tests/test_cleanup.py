import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import shutil
from utils.cleanup import cleanup_temp_video

class TestCleanup(unittest.TestCase):
    def setUp(self):
        self.temp_base = tempfile.mkdtemp()
        self.test_dir = Path(self.temp_base) / "test_cleanup"
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        if Path(self.temp_base).exists():
            shutil.rmtree(self.temp_base)

    def test_cleanup_temp_video_none(self):
        result = cleanup_temp_video(None)
        self.assertTrue(result)

    def test_cleanup_temp_video(self):
        test_video = self.test_dir / "test.mp4"
        test_thumb = self.test_dir / "test.mp4.jpg"
        test_audio = self.test_dir / "testTEMP_MPY_wvf_snd.mp3"
        
        test_video.touch()
        test_thumb.touch()
        test_audio.touch()
        
        result = cleanup_temp_video(test_video)
        self.assertTrue(result)
        self.assertFalse(test_video.exists())
        self.assertFalse(test_thumb.exists())
        self.assertFalse(test_audio.exists())