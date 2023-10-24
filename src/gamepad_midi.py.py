import pygame
import mido
import tkinter as tk
from tkinter import ttk, messagebox

class GamepadMidiApp:
    def __init__(self, main_window):
        self.root = main_window
        self.root.title("Gamepad to MIDI")

        # Calculate window size based on screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.2)
        window_height = int(screen_height * 0.6)
        self.root.geometry(f"{window_width}x{window_height}")

        # Center the window on the screen
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"+{x_position}+{y_position}")

        self.joystick = None
        self.outport = None

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TListbox", font=("Helvetica", 12))

        self.label_gamepad = ttk.Label(self.root, text="Select a gamepad:")
        self.label_gamepad.pack(pady=10)
        self.gamepad_listbox = tk.Listbox(self.root, exportselection=False, width=40, height=10)
        self.gamepad_listbox.pack()

        self.label_midi = ttk.Label(self.root, text="Select a MIDI output port:")
        self.label_midi.pack(pady=10)
        self.midi_listbox = tk.Listbox(self.root, exportselection=False, width=40, height=10)
        self.midi_listbox.pack()

        self.refresh_button = ttk.Button(self.root, text="Refresh", command=self.populate_lists)
        self.refresh_button.pack(pady=10)

        self.check_mapping_button = ttk.Button(self.root, text="Check Gamepad Mapping", command=self.check_gamepad_mapping)
        self.check_mapping_button.pack(pady=10)

        self.start_button = ttk.Button(self.root,
                                       text="Start MIDI Connection",
                                       command=self.start_midi)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root,
                                      text="Stop MIDI Connection",
                                      command=self.stop_midi,
                                      state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        self.running = False
        self.populate_lists()

        self.midi_id = None

        self.last_pressed = tk.StringVar(value="Press a gamepad button...")

        # Default note mappings (C Major scale)
        self.note_values = {
            'buttons': [60, 62, 64, 65, 67, 69, 71, 72],
            'axis': {
                0: 74,  # Left analog stick horizontal
                1: 75,  # Left analog stick vertical
                4: 76,  # L2 trigger
                3: 78,  # Right analog stick horizontal
                5: 79   # R2 trigger
            },
            'hat': {
                (1, 0): 77,   # D-pad right
                (-1, 0): 79,  # D-pad left
                (0, 1): 81,   # D-pad down
                (0, -1): 83   # D-pad up
            }
        }

        self.mapping_window = None
        self.mapping_label = None
        self.mapping_text = None

    def populate_lists(self):
        self.populate_gamepad_list()
        self.populate_midi_list()

    def populate_gamepad_list(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        self.gamepad_listbox.delete(0, tk.END)
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            self.gamepad_listbox.insert(tk.END, joystick.get_name())

    def populate_midi_list(self):
        self.midi_listbox.delete(0, tk.END)
        for name in mido.get_output_names():
            self.midi_listbox.insert(tk.END, name)

    def create_mapping_window(self):
        self.mapping_window = tk.Toplevel(self.root)
        self.mapping_window.title("Gamepad Mapping")

        self.mapping_label = ttk.Label(self.mapping_window, text="Gamepad Events:")
        self.mapping_label.pack()

        self.mapping_text = tk.Text(self.mapping_window, wrap=tk.WORD, font=("Helvetica", 12))
        self.mapping_text.pack()

    def check_gamepad_mapping(self):
        if not self.running:
            messagebox.showwarning("Warning", "Please start the MIDI connection before checking gamepad mappings.")
            return

        if self.mapping_window is None or not self.mapping_window.winfo_exists():
            self.create_mapping_window()

        pygame.init()  # Initialize the video system

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    self.mapping_text.insert(tk.END, f"Button {event.button} pressed\n")
                elif event.type == pygame.JOYBUTTONUP:
                    self.mapping_text.insert(tk.END, f"Button {event.button} released\n")
                elif event.type == pygame.JOYAXISMOTION:
                    self.mapping_text.insert(tk.END, f"Axis {event.axis} value: {event.value}\n")
                elif event.type == pygame.JOYHATMOTION:
                    self.mapping_text.insert(tk.END, f"D-pad: {event.value}\n")

            # Automatically scroll down
            self.mapping_text.see(tk.END)

            # Highlight the last printed event
            self.mapping_text.tag_add("highlight", "end-2l", "end-1l")

            self.mapping_text.update()
            self.mapping_window.update_idletasks()
            self.mapping_window.update()

            if self.mapping_window is None or not self.mapping_window.winfo_exists():
                break

    def start_midi(self):
        if self.running:
            return

        pygame.init()

        if pygame.joystick.get_count() == 0:
            messagebox.showerror("Error", "No gamepads detected.")
            return

        gamepad_index = self.gamepad_listbox.curselection()
        midi_port_index = self.midi_listbox.curselection()

        if len(gamepad_index) == 0 or len(midi_port_index) == 0:
            messagebox.showerror("Error", "Please select both a gamepad and a MIDI output port.")
            return

        gamepad_index = gamepad_index[0]
        midi_port_name = self.midi_listbox.get(midi_port_index[0])

        self.joystick = pygame.joystick.Joystick(gamepad_index)
        self.joystick.init()

        self.outport = mido.open_output(midi_port_name)

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.root.after(10, self.poll_midi_events)

    def stop_midi(self):
        self.running = False
        pygame.quit()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def determine_midi_note(self, event):
        if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]:
            return self.note_values['buttons'][event.button % 8]
        elif event.type == pygame.JOYAXISMOTION:
            return self.note_values['axis'].get(event.axis)
        elif event.type == pygame.JOYHATMOTION:
            return self.note_values['hat'].get(event.value)
        return None

    def poll_midi_events(self):
        if not self.running:
            return

        for event in pygame.event.get():
            note = self.determine_midi_note(event)
            if note is None:
                continue

            if event.type == pygame.JOYBUTTONDOWN:
                self.outport.send(mido.Message('note_on', note=note, velocity=64))
            elif event.type == pygame.JOYBUTTONUP:
                self.outport.send(mido.Message('note_off', note=note, velocity=64))
            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > 0.6:
                    self.outport.send(mido.Message('note_on', note=note, velocity=64))
                else:
                    self.outport.send(mido.Message('note_off', note=note, velocity=64))
            elif event.type == pygame.JOYHATMOTION:
                # Since the value is a tuple, we just check if it's not the neutral position
                if event.value != (0, 0):
                    self.outport.send(mido.Message('note_on', note=note, velocity=64))
                else:
                    self.outport.send(mido.Message('note_off', note=note, velocity=64))

        self.root.after(10, self.poll_midi_events)

if __name__ == '__main__':
    app_root = tk.Tk()
    app = GamepadMidiApp(app_root)
    app_root.mainloop()
