import praw
import os
import subprocess
import requests

# Reddit API credentials
client_id = 'AnT1VJEVnyqQ2rV6Px89jg'
client_secret = 'HTCyxmAi5gUEIXde_I1W9DYBBaqZTA'
user_agent = 'samasc'

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Subreddit to monitor
subreddit_name = 'SouthAsianMasculinity'

# File to keep track of processed submission IDs
processed_ids_file = 'processed_submissions.txt'

# imgBB API key
imgbb_api_key = 'e10fcb9d8adc96e9e32cbea24aeeb219'

# Load already processed submission IDs
if os.path.exists(processed_ids_file):
    with open(processed_ids_file, 'r') as f:
        processed_ids = f.read().splitlines()
else:
    processed_ids = []

# Function to take a screenshot using Puppeteer
def take_screenshot(url, output_path):
    # Run the Puppeteer script to take the screenshot
    subprocess.run(['node', 'screenshot.js', url, output_path])

# Function to upload a screenshot to imgBB
def upload_to_imgbb(image_path):
    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()

    response = requests.post(
        url='https://api.imgbb.com/1/upload',
        data={
            'key': imgbb_api_key,
            'image': image_data,
            'name': os.path.basename(image_path),
        },
    )

    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        raise Exception('Failed to upload image to imgBB')

# Get the 5 newest threads from the subreddit
subreddit = reddit.subreddit(subreddit_name)
new_submissions = subreddit.new(limit=5)

# Process new submissions
for submission in new_submissions:
    if submission.id not in processed_ids:
        submission_url = submission.url
        submission_id = submission.id
        
        # Screenshot file path
        screenshot_path = f'{submission_id}.png'
        
        # Take a screenshot
        take_screenshot(submission_url, screenshot_path)
        
        # Upload the screenshot to imgBB
        img_url = upload_to_imgbb(screenshot_path)
        
        # Add the submission ID to the processed list
        processed_ids.append(submission_id)
        
        # Save the imgBB URL to a text file
        with open('imgbb_urls.txt', 'a') as url_file:
            url_file.write(f'{submission_id}: {img_url}\n')
        
        # Print submission ID, URL, and imgBB URL (for debugging)
        print(f"New submission found: ID={submission_id}, URL={submission_url}, Image URL={img_url}")

# Save updated processed IDs
with open(processed_ids_file, 'w') as f:
    f.write("\n".join(processed_ids))
