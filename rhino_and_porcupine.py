import argparse
import os
import struct
from datetime import datetime
from threading import Thread

import numpy as np
import pvporcupine
import pvrhino
import pyaudio
import soundfile

#file for taking photo and running cnn
from photo import photoMain

class VoiceAssistant(Thread):
    """
    Voice Assistant for handling both wake word detection and intent inference.
    """

    def __init__(
            self,
            porcupine_library_path,
            porcupine_model_path,
            porcupine_keyword_paths,
            porcupine_sensitivities,
            rhino_library_path,
            rhino_model_path,
            rhino_context_path,
            audio_device_index=None,
            output_path=None):

        super(VoiceAssistant, self).__init__()

        self._porcupine_library_path = porcupine_library_path
        self._porcupine_model_path = porcupine_model_path
        self._porcupine_keyword_paths = porcupine_keyword_paths
        self._porcupine_sensitivities = porcupine_sensitivities

        self._rhino_library_path = rhino_library_path
        self._rhino_model_path = rhino_model_path
        self._rhino_context_path = rhino_context_path

        self._audio_device_index = audio_device_index

        self._output_path = output_path
        if self._output_path is not None:
            self._recorded_frames = []

        self._is_wake_word_detected = False
        self._last_detected_time = None
        self._max_command_duration = 5  # Maximum duration of the command in seconds
        self._command_started_time = None

    def run(self):
        porcupine = None
        rhino = None
        pa = None
        audio_stream = None
        
        
        keywords = list()
        for x in self._porcupine_keyword_paths:
            keywords.append(os.path.basename(x).replace('.ppn', '').split('_')[0])

        try:
            # Initialize Porcupine wake word engine
            porcupine = pvporcupine.create(
                library_path=self._porcupine_library_path,
                model_path=self._porcupine_model_path,
                keyword_paths=self._porcupine_keyword_paths,
                sensitivities=self._porcupine_sensitivities)

            # Initialize Rhino Speech-to-Intent engine
            rhino = pvrhino.create(
                library_path=self._rhino_library_path,
                model_path=self._rhino_model_path,
                context_path=self._rhino_context_path)

            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._audio_device_index)

            print(rhino.context_info)
            print()
            print('Listening {')
            for keyword, sensitivity in zip(keywords, self._porcupine_sensitivities):
                print('  %s (%.2f)' % (keyword, sensitivity))
            print('}')

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                # Porcupine processing
                porcupine_result = porcupine.process(pcm)
                if porcupine_result >= 0:
                    print('[%s] Wake word detected' % str(datetime.now()))
                    self._is_wake_word_detected = True
                    self._last_detected_time = datetime.now()
                    self._command_started_time = datetime.now()

                # Rhino processing
                if self._is_wake_word_detected:
                    is_finalized = rhino.process(pcm)
                    if is_finalized:
                        inference = rhino.get_inference()
                        if inference.is_understood:
                            print('{')
                            print("  intent : '%s'" % inference.intent)
                            print('  slots : {')
                            for slot, value in inference.slots.items():
                                print("    %s : '%s'" % (slot, value))
                            print('  }')
                            print('}\n')
                            photoMain()
                        else:
                            print("Didn't understand the command.\n")

                    # Check if the command duration has exceeded the maximum allowed duration
                    if (datetime.now() - self._command_started_time).total_seconds() > self._max_command_duration:
                        self._is_wake_word_detected = False

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if rhino is not None:
                rhino.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

    @classmethod
    def show_audio_devices(cls):
        fields = ('index', 'name', 'defaultSampleRate', 'maxInputChannels')

        pa = pyaudio.PyAudio()

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in fields))

        pa.terminate()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--porcupine_library_path', help='Absolute path to Porcupine dynamic library.', default=pvporcupine.LIBRARY_PATH)

    parser.add_argument(
        '--porcupine_model_path', help='Absolute path to Porcupine model file.', default=pvporcupine.MODEL_PATH)

    parser.add_argument(
        '--porcupine_keyword_paths', nargs='+', help='Absolute paths to Porcupine keyword model files.', default=[])

    parser.add_argument(
        '--porcupine_sensitivities',
        nargs='+',
        help='Sensitivities for detecting wake words.',
        type=float,
        default=[0.5])

    parser.add_argument(
        '--rhino_library_path', help='Absolute path to Rhino dynamic library.', default=pvrhino.LIBRARY_PATH)

    parser.add_argument(
        '--rhino_model_path',
        help='Absolute path to the file containing Rhino model parameters.',
        default=pvrhino.MODEL_PATH)

    parser.add_argument('--rhino_context_path', help='Absolute path to Rhino context file.')

    parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=None)

    args = parser.parse_args()

    assistant = VoiceAssistant(
        porcupine_library_path=args.porcupine_library_path,
        porcupine_model_path=args.porcupine_model_path,
        porcupine_keyword_paths=args.porcupine_keyword_paths,
        porcupine_sensitivities=args.porcupine_sensitivities,
        rhino_library_path=args.rhino_library_path,
        rhino_model_path=args.rhino_model_path,
        rhino_context_path=args.rhino_context_path,
        audio_device_index=args.audio_device_index)

    assistant.run()


if __name__ == '__main__':
    main()
