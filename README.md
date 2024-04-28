# Python Noise Cancellation Project 🎧🔇

Welcome to the Python Noise Cancellation Project! This project aims to cancel out noise from audio recordings using adaptive filtering techniques.

## Overview

This project utilizes the PyAudio library for audio input/output and implements adaptive filtering to cancel out background noise from microphone recordings. The noise-cancelled audio is then played through the speakers.

## Features

- Real-time noise cancellation
- Visualization of microphone and speaker signals
- Adjustable volume and microphone sensitivity

![Figure_10](https://github.com/Rishit-katiyar/python-noise-cancellation/assets/167756997/ccc7b993-1cad-493c-b3ac-dfedfcdac138)

## Installation

To run this project, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Rishit-katiyar/python-noise-cancellation.git
   ```

2. Navigate to the project directory:

   ```bash
   cd python-noise-cancellation
   ```

3. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. If you encounter issues with PyAudio installation, you may need to install additional system dependencies. Refer to the [PyAudio installation instructions](https://people.csail.mit.edu/hubert/pyaudio/docs/#installation) for details.

## Usage

1. Execute the script using the provided instructions.
2. Adjust the microphone sensitivity and volume as needed.
3. Speak into the microphone and observe the noise cancellation in action!
4. Use the following buttons for additional functionality:
   - **Start**: Begins real-time noise cancellation and audio playback.
   - **Stop**: Pauses noise cancellation and audio playback.
   - **Adjust Volume**: Use the volume slider to adjust the output volume.
   - **Microphone Sensitivity**: Use the sensitivity slider to adjust the microphone sensitivity.
   - **Save Recording**: Save the noise-cancelled audio recording to a file.
   - **Reset**: Reset all settings to their default values.

## Troubleshooting

If you encounter any issues while running the script, try the following troubleshooting steps:

- **No Audio Output**:
  - Ensure that your speakers are connected properly and turned on.
  - Check your system's audio settings to ensure that the correct output device is selected.
  - Adjust the volume using the volume slider in the application.

- **No Audio Input**:
  - Ensure that your microphone is connected properly and recognized by your system.
  - Check your system's audio settings to ensure that the correct input device is selected.
  - Adjust the microphone sensitivity using the sensitivity slider in the application.

- **Audio Quality Issues**:
  - Check for any background noise sources near the microphone and try to minimize them.
  - Adjust the microphone sensitivity and volume settings to optimize audio quality.

- **PyAudio Installation Issues**:
  - If PyAudio installation fails, ensure that you have the necessary system dependencies installed. Refer to the PyAudio installation instructions for details.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
