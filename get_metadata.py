import ffmpeg

def video_metadata(video_path):
    # Open the video file
    probe = ffmpeg.probe(video_path)

    # Get the video stream
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if video_stream is not None:
        # Get the resolution
        width = video_stream.get('width')
        height = video_stream.get('height')
        resolution = f"{width}x{height}"
        return f"Codec: {video_stream.get('codec_name')}  FPS: {video_stream.get('r_frame_rate')}  Bitrate: {video_stream.get('bit_rate')}  Resolution:{resolution} "
    else:
        return "No video stream found."