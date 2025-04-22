Project Description:

Create a virtual pet simulator where users can take care of digital pets through a command line interface (CLI). Pets' mood, hunger, and energy levels change over time and are represented by dynamic ASCII graphs (e.g.,(=^‥^=) for happy,   (=；ェ；=)  means sick). Users can feed, play or rest their pets to keep them healthy and save/load progress via JSON files. Optional features include mini-games or random events (e.g., "Found a toy!"). ). Built using core Python libraries such as json and time.

Features:

a. display_pet(status: dict) -> none

Print the pet's current ASCII image and state (e.g., hungry, happy) according to the pet's status dictionary.

B. handle_interaction(action: str, pet: dict) -> dict

Update the pet's status after the user action (for example, feeding reduces hunger) and return the modified state.

c. save_or_load_progress(filename: str, pet: dict = None) -> dict

Save the pet's data to a JSON file or load it, returning the pet's state to continue the game.

I am going to:

1\ add pictures for pets and make them refresh its spot in terminal window as soon as the user chose a certain pet to interact with, once being caught then any actions become available

2\ make the hunder and energy values changing in real time (?)

3\ adjust the setting of the time that energy and hunger changing so then winning the game (all pets happy) is at the same time challenging but doable. 




