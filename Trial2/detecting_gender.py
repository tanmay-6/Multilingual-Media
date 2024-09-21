# import parselmouth
# import numpy as np

# # Function to detect pitch
# def get_pitch(audio_file):
#     sound = parselmouth.Sound(audio_file)
#     pitch = sound.to_pitch()

#     # Extract all pitch values (ignoring unvoiced segments)
#     pitch_values = pitch.selected_array['frequency']
#     pitch_values = pitch_values[pitch_values != 0]  # Removing zero values (unvoiced segments)

#     # Calculate average pitch
#     avg_pitch = np.mean(pitch_values)
#     return avg_pitch

# # Function to classify gender based on average pitch
# def classify_gender(pitch_value):
#     if pitch_value < 165:
#         return "Male"
#     else:
#         return "Female"

# # Load your audio file
# audio_file = 'aud1.wav'
# average_pitch = get_pitch(audio_file)
# gender = classify_gender(average_pitch)

# print(f"Average Pitch: {average_pitch:.2f} Hz")
# print(f"Detected Gender: {gender}")

import parselmouth
import numpy as np
import matplotlib.pyplot as plt

# Function to detect pitch for each time frame
def get_pitch_per_frame(audio_file, time_step=0.5):
    sound = parselmouth.Sound(audio_file)
    pitch = sound.to_pitch(time_step=time_step)

    # Extract pitch values and time stamps
    pitch_values = pitch.selected_array['frequency']
    times = pitch.xs()

    # Filter out unvoiced segments (pitch == 0)
    voiced_times = times[pitch_values != 0]
    pitch_values = pitch_values[pitch_values != 0]

    return voiced_times, pitch_values

# Function to classify gender based on pitch
def classify_gender(pitch_value):
    if pitch_value < 165:  # Threshold for classifying male vs female
        return "Male"
    else:
        return "Female"

# Function to detect gender changes
def detect_gender_changes(audio_file, time_step=0.5):
    times, pitch_values = get_pitch_per_frame(audio_file, time_step)

    # Classify gender for each pitch value
    gender_classifications = [classify_gender(pitch) for pitch in pitch_values]

    # Track changes in gender over time
    last_gender = None
    gender_changes = []

    for i, gender in enumerate(gender_classifications):
        if gender != last_gender:
            gender_changes.append((gender, times[i]))  # Record when the gender changes
            last_gender = gender

    return gender_changes

# Load your audio file
audio_file = 'aud1.wav'

# Detect gender changes with a time step of 0.5 seconds
gender_changes = detect_gender_changes(audio_file, time_step=0.5)

# Print results
for gender, time in gender_changes:
    print(f"Time: {time:.2f} sec, Gender: {gender}")
