import tkinter
import tkinter.messagebox
import os
import sys
import json
import time
import numpy as np
import random

from analizer.audio_analyzer import AudioAnalyzer
from analizer.threading_helper import ProtectedList
from analizer.sound_thread import SoundThread

from appearanceManager.color_manager import ColorManager
from appearanceManager.image_manager import ImageManager
from appearanceManager.font_manager import FontManager
from appearanceManager.timing import Timer

from interface.main_frame import MainFrame

from settings import Settings


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):

        tkinter.Tk.__init__(self, *args, **kwargs)

        self.main_path = os.path.dirname(os.path.abspath(__file__))

        self.color_manager = ColorManager()
        self.font_manager = FontManager()
        self.image_manager = ImageManager(self.main_path)
        self.frequency_queue = ProtectedList()

        self.main_frame = MainFrame(self)

        self.audio_analyzer = AudioAnalyzer(self.frequency_queue)
        self.audio_analyzer.start()

        self.play_sound_thread = SoundThread(self.main_path + "/assets/sounds/drop.wav")
        self.play_sound_thread.start()

        self.timer = Timer(Settings.FPS)

        self.needle_buffer_array = np.zeros(Settings.NEEDLE_BUFFER_LENGTH)
        self.tone_hit_counter = 0
        self.note_number_counter = 0
        self.nearest_note_number_buffered = 69
        self.a4_frequency = 440

        self.dark_mode_active = False

        self.title(Settings.APP_NAME)
        self.geometry(str(Settings.WIDTH) + "x" + str(Settings.HEIGHT))
        self.resizable(True, True)
        self.minsize(Settings.WIDTH, Settings.HEIGHT)
        self.maxsize(Settings.MAX_WIDTH, Settings.MAX_HEIGHT)
        self.configure(background=self.color_manager.background_layer_1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if "win" in sys.platform: 
            self.bind("<Alt-Key-F4>", self.on_closing)

        self.draw_main_frame()

        self.open_app_time = time.time()

    @staticmethod
    def about_dialog():
        tkinter.messagebox.showinfo(title=Settings.APP_NAME,
                                    message=Settings.ABOUT_TEXT)

    def draw_settings_frame(self, event=0):
        self.main_frame.place_forget()

    def draw_main_frame(self, event=0):
        self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def write_user_setting(self, setting, value):
        with open(self.main_path + Settings.USER_SETTINGS_PATH, "r") as file:
            user_settings = json.load(file)

        user_settings[setting] = value

        with open(self.main_path + Settings.USER_SETTINGS_PATH, "w") as file:
            json.dump(user_settings, file)

    def read_user_setting(self, setting):
        with open(self.main_path + Settings.USER_SETTINGS_PATH) as file:
            user_settings = json.load(file)

        return user_settings[setting]

    def on_closing(self, event=0):
        self.audio_analyzer.running = False
        self.play_sound_thread.running = False
        self.destroy()

    def update_color(self):
        self.main_frame.update_color()

    def handle_appearance_mode_change(self):
        dark_mode_state = self.color_manager.detect_os_dark_mode()
        if dark_mode_state is not self.dark_mode_active:
            if dark_mode_state is True:
                self.color_manager.set_mode("Dark")
            else:
                self.color_manager.set_mode("Light")

            self.dark_mode_active = dark_mode_state
            self.update_color()

    def start(self):
        self.handle_appearance_mode_change()
        
        if self.read_user_setting("id") is None: self.write_user_setting("id", random.randint(10**20, (10**21)-1))  # generate random id
        self.write_user_setting("open_times", self.read_user_setting("open_times")+1)  # increase open_times counter

        while self.audio_analyzer.running:

            try:
                self.handle_appearance_mode_change()
                freq = self.frequency_queue.get()
                if freq is not None:
                    number = self.audio_analyzer.frequency_to_number(freq, self.a4_frequency)                    
                    
                    nearest_note_number = round(number)
                    nearest_note_freq = self.audio_analyzer.number_to_frequency(nearest_note_number, self.a4_frequency)

                    freq_difference = nearest_note_freq - freq
                    semitone_step = nearest_note_freq - self.audio_analyzer.number_to_frequency(round(number-1),
                                                                                                self.a4_frequency)
                    needle_angle = -90 * ((freq_difference / semitone_step) * 2)
                    if nearest_note_number != self.nearest_note_number_buffered:
                        self.note_number_counter += 1
                        if self.note_number_counter >= Settings.HITS_TILL_NOTE_NUMBER_UPDATE:
                            self.nearest_note_number_buffered = nearest_note_number
                            self.note_number_counter = 0

                    if abs(freq_difference) < 0.25:
                        self.main_frame.set_needle_color("green")
                        self.tone_hit_counter += 1
                    else:
                        self.main_frame.set_needle_color("red")
                        self.tone_hit_counter = 0

                    if self.tone_hit_counter > 7:
                        self.tone_hit_counter = 0

                    self.needle_buffer_array[:-1] = self.needle_buffer_array[1:]
                    self.needle_buffer_array[-1:] = needle_angle

                    self.main_frame.set_needle_angle(np.average(self.needle_buffer_array))
                    self.main_frame.set_note_names(note_name=self.audio_analyzer.number_to_note_name(self.nearest_note_number_buffered),
                                                   note_name_lower=self.audio_analyzer.number_to_note_name(self.nearest_note_number_buffered - 1),
                                                   note_name_higher=self.audio_analyzer.number_to_note_name(self.nearest_note_number_buffered + 1))

                    if semitone_step == 0:
                        diff_cents = 0
                    else:
                        diff_cents = (freq_difference / semitone_step) * 100
                    freq_label_text = f"+{round(-diff_cents, 1)} decibeles" if -diff_cents > 0 else f"{round(-diff_cents, 1)} decibeles"
                    self.main_frame.set_frequency_difference(freq_label_text)

                    if freq is not None: 
                        self.main_frame.set_frequency(freq)
                        self.main_frame.set_lvl(freq)

                self.update()
                self.timer.wait()

            except IOError as err:
                sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(err).__name__, err))
                self.update()
                self.timer.wait()


if __name__ == "__main__":
    app = App()
    app.start()
