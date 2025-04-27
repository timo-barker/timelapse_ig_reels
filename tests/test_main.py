import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from timelapse_ig_reels.main import process_daily_timelapse

class TestMain(unittest.TestCase):
    @patch('timelapse_ig_reels.main.Path')
    @patch('timelapse_ig_reels.main.generate_timelapse')
    @patch('timelapse_ig_reels.main.create_music_reel')
    @patch('timelapse_ig_reels.main.upload_ig_video')
    @patch('timelapse_ig_reels.main.cleanup_temp_video')
    def test_process_daily_timelapse_success_with_music(
        self, mock_cleanup, mock_upload, mock_create_reel, mock_generate, mock_path_class
    ):
        # Setup
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.__str__.return_value = "/tmp/test.mp4"
        mock_path_class.return_value = mock_path
        
        mock_generate.return_value = mock_path
        mock_create_reel.return_value = (True, None, "Test caption")

        # Test
        result = process_daily_timelapse()

        # Assert
        self.assertTrue(result)
        mock_generate.assert_called_once()
        mock_create_reel.assert_called_once_with(mock_path)

    @patch('timelapse_ig_reels.main.Path')
    @patch('timelapse_ig_reels.main.generate_timelapse')
    @patch('timelapse_ig_reels.main.create_music_reel')
    @patch('timelapse_ig_reels.main.upload_ig_video')
    @patch('timelapse_ig_reels.main.cleanup_temp_video')
    def test_process_daily_timelapse_fallback_to_video(
        self, mock_cleanup, mock_upload, mock_create_reel, mock_generate, mock_path_class
    ):
        # Setup
        mock_timelapse = MagicMock(spec=Path)
        mock_timelapse.exists.return_value = True
        mock_timelapse.__str__.return_value = "/tmp/test.mp4"
        mock_path_class.return_value = mock_timelapse
        
        mock_temp_video = MagicMock(spec=Path)
        mock_temp_video.exists.return_value = True
        mock_temp_video.__str__.return_value = "/tmp/temp.mp4"
        
        mock_generate.return_value = mock_timelapse
        mock_create_reel.return_value = (False, mock_temp_video, "Test caption")
        mock_upload.return_value = True

        # Test
        result = process_daily_timelapse()

        # Assert
        self.assertTrue(result)
        mock_generate.assert_called_once()
        mock_create_reel.assert_called_once_with(mock_timelapse)
        mock_upload.assert_called_once_with(
            video_path=mock_temp_video,
            caption="Test caption"
        )
        mock_cleanup.assert_called_once_with(mock_temp_video)

    @patch('timelapse_ig_reels.main.generate_timelapse')
    def test_process_daily_timelapse_generation_failed(self, mock_generate):
        # Setup
        mock_generate.return_value = None

        # Test
        result = process_daily_timelapse()

        # Assert
        self.assertFalse(result)
        mock_generate.assert_called_once()