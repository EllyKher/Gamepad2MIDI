# Gamepad to MIDI

This project allows you to use your gamepad (Xbox controllers by default) to generate MIDI signals, turning your gamepad into a musical controller. You can easily customize the mapping of gamepad buttons and axes to MIDI notes.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Compatibility](#compatibility)
- [Customization](#customization)
- [Mapping Checking](#mapping-checking)
- [Troubleshooting](#troubleshooting)
- [Additional Information](#additional-information)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Requirements

- Windows 10 (The development was done on Windows 10, but it might work on other Windows versions as well.)
- Python 3.6 or higher

## Installation

1. Clone or download this repository.

2. **Install Python:**

   If you don't have Python installed, you can download it from the official Python website: [Download Python](https://www.python.org/downloads/)

3. **Check Python Installation:**

   Open a terminal or command prompt and run the following commands to ensure Python is installed and accessible:
   python --version

This should display the installed Python version. If you encounter an error, please make sure Python is added to your system's PATH environment variable.

4. **Install the required Python packages:**
Use pip (Python's package manager) to install the necessary packages:
pip install pygame mido tkinter

This will install the required packages for the Gamepad to MIDI application.

5. **Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)**
This tool will allow you to create a virtual MIDI controller.


## Usage

1. Open loopMIDI and create a virtual MIDI port (e.g., "Gamepad MIDI").

2. Navigate to the Gamepad to MIDI Application Folder:

   Open a terminal or command prompt and use the `cd` command to navigate to the folder where you downloaded or cloned the Gamepad to MIDI application.

   cd path/to/gamepad-midi-folder

Replace path/to/gamepad-midi-folder with the actual path to the application folder.

3. Run the Gamepad to MIDI application by executing `gamepad_midi.py`:
python gamepad_midi.py

4. In the application's GUI, follow these steps:
- Select your gamepad from the "Select a gamepad" dropdown.
- Select the virtual MIDI port you created earlier from the "Select a MIDI output port" dropdown.
- Click the "Start MIDI Connection" button.

5. Your gamepad is now ready to generate MIDI signals. Press buttons and move analog sticks to trigger MIDI notes.

6. To stop the MIDI connection, click the "Stop MIDI Connection" button.

## Changing Compatibility from Xbox to DS4:

By default, this project is designed for Xbox controllers. 
In the script, you can change the compatibility from Xbox to DS4 by updating the note_values dictionary to match DS4 controller button and axis mappings. 
Here's how you can modify the code:

Before (Xbox compatibility):
note_values = {
    'buttons': [60, 62, 64, 65, 67, 69, 71, 72],  # C Major scale
    'axis': {
        0: 74,  # Left analog stick horizontal
        1: 75,  # Left analog stick vertical
        4: 76,  # L2 trigger
        3: 78   # Right analog stick horizontal
    },
    'hat': {
        (1, 0): 77,   # D-pad right
        (-1, 0): 79,  # D-pad left
        (0, 1): 81,   # D-pad down
        (0, -1): 83   # D-pad up
    }
}


After (DS4 compatibility):
note_values = {
    'buttons': [60, 62, 64, 65, 67, 69, 71, 72],  # C Major scale
    'axis': {
        0: 74,   # Left analog stick horizontal
        1: 75,   # Left analog stick vertical
        5: 76,   # R2 trigger (DS4 compatibility)
        3: 78    # Right analog stick horizontal
    },
    'hat': {
        (1, 0): 77,   # D-pad right
        (-1, 0): 79,  # D-pad left
        (0, 1): 81,   # D-pad down
        (0, -1): 83   # D-pad up
    }
}


You can find DS4 controller mappings online or use the provided [gamepad-mappings](https://gamepad-tester.com) website.


## Customization

### Changing the Default Note Mapping

The default note mapping corresponds to a C-major scale. You can customize this mapping by modifying the `note_values` dictionary in the code. The dictionary is organized into "buttons," "axis," and "hat" categories, allowing you to map different events to MIDI notes.

For example, here's how to change the note scale from C Major to D Major:

Before (C Major scale):
'buttons': [60, 62, 64, 65, 67, 69, 71, 72],  # C Major scale

After (D Major scale):
'buttons': [62, 64, 66, 67, 69, 71, 73, 74],  # D Major scale


### Mapping Checking

To check the mapping of your gamepad buttons and axes, you can use the "Check Gamepad Mapping" button in the application's GUI. It opens a window where you can see which buttons and axes are being pressed or moved on your gamepad.

## Troubleshooting

If you encounter issues with mapping or if a button is not recognized, consider the following troubleshooting steps:

- Ensure you have selected both a gamepad and a MIDI output port in the GUI before starting the MIDI connection.

- Check that your gamepad is properly connected and recognized by your operating system.

- Verify that loopMIDI is running and that you have created a virtual MIDI port.

- Double-check the `note_values` dictionary in the code to ensure your gamepad mappings match the actual controller.

## Additional Information

- You can use [MIDIVIEW](https://hautetechnique.com/midi/midiview/) to check if MIDI signals are being sent and to see which notes are mapped to which events.

- Feel free to contribute to this project or report issues on [GitHub](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME).

- Follow the developer on Twitter: [@kher_elena](https://twitter.com/kher_elena).

## Acknowledgments

This project is an expansion of the [original repository](https://github.com/k0rean-rand0m/gamepad-midi), with additional features and customization.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
