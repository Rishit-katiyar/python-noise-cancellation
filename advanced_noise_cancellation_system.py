import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
CHUNK_SIZE = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Format of audio samples (16-bit PCM)
CHANNELS = 1  # Number of audio channels (mono)
RATE = 44100  # Sampling rate (samples per second)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Initialize input and output streams
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                          input=True, frames_per_buffer=CHUNK_SIZE)
output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                           output=True, frames_per_buffer=CHUNK_SIZE)

# Check if streams are active
if not input_stream.is_active():
    print("Error: Input stream is not active.")
    exit()

if not output_stream.is_active():
    print("Error: Output stream is not active.")
    exit()

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

    # Write data to speakers
    output_stream.write(mic_data)

    # Compute FFT of microphone and speaker signals
    mic_fft = np.abs(np.fft.rfft(mic_data))
    spk_fft = np.abs(np.fft.rfft(mic_data))

    # Update plots
    line_mic_wave.set_ydata(mic_data)
    line_spk_wave.set_ydata(mic_data)
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
