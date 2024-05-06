# YouTube Transcript Downloader

This script allows you to download the transcripts of YouTube videos either individually or from a playlist. It utilizes the `youtube_transcript_api` to fetch the transcripts and `pytube` to fetch video details. The downloaded transcripts are saved as text files.

## Prerequisites

- Python 3.x
- `pip` package manager

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/LuxuryTimepiece/YouTubeTranscriptDownloader.git
   ```

2. Install the required dependencies:

   ```bash
   pip install pytube youtube_transcript_api
   ```

## Usage

1. Run the script:

   ```bash
   python YouTubeTranscriptDownloader.py
   ```

2. Enter the YouTube video ID or playlist URL when prompted.
3. Click the corresponding button to add the video/playlist to the download queue.
4. Once you've added all the videos you want to download, click the "Start Download" button to begin downloading the transcripts.
5. The transcripts will be saved in the specified directory (you will be prompted to select a directory if not already specified).

## Note

- If a video does not have a transcript available, the script will display a message indicating so.
- Ensure you have the necessary permissions to download transcripts for the videos you intend to process.

