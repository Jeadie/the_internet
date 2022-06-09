#!/bin/bash
#
# Build the python dependencies needed for the lmabda into an AWS lambda layer

cd layer/
pip install -r ../requirements.txt -t .python
zip -r ../content_scraper_dependencies.zip *
cd -
