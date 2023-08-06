
import os
import sys
import time

if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

import threading
import signal

import numpy
import quiet
#from quiet.quiet import Decoder


class Decoder(object):
    def __init__(self):
        self.pyaudio_instance = None
        self.done = None
        self.thread = None
        self.queue = queue.Queue()

    def start(self):
        self.done = False
        if not (self.thread and self.thread.is_alive()):
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def put(self, data):
        self.queue.put(data)

    def run(self):
        decoder = quiet.Decoder(sample_rate=48000, profile_name='ultrasonic-experimental')

        while not self.done:
            audio = self.queue.get()
            audio = numpy.fromstring(audio, dtype='int16').astype('float32')
            data = decoder.decode(audio)
            if data is not None:
                self.on_data(data)

        #data = decoder.decode('', flush=True)
        #if data is not None:
        #    self.on_data(data)

    def stop(self):
        self.done = True
        self.queue.put('\0'*8)
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def on_data(self, data):
        print(data)


def main():
    # from voice_engine.source import Source
    from voice_engine.file_source import Source
    from voice_engine.channel_picker import ChannelPicker

    #src = Source(rate=48000, channels=4, device_name='ac108')
    src = Source(sys.argv[1], frames_size=8000)
    chn = ChannelPicker(channels=src.channels, pick=0)
    decoder = Decoder()


    def on_data(data):
        print(data.tostring().decode('utf-8'))


    # def int_handler(sig, frame):
    #     listener.stop()

    #signal.signal(signal.SIGINT, int_handler)

    decoder.on_data = on_data

    src.pipeline(chn, decoder)
    src.pipeline_start()

    while src.is_active():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('exit')
            break



    time.sleep(3)
    src.pipeline_stop()


if __name__ == '__main__':
    main()
