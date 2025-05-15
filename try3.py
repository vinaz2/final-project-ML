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

# -----------------------------
# Configurations
# -----------------------------
MODEL_PATH = 'model-resnet50-final2.h5'
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# -----------------------------
# Load model
# -----------------------------
def load_trained_model():
    return load_model(MODEL_PATH)

def classify_pet(model, img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    prediction = model.predict(img_array)
    class_idx = np.argmax(prediction)
    return class_idx

# -----------------------------
# Image loading and scaling
# -----------------------------
def load_background_image(img_path):
    img = Image.open(img_path)
    img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)

# -----------------------------
# Main Game Function
# -----------------------------
def run_game(img_path, pet_type):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Your Virtual Pet")

    font = pygame.font.SysFont(None, 32)
    large_font = pygame.font.SysFont(None, 40)
    background = load_background_image(img_path)

    actions_cat = ["Collect Cat Fur", "Clean Litter", "Feed Treats"]
    actions_dog = ["Feed Bone", "Walk Dog", "Hug Dog"]
    actions = actions_cat if pet_type == "cat" else actions_dog

    button_rects = []
    for i, action in enumerate(actions):
        rect = pygame.Rect(100 + i * 220, 500, 200, 50)
        button_rects.append((rect, action))

    message = "I am lonely, I need you."
    action_taken = False

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Render message
        color = (255, 255, 255)
        text_surface = large_font.render(message, True, color)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 30))

        # Draw buttons
        for rect, label in button_rects:
            pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(-4, -4), border_radius=10)
            label_surface = font.render(label, True, (0, 0, 0))
            screen.blit(label_surface, (rect.x + 20, rect.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, label in button_rects:
                    if rect.collidepoint(event.pos):
                        message = "I love you. I will always be by your side, my human."
                        action_taken = True

    pygame.quit()

# -----------------------------
# File dialog to choose image
# -----------------------------
def choose_image_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Choose an image of a cat or dog",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return file_path

# -----------------------------
# Main logic
# -----------------------------
def main():
    model = load_trained_model()
    img_path = choose_image_file()
    if not img_path or not os.path.exists(img_path):
        print("❌ No image selected or file does not exist.")
        return

    pet_class = classify_pet(model, img_path)
    pet_type = "cat" if pet_class == 0 else "dog"

    run_game(img_path, pet_type)

if __name__ == "__main__":
    main()
