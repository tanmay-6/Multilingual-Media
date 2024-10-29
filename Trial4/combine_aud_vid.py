from moviepy.editor import VideoFileClip, AudioFileClip

def add_audio_to_video(video_file, audio_file, output_file):
    # Load the video file
    video_clip = VideoFileClip(video_file)

    # Load the audio file
    audio_clip = AudioFileClip(audio_file)

    # Set the audio clip's duration to match the video if necessary
    audio_clip = audio_clip.subclip(0, min(audio_clip.duration, video_clip.duration))

    # Add the audio to the video
    final_video = video_clip.set_audio(audio_clip)

    # Write the output file
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Close the clips to release resources
    video_clip.close()
    audio_clip.close()
    final_video.close()

    print(f"Video with audio saved to {output_file}")

# Example usage
video_file = "Video.mp4"  # Replace with the path to your video file
audio_file = "output_audio.mp3"  # Replace with the path to your audio file
output_file = "output_with_audio.mp4"  # Desired output file

add_audio_to_video(video_file, audio_file, output_file)
