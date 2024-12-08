# Video-Search-and-Upload_Bot
🎥 Video Search and Upload Bot Overview This is a Python-based bot designed to automate the process of searching, downloading, and uploading videos from social media platforms like Instagram and Youtube. The bot integrates with APIs to upload videos to a server, ensuring a seamless and efficient workflow.
## Overview
This bot automates the process of downloading and uploading videos to a server using pre-signed URLs. It monitors a directory for `.mp4` files, processes them, and uploads them to the specified API.

## Features
- Monitors a directory for new `.mp4` files.
- Uploads videos to a server using pre-signed URLs.
- Automatically deletes videos after processing.
- Logs the progress of uploads and API interactions.

## Requirements
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

## Setup
1. Clone or download the repository.
2. Open the project in VS Code.
3. Create a folder named `videos` in the project root.
4. Place your `.mp4` files in the `videos` folder.
5. Install dependencies using:
   ```bash
   pip install -r requirements.txt
