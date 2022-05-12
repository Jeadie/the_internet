import os

stage = os.environ.get("STAGE", "base")

if stage == "production":
    from the_internet.production import *
else:
    from .base import *