#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import os
from traceback import format_exc

import speech_recognition as sr
import pyttsx3

import argparse

from aichat.audio import record_audio, play_audio


# TODO move stt/tts to speech.py
def stt(audio, api='google'):
    r = sr.Recognizer()
    text = getattr(r, 'recognize_{}'.format(api), 'recognize_google')(audio)
    try:
        print("This is what {} thinks you said: ".format(api=api) + text)
    except LookupError:                            # speech is unintelligible
        print("ERROR: {} couldn't understand that.".format(api))
    return text


def tts(text, rate=200, voice='Alex'):
    engine = pyttsx3.init()
    voices = [v.id for v in engine.getProperty('voices')]
    voice_names = [v.split('.')[-1] for v in voices]
    if rate:
        engine.setProperty('rate', int(rate))
    if voice in voice_names:
        engine.setProperty('voice', voices[voice_names.index(voice)])
    else:
        voice = engine.getProperty('voice').split('.')[-1]
        print("WARN: Voice name '{}' not found.\n  Valid voice names: {}".format(voice, ' '.join(voices)))
        print("Using default voice named '{}'.".format(voice))
    engine.say(text)
    engine.runAndWait()
    return voice


def save_audio(audio, path='audio.wav'):
    data = getattr(audio, 'get_{}_data'.format(path.lower().split('.')[-1].strip()), 'get_wav_data')()
    with open(path, 'wb') as fout:
        fout.write(data)
    return path


def parse_args():
    parser = argparse.ArgumentParser(description='Record an audio clip.')
    parser.add_argument('-n', '--num', '--num_recordings', type=int, default=0, dest='num_recordings',
                        help='Record N audio clips.')
    parser.add_argument('-r', '--record', '--recordpath', type=str, default='', dest='recordpath',
                        help='Record N audio clips (delimitted by silence).')

    parser.add_argument('-b', '--begin', '--begining', type=int, default=0, dest='begin',
                        help='Sample number to begin clip')
    parser.add_argument('-e', '--end', type=int, default=-1, dest='end',
                        help='Sample number to end clip')
    parser.add_argument('-p', '--play', type=str, default='', dest='playpath',
                        help='Path of audio file to play.')
    args = parser.parse_args()
    return args


def try_tts(audio):
    text = []
    try:
        text.append(stt(audio, api='sphinx'))
    except sr.RequestError:
        try:
            text = text.append(stt(audio, api='google'))
        except Exception:
            print(format_exc())
    return text


def main():
    args = parse_args()
    i, j = 0, 0
    if args.recordpath:
        args.num_recordings = 1
    for i in range(args.num_recordings):
        print("Say something! I'm listening...")
        audio = record_audio()
        base_dir = '.'
        ext = '.wav'
        filepath = args.recordpath or os.path.join(base_dir, 'audio-{}{}'.format(i, ext))
        while os.path.exists(filepath):
            j += 1
            filepath = os.path.join(base_dir, 'audio-{}{}'.format(j + i, ext))
            print("filepath '{}'".format(filepath))
        save_audio(audio, filepath)
        print("Saved audio clip to '{}'".format(filepath))
        print("Playing audio clip ...")
        play_audio(audio)
        print("Done.")

    if args.playpath:
        print("Playing '{}'[{}:{}]".format(args.playpath, args.begin, args.end))
        play_audio(args.playpath)



if __name__ == '__main__':
    main()
