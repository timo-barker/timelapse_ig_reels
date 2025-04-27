import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
from timelapse_ig_reels.music_reel import (
    get_random_track, create_music_reel, load_music_genres, get_filename
)

class TestMusicReel(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("/tmp/test_music")
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        if self.test_dir.exists():
            for file in self.test_dir.glob("*"):
                file.unlink()
            self.test_dir.rmdir()

    def test_load_music_genres(self):
        genres = load_music_genres()
        self.assertIsInstance(genres, dict)
        self.assertGreater(len(genres), 0)
        self.assertIn("Ambient/Electronic", genres)

    @patch('timelapse_ig_reels.music_reel.get_instagram_client')
    def test_get_random_track(self, mock_client):
        mock_cl = MagicMock()
        mock_client.return_value = mock_cl
        mock_cl.private_request.return_value = {
            'items': [{
                'track': {
                    'id': '12345678',
                    'title': 'Test Track',
                    'subtitle': 'Test Subtitle',
                    'display_artist': 'Test Artist',
                    'audio_cluster_id': 123456,  
                    'highlight_start_times_in_ms': [0],
                    'has_lyrics': True,
                    'audio_asset_id': 789012,    
                    'duration_in_ms': 90000,
                    'allows_saving': True,
                    'dash_manifest': 'test_manifest',
                    'territory_validity_periods': {},
                    'is_explicit': False,
                    'uri': 'spotify:track:123',
                    'preview_uri': 'http://example.com/preview'
                }
            }]
        }

        track = get_random_track(mock_cl)
        self.assertIsNotNone(track)
        self.assertEqual(track.title, 'Test Track')
        self.assertEqual(track.display_artist, 'Test Artist')
        self.assertEqual(track.id, '12345678')

    @patch('timelapse_ig_reels.music_reel.get_instagram_client')
    @patch('timelapse_ig_reels.music_reel.get_random_track')
    def test_create_music_reel(self, mock_track, mock_client):
        mock_cl = MagicMock()
        mock_client.return_value = mock_cl
        mock_track.return_value = MagicMock(
            display_artist="Test Artist",
            title="Test Track"
        )
        
        test_file = self.test_dir / "test.mp4"
        test_file.touch()
        
        success, temp_video, caption = create_music_reel(test_file)
        self.assertIsNotNone(caption)
        self.assertIn("Test Artist", caption)