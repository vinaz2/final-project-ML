# TODO: check whether it run as-is
# This is the main Python file that combines image classification and a simple game.

import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import math
import time
import random

MODEL_PATH = 'model-resnet50-final3.h5'

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Sound files for each pet types
# When the game starts for each pet type
SOUND_STARTS = {
    "cat": "cat_start.wav",
    "dog": "dog_start.wav",
    "snake": "snake_start.wav"
}

# When an action is taken
SOUND_ACTIONS = {
    "cat": "cat_action.wav",
    "dog": "dog_action.wav",
    "snake": "snake_action.wav"
}


# to load the pre-trained model
def load_trained_model():
    try:
        print("Loading the pre-trained model...")
        return load_model(MODEL_PATH)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None


# Classify the pet in the given image
def classify_pet(model, img_path):
    if model is None:
        print("Model is not loaded properly. Cannot classify the image.")
        return None
    try:
        print(f"Loading and preprocessing the image: {img_path}")
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        print("Making a prediction on the class of image...")
        prediction = model.predict(img_array)
        class_idx = np.argmax(prediction)
        return class_idx
    except Exception as e:
        print(f"Error classifying the image: {e}")
        return None


# set the background image for the pygame
def load_background_image(img_path):
    img = Image.open(img_path)
    img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    

# Main function
def run_game(img_path, pet_type):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Your Virtual Pet")
    normal_font = pygame.font.SysFont(None, 32)
    large_font = pygame.font.SysFont(None, 40)
    background = load_background_image(img_path)

    start_sound = None
    action_sound = None
    if pet_type in SOUND_STARTS and os.path.exists(SOUND_STARTS[pet_type]):
        start_sound = pygame.mixer.Sound(SOUND_STARTS[pet_type])
    if pet_type in SOUND_ACTIONS and os.path.exists(SOUND_ACTIONS[pet_type]):
        action_sound = pygame.mixer.Sound(SOUND_ACTIONS[pet_type])

    # Play the start sound wav.
    if start_sound:
        start_sound.play()

    # actions available for each pet type
    cat_actions = ["Collect Cat Fur", "Clean Litter", "Feed Treats"]
    dog_actions = ["Feed Bone", "Walk Dog", "Hug Dog"]
    snake_actions = ["Feed Rats", "Clean Ecdysis", "Curl Up Gently"]

    available_actions = []
    if pet_type == "cat":
        available_actions = cat_actions
    elif pet_type == "dog":
        available_actions = dog_actions
    elif pet_type == "snake":
        available_actions = snake_actions
    else:
        print(f"Unknown pet type: {pet_type}. Please select a cat/dog/snake image")


    # action buttons
    total_button_width = len(available_actions) * 200
    total_padding_width = WINDOW_WIDTH - total_button_width
    padding = total_padding_width // (len(available_actions) + 1)

    action_buttons = []
    for index, action in enumerate(available_actions):
        x = padding + index * (200 + padding)
        button_rect = pygame.Rect(x, 500, 200, 50)
        action_buttons.append((button_rect, action))

    # the starting interface of pygame (fade-in effect)
    display_message = "I am lonely, I need you."
    action_performed = False

    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade_surface.fill((0, 0, 0))
    alpha_value = 255


    # Main game loop
    game_running = True
    animation_start_time = time.time()

    while game_running:
        screen.blit(background, (0, 0))

        if alpha_value > 0:
            fade_surface.set_alpha(alpha_value)
            screen.blit(fade_surface, (0, 0))
            alpha_value -= 5

        # the bounce effect of the message
        elapsed_time = time.time() - animation_start_time
        bounce_offset = 10 * math.sin(elapsed_time * 3)

        text_color = (255, 255, 255)
        text_surface = large_font.render(display_message, True, text_color)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 30 + bounce_offset))
        screen.blit(text_surface, text_rect)

        # Got the current mouse position
        mouse_position = pygame.mouse.get_pos()

        # changing colors of buttons when hoovering
        for rect, label in action_buttons:
            if rect.collidepoint(mouse_position):
                pygame.draw.rect(screen, (100, 100, 255), rect, border_radius=10)
                pygame.draw.rect(screen, (180, 180, 255), rect.inflate(-4, -4), border_radius=10)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), rect.inflate(-4, -4), border_radius=10)

            label_surface = normal_font.render(label, True, (0, 0, 0))
            screen.blit(label_surface, (rect.x + 20, rect.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, label in action_buttons:
                    if rect.collidepoint(event.pos):
                        display_message = "I love you. I will always be by your side, my human."
                        action_performed = True
                        if action_sound:
                            action_sound.play()

    pygame.quit()


# Function to let the user select an image
def choose_image_file():
    root = tk.Tk()
    root.withdraw()
    print("Opening the finder dialog to choose an image...")
    file_path = filedialog.askopenfilename(
        title="Choose an image of a cat, dog, or snake",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return file_path


def main():
    model = load_trained_model()

    if model is None:
        return
    image_path = choose_image_file()
    if not image_path or not os.path.exists(image_path):
        print("No image selected or the selected image does not exist.")
        return
    pet_class_index = classify_pet(model, image_path)
    if pet_class_index is None:
        return

    pet_type_mapping = {0: "cat", 1: "dog", 2: "snake"}
    pet_type = pet_type_mapping.get(pet_class_index, "unknown")
    print(f"The image is classified as {pet_type}.")
    run_game(image_path, pet_type)


if __name__ == "__main__":
    main()