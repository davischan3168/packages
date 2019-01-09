#!/usr/bin/env python3
# -*-coding:utf-8-*-
from pydub import AudioSegment
import pygame
pygame.mixer.init()

"""sample

sound = AudioSegment.from_mp3("/path/to/file.mp3")
# len() and slicing are in milliseconds
halfway_point = len(sound) / 2
second_half = sound[halfway_point:]
# Concatenation is just adding
second_half_3_times = second_half + second_half + second_half
# writing mp3 files is a one liner
second_half_3_times.export("/path/to/new/file.mp3", format="mp3")
"""

pygame.mixer.music.load('baobao/newsong/asasa.m4a')
pygame.mixer.music.play()

pygame.mixer.music.load('经典咏流传-第1期_明日歌-(Live)_王俊凯.m4a')
pygame.mixer.music.play()

