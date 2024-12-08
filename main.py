import os
import asyncio
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API Token and Constants
FLIC_TOKEN = "flic_d7ef29143564c6cbf9b2fa25c8c74fe61294b3bfc8c49801fe8edacfd6718470"
BASE_UPLOAD_URL = "https://api.socialverseapp.com/posts"
VIDEO_DIR = "./videos"

# API Headers
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json",
}

# Ensure video directory exists
os.makedirs(VIDEO_DIR, exist_ok=True)

async def get_upload_url():
    """Fetch pre-signed upload URL from the API."""
    try:
        response = requests.get(  # Changed to GET
            f"{BASE_UPLOAD_URL}/generate-upload-url",
            headers=HEADERS,
        )
        if response is not None and response.status_code == 200:
            data = response.json()
            logging.info(f"Upload URL and hash retrieved: {data}")
            return data.get("url"), data.get("hash")
        elif response is not None:
            logging.error(f"Failed to get upload URL: Status Code: {response.status_code}, Response: {response.text}")
        else:
            logging.error("Failed to get upload URL: No response from server.")
        return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while fetching upload URL: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Unexpected error while fetching upload URL: {e}")
        return None, None

async def upload_video_to_presigned_url(file_path, upload_url):
    """Upload video to the pre-signed URL using a PUT request."""
    try:
        with open(file_path, "rb") as f:
            response = requests.put(upload_url, data=f)
        if response.status_code == 200:
            logging.info(f"Video uploaded successfully: {file_path}")
        else:
            logging.error(f"Failed to upload video: {response.text}")
    except Exception as e:
        logging.error(f"Error during video upload: {e}")

async def create_post(title, video_hash, category_id=25):
    """Create a post using the uploaded video's hash."""
    data = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,  # Changed to 25 as per instructions
    }
    try:
        response = requests.post(BASE_UPLOAD_URL, headers=HEADERS, json=data)
        if response.status_code == 200:
            logging.info(f"Post created successfully with title: {title}")
        else:
            logging.error(f"Failed to create post: {response.text}")
    except Exception as e:
        logging.error(f"Error creating post: {e}")

async def process_video(file_path):
    """Process a single video: upload and create post."""
    title = os.path.basename(file_path)  # Set the title from the filename
    upload_url, video_hash = await get_upload_url()  # Get the upload URL and hash
    if upload_url and video_hash:
        await upload_video_to_presigned_url(file_path, upload_url)  # Upload the video
        await create_post(title, video_hash)  # Create the post with title and hash
        os.remove(file_path)  # Delete the file after processing
        logging.info(f"Processed and deleted: {file_path}")

async def monitor_directory():
    """Monitor the directory for new video files and process them."""
    processed_files = set()  # Track processed files to avoid reprocessing
    while True:
        for file_name in os.listdir(VIDEO_DIR):
            if file_name.endswith(".mp4") and file_name not in processed_files:
                file_path = os.path.join(VIDEO_DIR, file_name)
                asyncio.create_task(process_video(file_path))  # Process the video
                processed_files.add(file_name)  # Mark this file as processed
        await asyncio.sleep(5)  # Check every 5 seconds for new files

async def main():
    """Main function to start monitoring and processing videos."""
    logging.info("Starting video bot...")
    await monitor_directory()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        stop_bot = True  # Set flag to stop the bot
        logging.info("Shutting down video bot.")

