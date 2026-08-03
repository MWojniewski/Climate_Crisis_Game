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
