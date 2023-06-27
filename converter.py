import subprocess
import os
import re

class Containers:
   MP4 = 'mp4'
   MOV = 'mov'
   AVI = 'avi'
   MKV = 'mkv'
   FLV = 'flv'
   WEBM = 'webm'
   OGG = 'ogg'
   MPEG = 'mpeg'

class Codecs:
   H264 = 'libx264'
   H265 = 'libx265'
   H264_NVENC = 'h264_nvenc'
   H265_NVENC = 'hevc_nvenc'
   VP8 = 'libvpx'
   VP9 = 'libvpx-vp9'
   AV1 = 'libaom-av1'
   MPEG2 = 'mpeg2video'
   MPEG4 = 'mpeg4'
   THEORA = 'libtheora'
   WMV = 'wmv2'
   PRORES = 'prores'
   DNxHD = 'dnxhd'
   DNxHR = 'dnxhr'

class Bitrates:
   ORIGINAL = None
   LOW = '500k'
   MEDIUM = '1000k'
   HIGH = '2000k'
   HD = '5000k'
   FULLHD = '10000k'
   UHD_4K = '35000k'

class Resolutions:
    Original = None
    SD = '720x480'
    HD = '1280x720'
    FULLHD = '1920x1080'
    UHD_4K = '3840x2160'
    UHD_8K = '7680x4320'

def convert_video(input_video, output_video=None, new_fps=None, new_bitrate=None, new_resolution=None, new_codec=None, new_container=None, folder=None, callback=None):
   
   video_name = os.path.splitext(os.path.basename(input_video))[0]
   valid_name=video_name.replace(" ", "_")
   if not output_video:
      if new_container is not None:
         output_video = valid_name + "_output." + new_container
      else:
         output_video = "output." + input_video.split('.')[-1]
   
   if folder:
      output_video = os.path.join(folder, output_video)
   
   command = f"ffmpeg -y -i {input_video}"

   if new_fps:
      command += f' -r {new_fps}'
   
   if new_bitrate:
      command += f' -b:v {new_bitrate}'
   
   if new_resolution:
      if not isinstance(new_resolution, str):
         new_resolution = f'{new_resolution[0]}x{new_resolution[1]}'
      command += f' -s {new_resolution}'
   
   if new_codec:
      command += f' -c:v {new_codec}'

   command += f' {output_video}'

   process =subprocess.Popen(command,shell = True, stderr=subprocess.PIPE, universal_newlines=True)

   duration = None

   for line in process.stderr:
      # Extract duration
      match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
      if match is not None:
         hours, minutes, seconds, _ = map(int, match.groups())
         duration = hours * 3600 + minutes * 60 + seconds
         continue

      # Extract time
      match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})", line)
      if match is not None and duration is not None:
         hours, minutes, seconds, _ = map(int, match.groups())
         time = hours * 3600 + minutes * 60 + seconds
         progress = (time/duration) * 100
         if callback:
            callback( progress )

   output,error= process.communicate( input="y")
   rc = process.returncode
   if rc is not None:  
      if rc == 0:
         return True
      else:
         return False

