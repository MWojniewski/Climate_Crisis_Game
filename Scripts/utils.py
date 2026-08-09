import pygame
import os

BASE_PATH_FOR_IMGS = "data/images/"


def load_image(path):
    img = pygame.image.load(BASE_PATH_FOR_IMGS + path).convert()
    img.set_colorkey((255, 0, 255))
    return img


def load_image_alpha(path):
    img = pygame.image.load(BASE_PATH_FOR_IMGS + path).convert_alpha()
    return img


def load_images(path):
    images = []
    for img_name in os.listdir(BASE_PATH_FOR_IMGS + path):
        images.append(load_image(path + "/" + img_name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_duration)
        else:
            self.frame = min(self.frame + 1, len(self.images) * self.img_duration - 1)
            if self.frame >= len(self.images) * self.img_duration - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
