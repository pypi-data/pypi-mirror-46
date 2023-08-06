import argparse
from urllib.request import urlopen
import io
import tarfile

import ipa_recognizer
from ipa_recognizer.am import *
from ipa_recognizer.feature import *
from ipa_recognizer.audio import *
from ipa_recognizer.decode import *
import os

def download_model(model_name):
    model_dir = (Path(ipa_recognizer.__file__).parent) / 'model'

    if not (model_dir / model_name).exists():
        url = 'http://islpc21.is.cs.cmu.edu/xinjianl/ipa_recognizer/model/'+model_name+'.tar.gz'
        print("downloading model ...")
        print("from: ", url)
        print("to:   ", str(model_dir))
        resp = urlopen(url)
        compressed_files = io.BytesIO(resp.read())
        files = tarfile.open(fileobj=compressed_files)
        files.extractall(str(model_dir))

    return model_dir / model_name


class Recognizer:

    def __init__(self, model_name='english'):

        # ensure model is available
        self.model_dir = download_model(model_name)

        am_path = self.model_dir / 'model.npy'
        mfcc_path = self.model_dir / 'feature.json'

        self.am_model = BLSTM(am_path)
        self.mfcc = create_feature_model(mfcc_path)
        self.decoder = create_decoder(self.model_dir / 'units.txt')


    def recognize(self, audio_path, blank_factor=0.8, no_remove=False):

        # load audio
        audio = read_wav(audio_path)

        # get feature
        raw_feat = self.mfcc.compute(audio)

        aug_feat = np.concatenate((np.roll(raw_feat, 1, axis=0), raw_feat, np.roll(raw_feat, -1, axis=0)), axis=1)
        feat = aug_feat[::3, ]

        # run acoustic model
        logits = self.am_model.inference(feat)

        # decode phone
        phones = self.decoder.decode_phone(logits, blank_factor, no_remove=no_remove)

        return phones

    def logits(self, audio_path, blank_factor=0.8):

                # load audio
        audio = read_wav(audio_path)

        # get feature
        raw_feat = self.mfcc.compute(audio)

        aug_feat = np.concatenate((np.roll(raw_feat, 1, axis=0), raw_feat, np.roll(raw_feat, -1, axis=0)), axis=1)
        feat = aug_feat[::3, ]

        # run acoustic model
        logits = self.am_model.inference(feat)

        return logits