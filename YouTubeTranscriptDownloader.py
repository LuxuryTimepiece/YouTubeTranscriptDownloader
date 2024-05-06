import tkinter as tk
from tkinter import scrolledtext, filedialog
save_directory = ''
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import threading
from queue import Queue
from pytube import YouTube, Playlist

# Function to download the transcript of a given YouTube video
def download_transcript(video_id, video_title):
    try:
        # Attempt to fetch the transcript of the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        transcript_data = transcript.fetch()

        # Convert the fetched transcript into text
        transcript_text = "\n".join([item['text'] for item in transcript_data])

        # Save the transcript to a file named after the video title
        with open(f"{save_directory}/{video_title}_transcript.txt", "w", encoding='utf-8') as file:
            file.write(transcript_text)

        return f"Transcript downloaded for: {video_title}"

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcript found for this video."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to process each item in the queue
def process_queue():
    while not video_queue.empty():
        # Get the next video ID and title from the queue
        video_id, video_title = video_queue.get()
        # Download the transcript and get the status message
        message = download_transcript(video_id, video_title)
        # Update the status in the GUI
        update_status(message)
        # Mark the current task as done
        video_queue.task_done()
        # Remove the first item from the listbox in the GUI
        queue_display.delete(0)

# Function to update the status display in the GUI
def update_status(message):
    # Enable the text box, insert the message, and then disable it again
    status_display.config(state=tk.NORMAL)
    status_display.insert(tk.END, message + "\n")
    status_display.config(state=tk.DISABLED)

# Function to add a single video to the download queue
def add_to_queue():
    video_id = video_id_entry.get()
    if video_id:
        try:
            # Fetch the video title from YouTube
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            video_title = yt.title
            # Add the video ID and title to the queue
            video_queue.put((video_id, video_title))
            # Display the video title in the listbox
            queue_display.insert(tk.END, video_title)
            # Clear the text entry field
            video_id_entry.delete(0, tk.END)
        except Exception as e:
            update_status(f"An error occurred: {e}")

# Function to add all videos from a playlist to the download queue
def add_playlist_to_queue():
    playlist_url = playlist_entry.get()
    if playlist_url:
        try:
            # Fetch all videos from the given playlist URL
            pl = Playlist(playlist_url)
            for url in pl.video_urls:
                yt = YouTube(url)
                video_title = yt.title
                # Add each video to the queue
                video_queue.put((yt.video_id, video_title))
                # Display each video title in the listbox
                queue_display.insert(tk.END, video_title)
            # Clear the playlist URL entry field
            playlist_entry.delete(0, tk.END)
        except Exception as e:
            update_status(f"An error occurred: {e}")

# Function to start the download process in a separate thread
def start_download():
    global save_directory
    if not save_directory:
        save_directory = filedialog.askdirectory()
        if not save_directory:
            return  # User cancelled the directory selection
    threading.Thread(target=process_queue, daemon=True).start()
# Function to clear queue
def clear_queue():
    while not video_queue.empty():
        video_queue.get()
        video_queue.task_done()
    queue_display.delete(0, tk.END)
    update_status("Queue cleared.")
# Queue for storing video IDs and titles
video_queue = Queue()

# Creating the main window of the application
root = tk.Tk()
root.title("YouTube Transcript Downloader")

# Creating and packing widgets for video ID entry
video_label = tk.Label(root, text="Enter YouTube Video ID:")
video_label.pack()
video_id_entry = tk.Entry(root, width=50)
video_id_entry.pack()

# Creating and packing widgets for playlist URL entry
playlist_label = tk.Label(root, text="Enter YouTube Playlist URL:")
playlist_label.pack()
playlist_entry = tk.Entry(root, width=50)
playlist_entry.pack()

# Creating and packing the listbox to display the download queue
queue_label = tk.Label(root, text="Download Queue:")
queue_label.pack()
queue_display = tk.Listbox(root, width=50)
queue_display.pack()

# Creating and packing the status display
status_label = tk.Label(root, text="Status:")
status_label.pack()
status_display = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED)
status_display.pack()

# Creating and packing buttons for adding videos/playlists and starting downloads
add_video_button = tk.Button(root, text="Add Video to Queue", command=add_to_queue)
add_video_button.pack()
add_playlist_button = tk.Button(root, text="Add Playlist to Queue", command=add_playlist_to_queue)
add_playlist_button.pack()
download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack()
# clear the queue
clear_queue_button = tk.Button(root, text="Clear Queue", command=clear_queue)
clear_queue_button.pack()

# Starting the application
root.mainloop()
