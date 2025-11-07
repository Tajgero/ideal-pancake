from os.path import join
from os import walk
from settings import *
import pygame

def import_image(*path, format='png', alpha=True):
    full_path = join(*path) + f".{format}"
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path) 

def import_folder(*path):
    frames = []
    for folder, _, files in walk(join(*path)):
        for file in sorted(files, key=lambda name: int(name.split('.')[0])):
            frames.append(pygame.image.load(join(folder, file)).convert_alpha())
    return frames

def audio_importer(*path):
    audio_dict = dict()
    for folder, _, files in walk(join(*path)):
        for file in files:
            audio_dict[file.split('.')[0]] = pygame.mixer.Sound(join(folder, file))
    return audio_dict
