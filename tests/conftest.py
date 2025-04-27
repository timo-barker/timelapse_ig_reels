import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
timelapse_package = project_root / 'timelapse_ig_reels'
sys.path.insert(0, str(timelapse_package))