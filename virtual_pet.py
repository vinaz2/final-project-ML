import json
import time
import random
import os
from datetime import datetime

# ASCII art for different pet moods
PET_HAPPY = "(=^‥^=)"
PET_SAD = "(=；ェ；=)"
PET_SLEEPY = "(-_-)zzz"
PET_HUNGRY = "(=｀ェ´=)"
PET_SICK = "(=´；ω；｀=)"

# Movement patterns to make the pet seem like it's moving
MOVEMENT_PATTERNS = [
    "   " + PET_HAPPY,
    "  " + PET_HAPPY,
    " " + PET_HAPPY,
    PET_HAPPY,
    " " + PET_HAPPY,
    "  " + PET_HAPPY,
    "   " + PET_HAPPY
]

# Nice messages to show when all pets are happy
LOVE_WORDS = [
    "Your pets are all so happy! You're an amazing pet owner!",
    "Aww, look at your happy little furry friends. You're doing great!",
    "Your pets' happiness is a testament to your love and care."
]


def show_pet_status(pet_status, movement_index=0):
    """
    Displays the pet's current ASCII art and its status information.

    Args:
        pet_status (dict): A dictionary holding the pet's mood, hunger, and energy.
        movement_index (int): Index for the movement pattern to show different positions.
    """
    mood = pet_status.get("mood", "neutral")
    hunger = pet_status.get("hunger", 50)
    energy = pet_status.get("energy", 50)

    if mood == "happy":
        pet_art = MOVEMENT_PATTERNS[movement_index % len(MOVEMENT_PATTERNS)]
    elif mood == "sad":
        pet_art = PET_SAD
    elif mood == "sleepy":
        pet_art = PET_SLEEPY
    elif hunger > 75:
        pet_art = PET_HUNGRY
    elif mood == "sick":
        pet_art = PET_SICK
    else:
        pet_art = MOVEMENT_PATTERNS[movement_index % len(MOVEMENT_PATTERNS)]

    print(pet_art)
    print(f"Mood: {mood}, Hunger: {hunger}, Energy: {energy}")


def handle_user_action(action, pet):
    """
    Updates the pet's status according to the user's action.

    Args:
        action (str): The action the user takes, like "feed", "play", or "rest".
        pet (dict): The current status of the pet.

    Returns:
        tuple: Updated pet status, change in hunger, change in energy, and movement index change.
    """
    hunger_change = 0
    energy_change = 0
    movement_index_change = 1

    # Check if the pet can't perform the action due to its state
    if pet["mood"] == "sleepy":
        if action in ["feed", "play"]:
            print(f"{pet['name']} is sleepy and can't {action}. Let it rest first.")
            return pet, 0, 0, 0
    if pet["mood"] == "hungry":
        if action in ["play", "rest"]:
            print(f"{pet['name']} is hungry and can't {action}. Feed it first.")
            return pet, 0, 0, 0

    if action == "feed":
        old_hunger = pet["hunger"]
        pet["hunger"] = max(0, pet["hunger"] - 30)
        hunger_change = old_hunger - pet["hunger"]
        pet["mood"] = "happy"
        print(f"You fed your pet! Hunger: {pet['hunger']} (-{hunger_change})")
    elif action == "play":
        old_energy = pet["energy"]
        old_hunger = pet["hunger"]
        pet["energy"] = max(0, pet["energy"] - 20)
        pet["hunger"] = min(100, pet["hunger"] + 10)
        energy_change = old_energy - pet["energy"]
        hunger_change = pet["hunger"] - old_hunger
        pet["mood"] = "happy"
        pet["last_play_time"] = datetime.now().timestamp()
        print(f"You played with your pet! Energy: {pet['energy']} (-{energy_change}), Hunger: {pet['hunger']} (+{hunger_change})")
    elif action == "rest":
        old_energy = pet["energy"]
        old_hunger = pet["hunger"]
        pet["energy"] = min(100, pet["energy"] + 40)
        pet["hunger"] = min(100, pet["hunger"] + 5)
        energy_change = pet["energy"] - old_energy
        hunger_change = pet["hunger"] - old_hunger
        pet["mood"] = "sleepy"
        print(f"Your pet is resting. Energy: {pet['energy']} (+{energy_change}), Hunger: {pet['hunger']} (+{hunger_change})")
    else:
        print("Try to feed, play or rest your pet!")
        movement_index_change = 0

    # Random event: 10% chance of finding a toy
    if random.random() < 0.1:
        print("Your pet found a toy!")
        pet["mood"] = "happy"

    return pet, hunger_change, energy_change, movement_index_change


def save_or_load_pet_data(filename, pet=None):
    """
    Saves or loads the pet's data from a JSON file.

    Args:
        filename (str): The name of the JSON file to save to or load from.
        pet (dict, optional): The pet's data to save. If None, it will load data.

    Returns:
        dict: The loaded pet data or an empty dictionary if loading fails.
    """
    if pet:
        try:
            with open(filename, "w") as file:
                json.dump(pet, file)
            print(f"Game saved to {filename}")
            return pet
        except Exception as error:
            print(f"Error saving game: {error}")
            return pet
    else:
        try:
            with open(filename, "r") as file:
                loaded_pet = json.load(file)
                if "last_play_time" in loaded_pet:
                    loaded_pet["last_play_time"] = float(loaded_pet["last_play_time"])
                if "creation_time" in loaded_pet:
                    loaded_pet["creation_time"] = float(loaded_pet["creation_time"])
            print(f"Game loaded from {filename}")
            return loaded_pet
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
            return {}
        except Exception as error:
            print(f"Error loading game: {error}")
            return {}


def update_pet_conditions(pet):
    """
    Updates the pet's energy, hunger, and mood based on the time passed.

    Args:
        pet (dict): The current status of the pet.

    Returns:
        dict: The updated pet status.
    """
    current_time = datetime.now().timestamp()
    creation_time = pet.get("creation_time", current_time)
    last_play_time = pet.get("last_play_time", current_time)


    # Hunger increases over time
    pet["hunger"] = min(100, pet["hunger"] + 5)

    # Determine the pet's mood
    if pet["hunger"] >= 90 and pet["energy"] <= 10:
        pet["mood"] = "sick"
    elif pet["hunger"] >= 90:
        pet["mood"] = "hungry"
    elif pet["energy"] <= 10:
        pet["mood"] = "sleepy"
        print(f"{pet['name']} is sleepy!")
    else:
        # Check if the pet is sad due to lack of play
        if current_time - last_play_time > 600:
            pet["mood"] = "sad"

    return pet


def check_all_pets_status(pets_folder, badges):
    """
    Checks the status of all saved pets and gives feedback to the user.

    Args:
        pets_folder (str): The folder where pet data is stored.
        badges (int): The current number of badges the user has.

    Returns:
        int: The updated number of badges.
    """
    all_pets_happy = True
    for filename in os.listdir(pets_folder):
        if filename.endswith(".json"):
            pet = save_or_load_pet_data(os.path.join(pets_folder, filename))
            pet = update_pet_conditions(pet)
            save_or_load_pet_data(os.path.join(pets_folder, filename), pet)
            if pet["mood"] in ["sad", "hungry", "sleepy", "sick"]:
                all_pets_happy = False
                print(f"{pet['name']} is {pet['mood']}!")
    if all_pets_happy:
        badges += 1
        print(random.choice(LOVE_WORDS))
        print(f"You earned a badge! Total badges: {badges}")
    return badges


def manage_pets():
    """
    The main function to manage multiple pets. It allows users to create, interact, and view pet statuses.
    """
    pets_folder = "pets"
    if not os.path.exists(pets_folder):
        os.makedirs(pets_folder)

    badges = 0
    while True:
        badges = check_all_pets_status(pets_folder, badges)
        print("\n1. Create a new pet")
        print("2. Interact with a pet")
        print("3. View all pets' status")
        print("4. Show badges")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            pet_name = input("Enter a name for your new pet: ")
            pet_filename = os.path.join(pets_folder, f"{pet_name}.json")
            new_pet = {
                "name": pet_name,
                "mood": "happy",
                "hunger": 50,
                "energy": 50,
                "last_play_time": datetime.now().timestamp(),
                "creation_time": datetime.now().timestamp()
            }
            save_or_load_pet_data(pet_filename, new_pet)
            print(f"New pet {pet_name} created!")
        elif choice == "2":
            pet_name = input("Enter the name of the pet you want to interact with: ")
            pet_filename = os.path.join(pets_folder, f"{pet_name}.json")
            pet = save_or_load_pet_data(pet_filename)
            if pet:
                movement_index = 0
                last_update_time = datetime.now().timestamp()
                while True:
                    current_time = datetime.now().timestamp()
                    elapsed_time = current_time - last_update_time

                    # Update energy and hunger in real - time
                    energy_decrease = int(elapsed_time // 5)
                    pet["energy"] = max(0, pet["energy"] - energy_decrease)
                    pet["hunger"] = min(100, pet["hunger"] + int(elapsed_time * 0.5))
                    pet = update_pet_conditions(pet)
                    last_update_time = current_time

                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Interacting with {pet_name}")
                    show_pet_status(pet, movement_index)
                    action = input("What do you want to do? (feed, play, rest, save, back): ").lower()
                    if action == "back":
                        save_or_load_pet_data(pet_filename, pet)
                        break
                    elif action == "save":
                        save_or_load_pet_data(pet_filename, pet)
                    else:
                        pet, _, _, movement_index_change = handle_user_action(action, pet)
                        movement_index += movement_index_change
                        save_or_load_pet_data(pet_filename, pet)
                        # Reset the last update time after an action to avoid double - counting energy decrease
                        last_update_time = datetime.now().timestamp()
                    time.sleep(1)
            else:
                print(f"Pet {pet_name} not found.")
        elif choice == "3":
            for filename in os.listdir(pets_folder):
                if filename.endswith(".json"):
                    pet = save_or_load_pet_data(os.path.join(pets_folder, filename))
                    print(f"Pet: {pet['name']}")
                    show_pet_status(pet)
        elif choice == "4":
            print(f"Total badges: {badges}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    manage_pets()

