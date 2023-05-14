import json
from flask import Flask, request
from pytube import YouTube

app = Flask(__name__)

@app.route('/api/download/videolink', methods=['GET'])
def download_links():
    video_url = request.args.get('videolink')
    if video_url:
        links = get_download_links(video_url)
        if links:
            # Convert links to JSON
            json_response = json.dumps(links)
            return json_response
        else:
            return "Error: Failed to fetch download links."
    else:
        return "Error: Video link parameter is missing."

def get_download_links(url):
    try:
        # Create a YouTube object
        video = YouTube(url)

        # Get all available streams
        streams = video.streams

        # Create a list to store the download links
        download_links = []

        # Iterate over each stream
        for stream in streams:
            # Get the stream format and size
            format = stream.mime_type.split("/")[1]
            size = stream.filesize_approx / (1024 * 1024)  # Convert to MB

            # Append the format and size along with the download link
            download_links.append({"format": format, "size": size, "url": stream.url})

        return download_links

    except Exception as e:
        print("Error:", str(e))

# This is required to run the Flask app on Vercel
if __name__ == '__main__':
    app.run()
