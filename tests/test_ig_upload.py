import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import shutil  
from timelapse_ig_reels.ig_upload import get_instagram_client, upload_ig_video

class TestIGUpload(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("/tmp/test_upload")
        self.test_dir.mkdir(exist_ok=True)
        self.temp_file = self.test_dir / "temp"
        self.temp_file.mkdir(exist_ok=True)  
        
    def tearDown(self):
        if self.test_dir.exists():
            for file in self.test_dir.glob("*"):
                if file.is_dir():
                    shutil.rmtree(file)  
                else:
                    file.unlink()
            self.test_dir.rmdir()

    @patch('timelapse_ig_reels.ig_upload.Client')
    def test_get_instagram_client(self, mock_client):
        mock_cl = MagicMock()
        mock_client.return_value = mock_cl
        
        config = {
            'instagram_username': 'test_user',
            'instagram_password': 'test_pass',
            'session_file_path': str(self.test_dir / 'session.json')
        }
        
        client = get_instagram_client(config)
        self.assertIsNotNone(client)
        mock_cl.login.assert_called_once()

    @patch('timelapse_ig_reels.ig_upload.get_instagram_client')
    def test_upload_ig_video(self, mock_get_client):
        mock_cl = MagicMock()
        mock_get_client.return_value = mock_cl
        mock_cl.video_upload.return_value = True
        
        test_file = self.test_dir / "test.mp4"
        test_file.touch()
        
        result = upload_ig_video(test_file)
        self.assertTrue(result)
        mock_cl.video_upload.assert_called_once()