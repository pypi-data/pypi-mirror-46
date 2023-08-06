import struct
import wave
import numpy as np
import subprocess
from pathlib import Path

def read_wav(filename, header_only=False):
    """
    read_audio will read a raw wav and return an Audio object

    :param header_only: only load header without frames
    """

    if isinstance(filename, Path):
        filename = str(filename)

    wf = wave.open(filename)

    # initialize audio
    audio = Audio()

    # set stream basic info
    channel_number = wf.getnchannels()

    # only handle channel number == 1
    audio.set_header(sample_rate=wf.getframerate(), frame_size=wf.getnframes(), channel_number=1, sample_width=wf.getsampwidth())

    # set audio
    x = wf.readframes(wf.getnframes())

    assert(channel_number <= 2)

    audio_bytes = np.frombuffer(x, dtype='int16')

    # get the first channel if stereo
    if channel_number == 2:
        audio_bytes = (audio_bytes[::2]+audio_bytes[1::2])/2

    audio.frames = audio_bytes

    wf.close()

    if audio.sample_rate != 8000:
        audio = resample_audio(audio, 8000)

    return audio


def resample_audio(audio, target_sample_rate):
    """
    resample the audio by the target_sample_rate

    :param audio:
    :param target_sample_rate:
    :return:
    """

    # return the origin audio if sample rate is identical
    if audio.sample_rate == target_sample_rate:
        return audio

    origin_rate = audio.sample_rate

    frame_point = 0.0
    resample_ratio = origin_rate/target_sample_rate

    new_frames = []

    while frame_point < len(audio.frames)-1:

        # down sampling
        new_frames.append(audio.frames[int(frame_point)])
        frame_point += resample_ratio

    # create new wave stream
    new_frames = np.array(new_frames)
    new_audio = Audio(new_frames, target_sample_rate)

    return new_audio

def split_audio(audio, frame_start, frame_end, frame_size, frame_step):
    """
    split an audio into multiple small audios

    :param audio: input wave stream
    :param frame_start: start frame
    :param frame_end: end frame
    :param frame_size: how many frames in each small wave stream
    :param frame_step: how many frames to move forward for each iteration
    :return:
    """

    audio_lst = []

    while frame_start + frame_size <= frame_end:

        new_audio = Audio()
        new_audio.set_header(sample_rate=audio.sample_rate, channel_number=audio.channel_number,
                             sample_width=audio.sample_width, frame_size=audio.frame_size)

        new_audio_frames = audio.frames[frame_start:frame_start+frame_size].copy()
        new_audio.set_frames(new_audio_frames)

        audio_lst.append(new_audio)

        # inc frame start for next iteration
        frame_start += frame_step

    return audio_lst

def split_stream_audio(audio, frame_step):
    """
    split an audio into multiple non-overlapping stream audios
    each stream audio starts from the first frame

    for example: splitting [1 2 3 4 5 6] with frame_step 2 will yield following audios
    1 2
    1 2 3 4
    1 2 3 4 5 6

    :param audio: target audio
    :param frame_step: how many frame to skip for each stream audio
    :return: stream audio list
    """

    audio_lst = []
    frame_start = 0
    frame_len = len(audio.frames)

    while frame_start < frame_len:

        new_audio = Audio()
        new_audio.set_header(sample_rate=audio.sample_rate, channel_number=audio.channel_number,
                             sample_width=audio.sample_width, frame_size=audio.frame_size)

        new_audio_frames = audio.frames[:frame_start+frame_step].copy()
        new_audio.set_frames(new_audio_frames)

        audio_lst.append(new_audio)

        # inc frame start for next iteration
        frame_start += frame_step

    return audio_lst


def slice_audio(audio, frame_start, frame_end, second=False):

    if second:
        frame_start = int(audio.sample_rate * frame_start)
        frame_end = int(audio.sample_rate * frame_end)

    new_audio = Audio()
    new_audio.set_header(sample_rate=audio.sample_rate, channel_number=audio.channel_number,
                         sample_width=audio.sample_width, frame_size=audio.frame_size)

    new_frames = audio.frames[frame_start:frame_end].copy()
    new_audio.set_frames(new_frames)

    return new_audio


def concatenate_audio(audio_lst, sample_rate=None):

    print(audio_lst[0].sample_rate)

    if sample_rate is None:
        sample_rate = audio_lst[0].sample_rate

    new_audio = Audio(sample_rate=sample_rate)

    frame_lst = []

    for audio in audio_lst:

        # resample
        if audio.sample_rate != sample_rate:
            audio = resample_audio(audio, sample_rate)

        frame_lst.append(audio.frames)

    frames = np.concatenate(frame_lst)
    new_audio.set_frames(frames)

    return new_audio


class Audio:

    def __init__(self, frames=[], sample_rate=8000):
        """
        Audio is the basic data structure used in this package.
        It is used to capture fundamental info about audio files such as frequency and frames.

        :param frames:
        :param sample_rate:
        :param stream_name:
        """

        # default parameters
        self.sample_rate = sample_rate
        self.channel_number = 1
        self.sample_width = 2

        # all frames
        self.set_frames(frames)

    def __str__(self):
        wave_info = "<Audio sample rate: "+str(self.sample_rate)+", frames: "\
                    + str(self.frame_size) + ", second: " + str(self.frame_size/self.sample_rate) + " > "
        return wave_info

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.frame_size

    def set_frames(self, frames):
        self.frames = frames
        self.frame_size = len(frames)

    def empty(self):
        return self.frames is None or self.frame_size == 0

    def clear(self):
        self.set_frames([])

    def extend(self, new_audio):
        """
        extend wave stream

        :param new_audio:
        :return:
        """

        # resample if sample_rate does not match
        if self.sample_rate != new_audio.sample_rate:
            audio =  resample_audio(new_audio, self.sample_rate)
            frames = audio.frames

        else:
            frames = new_audio.frames

        # extend
        new_frames = np.append(self.frames, frames)
        self.set_frames(new_frames)


    def set_header(self, sample_rate=8000, frame_size=0, channel_number=1, sample_width=2):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.channel_number = channel_number
        self.sample_width = sample_width

    def duration(self):
        return self.frame_size/self.sample_rate