import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
CHUNK_SIZE = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Format of audio samples (16-bit PCM)
CHANNELS = 1  # Number of audio channels (mono)
RATE = 44100  # Sampling rate (samples per second)
AMPLIFICATION_FACTOR = 2  # Increase the volume by a factor of 2

# Parameters for adaptive filtering
FILTER_LENGTH = 1024  # Length of adaptive filter
LEARNING_RATE = 0.01  # Learning rate for adaptive filter

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open input stream (microphone)
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                          input=True, frames_per_buffer=CHUNK_SIZE)

# Open output stream (speakers)
output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                           output=True, frames_per_buffer=CHUNK_SIZE)

# Check if streams are active
if not input_stream.is_active():
    print("Error: Input stream is not active.")
    exit()

if not output_stream.is_active():
    print("Error: Output stream is not active.")
    exit()

# Initialize adaptive filter coefficients
w = np.zeros(FILTER_LENGTH)

# Initialize plots
fig, ((ax_mic_wave, ax_mic_freq), (ax_spk_wave, ax_spk_freq)) = plt.subplots(2, 2, figsize=(12, 8))

time = np.arange(0, CHUNK_SIZE) / RATE * 1000  # Time in milliseconds
freq = np.fft.rfftfreq(CHUNK_SIZE, 1 / RATE)  # Frequency bins

line_mic_wave, = ax_mic_wave.plot(time, np.zeros(CHUNK_SIZE))
line_spk_wave, = ax_spk_wave.plot(time, np.zeros(CHUNK_SIZE))
line_mic_freq, = ax_mic_freq.plot(freq, np.zeros(CHUNK_SIZE // 2 + 1))
line_spk_freq, = ax_spk_freq.plot(freq, np.zeros(CHUNK_SIZE // 2 + 1))

ax_mic_wave.set_title('Microphone Signal (Time Domain)')
ax_mic_wave.set_xlabel('Time (ms)')
ax_mic_wave.set_ylabel('Amplitude')
ax_mic_wave.set_xlim(0, CHUNK_SIZE / RATE * 1000)
ax_mic_wave.set_ylim(-32768, 32767)

ax_mic_freq.set_title('Microphone Signal (Frequency Domain)')
ax_mic_freq.set_xlabel('Frequency (Hz)')
ax_mic_freq.set_ylabel('Magnitude')
ax_mic_freq.set_xlim(0, RATE / 2)
ax_mic_freq.set_ylim(0, 100)

ax_spk_wave.set_title('Speaker Signal (Time Domain)')
ax_spk_wave.set_xlabel('Time (ms)')
ax_spk_wave.set_ylabel('Amplitude')
ax_spk_wave.set_xlim(0, CHUNK_SIZE / RATE * 1000)
ax_spk_wave.set_ylim(-32768, 32767)

ax_spk_freq.set_title('Speaker Signal (Frequency Domain)')
ax_spk_freq.set_xlabel('Frequency (Hz)')
ax_spk_freq.set_ylabel('Magnitude')
ax_spk_freq.set_xlim(0, RATE / 2)
ax_spk_freq.set_ylim(0, 100)

# Function to update plots
def update_plot(frame):
    # Read data from microphone
    mic_data = np.frombuffer(input_stream.read(CHUNK_SIZE), dtype=np.int16)

    # Amplify the microphone data
    mic_data_amplified = mic_data * AMPLIFICATION_FACTOR

    # Write amplified data to speakers
    output_stream.write(mic_data_amplified)

    # Apply adaptive filter to cancel out speaker audio from microphone
    # (we don't need to read from the output stream)
    # Estimate the speaker audio in the microphone signal
    y = np.convolve(w, mic_data_amplified)[:CHUNK_SIZE]

    # Filter the microphone signal to remove speaker audio
    filtered_mic_data = mic_data_amplified - y

    # Compute FFT of microphone and speaker signals
    mic_fft = np.abs(np.fft.rfft(filtered_mic_data))
    spk_fft = np.abs(np.fft.rfft(y))

    # Update plots
    line_mic_wave.set_ydata(filtered_mic_data)
    line_spk_wave.set_ydata(y)
    line_mic_freq.set_ydata(mic_fft)
    line_spk_freq.set_ydata(spk_fft)

    return line_mic_wave, line_spk_wave, line_mic_freq, line_spk_freq

# Update plots every frame
ani = FuncAnimation(fig, update_plot, blit=True, interval=100)

plt.tight_layout()
plt.show()

# Close streams
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()

# Terminate PyAudio
audio.terminate()
