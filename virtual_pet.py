import json
import time
import random

# Pet ASCII art (can be expanded)
PET_HAPPY = "(=^‥^=)"
PET_SAD = "(=；ェ；=)"
PET_SLEEPY = "(-_-)zzz"
PET_HUNGRY = "(=｀ェ´=)"
PET_SICK = "(=´；ω；｀=)"

def display_pet(status: dict) -> None:
    """
    Prints the pet's current ASCII image and state.

    Args:
        status (dict): A dictionary containing the pet's status (e.g., mood, hunger).
    """

    mood = status.get("mood", "neutral")
    hunger = status.get("hunger", 50)
    energy = status.get("energy", 50)

    if mood == "happy":
        pet_art = PET_HAPPY
    elif mood == "sad":
        pet_art = PET_SAD
    elif mood == "sleepy":
        pet_art = PET_SLEEPY
    elif hunger > 75:
        pet_art = PET_HUNGRY
    elif mood == "sick":
        pet_art = PET_SICK
    else:
        pet_art = PET_HAPPY  # default state of the pet

    print(pet_art)
    print(f"Mood: {mood}, Hunger: {hunger}, Energy: {energy}")


def handle_interaction(action: str, pet: dict) -> dict:
    """
    Updates the pet's status based on the user's action.

    Args:
        action (str): The action performed by the user (e.g., "feed", "play", "rest").
        pet (dict): The current pet's status.

    Returns:
        dict: The updated pet status.
    """

    if action == "feed":
        pet["hunger"] = max(0, pet["hunger"] - 30)  # Reduce hunger
        pet["mood"] = "happy"  # Feeding makes pet happy
        print("You fed your pet!")
    elif action == "play":
        pet["energy"] = max(0, pet["energy"] - 20)  # Reduce energy
        pet["hunger"] = min(100, pet["hunger"] + 10)  # Playing increases hunger
        pet["mood"] = "happy"
        print("You played with your pet!")
    elif action == "rest":
        pet["energy"] = min(100, pet["energy"] + 40)  # Increase energy
        pet["hunger"] = min(100, pet["hunger"] + 5)  # Resting increases hunger slightly
        pet["mood"] = "sleepy"
        print("Your pet is resting.")
    else:
        print("Try to feed, play or rest your pet!")

    # Add random events or status changes here (optional)
    if random.random() < 0.1:  # 10% chance of a random event
        print("Your pet found a toy!")
        pet["mood"] = "happy"

    # Update pet's status over time (hunger increases, energy decreases)
    pet["hunger"] = min(100, pet["hunger"] + 5)
    pet["energy"] = max(0, pet["energy"] - 2)

    # Check if pet is sick
    if pet["hunger"] >= 90 and pet["energy"] <= 10:
        pet["mood"] = "sick"
    elif pet["hunger"] >= 90:
        pet["mood"] = "hungry"
    elif pet["energy"] <= 10:
        pet["mood"] = "sleepy"
    else:
        pet["mood"] = "happy"

    return pet



def save_or_load_progress(filename: str, pet: dict = None) -> dict:
    """
    Saves or loads the pet's data from a JSON file.

    Args:
        filename (str): The name of the JSON file.
        pet (dict, optional): The pet's data to save.  If None, load data. Defaults to None.

    Returns:
        dict: The loaded pet data, or an empty dictionary if loading fails.
    """

    if pet:  # Save
        try:
            with open(filename, "w") as f:
                json.dump(pet, f)
            print(f"Game saved to {filename}")
            return pet
        except Exception as e:
            print(f"Error saving game: {e}")
            return pet #Return the original pet even if save fails.
    else:  # Load
        try:
            with open(filename, "r") as f:
                loaded_pet = json.load(f)
            print(f"Game loaded from {filename}")
            return loaded_pet
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
            return {}  # Return an empty dictionary for a new game
        except Exception as e:
            print(f"Error loading game: {e}")
            return {} #Return empty dict if load fails.


def main():
    """
    Main game loop.
    """
    filename = "pet_data.json"
    pet = save_or_load_progress(filename)

    if not pet:
        # Initialize a new pet if no saved data is found
        pet = {"mood": "happy", "hunger": 50, "energy": 50}

    while True:
        display_pet(pet)
        action = input("What do you want to do? (feed, play, rest, save, exit): ").lower()

        if action == "exit":
            print("Goodbye!")
            break
        elif action == "save":
            save_or_load_progress(filename, pet)
        else:
            pet = handle_interaction(action, pet)
            display_pet(pet)  # Display after handle_interaction

        time.sleep(2)  # Wait for 2 seconds




if __name__ == "__main__":
    main()
