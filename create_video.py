#!/usr/bin/env python
"""Simple wrapper to make video creation even easier.

Usage:
    python create_video.py "how docker technology works"
    python create_video.py "what is machine learning" --duration 30
    python create_video.py "how wifi works" --segments 6 --voice "british-female"
"""

import sys
from cli.build_project import main

if __name__ == "__main__":
    main()