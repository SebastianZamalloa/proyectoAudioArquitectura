import copy
from pyaudio import PyAudio, paInt16
from threading import Thread
import numpy as np
import sys


class AudioAnalyzer(Thread):
    SAMPLING_RATE = 48000
    CHUNK_SIZE = 1024
    BUFFER_TIMES = 50 
    ZERO_PADDING = 3
    NUM_HPS = 3 

    NOTE_NAMES = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']

    def __init__(self, queue, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)

        self.queue = queue  
        self.buffer = np.zeros(self.CHUNK_SIZE * self.BUFFER_TIMES)
        self.hanning_window = np.hanning(len(self.buffer))
        self.running = False

        try:
            self.audio_object = PyAudio()
            self.stream = self.audio_object.open(format=paInt16,
                                                 channels=1,
                                                 rate=self.SAMPLING_RATE,
                                                 input=True,
                                                 output=False,
                                                 frames_per_buffer=self.CHUNK_SIZE)
        except Exception as e:
            sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))
            return

    @staticmethod
    def frequency_to_number(freq, a4_freq):
        if freq == 0:
            sys.stderr.write("Error: No hay frecuencia, el sistema no reconoce la entrada de audio\n")
            return 0
        return 12 * np.log2(freq / a4_freq) + 69

    @staticmethod
    def number_to_frequency(number, a4_freq):
        return a4_freq * 2.0**((number - 69) / 12.0)

    @staticmethod
    def number_to_note_name(number):
        return AudioAnalyzer.NOTE_NAMES[int(round(number) % 12)]

    @staticmethod
    def frequency_to_note_name(frequency, a4_freq):
        number = AudioAnalyzer.frequency_to_number(frequency, a4_freq)
        note_name = AudioAnalyzer.number_to_note_name(number)
        return note_name

    def run(self):
        self.running = True

        while self.running:
            try:                
                data = self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False)
                data = np.frombuffer(data, dtype=np.int16)

                self.buffer[:-self.CHUNK_SIZE] = self.buffer[self.CHUNK_SIZE:]
                self.buffer[-self.CHUNK_SIZE:] = data

                magnitude_data = abs(np.fft.fft(np.pad(self.buffer * self.hanning_window,
                                                       (0, len(self.buffer) * self.ZERO_PADDING),
                                                       "constant")))
                magnitude_data = magnitude_data[:int(len(magnitude_data) / 2)]
                magnitude_data_orig = copy.deepcopy(magnitude_data)
                for i in range(2, self.NUM_HPS+1, 1):
                    hps_len = int(np.ceil(len(magnitude_data) / i))
                    magnitude_data[:hps_len] *= magnitude_data_orig[::i]  

                frequencies = np.fft.fftfreq(int((len(magnitude_data) * 2) / 1),
                                             1. / self.SAMPLING_RATE)
                
                for i, freq in enumerate(frequencies):
                    if freq > 60:
                        magnitude_data[:i - 1] = 0
                        break

                self.queue.put(round(frequencies[np.argmax(magnitude_data)], 2))

            except Exception as e:
                sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))

        self.stream.stop_stream()
        self.stream.close()
        self.audio_object.terminate()


if __name__ == "__main__":
    from analizer.threading_helper import ProtectedList
    import time

    q = ProtectedList()
    a = AudioAnalyzer(q)
    a.start()

    while True:
        q_data = q.get()
        if q_data is not None:
            print("loudest frequency:", q_data, "nearest note:", a.frequency_to_note_name(q_data, 440))
            time.sleep(0.02)
