import pytest
import virtual_pet  # Import your virtual_pet.py file
import os
import json

def test_display_pet_happy(capsys):
    """Tests that display_pet prints something when the pet is happy."""
    status = {"mood": "happy", "hunger": 20, "energy": 80}
    virtual_pet.display_pet(status)
    captured = capsys.readouterr()
    assert virtual_pet.PET_HAPPY in captured.out  # Check if happy art is printed
    assert "Mood: happy" in captured.out
    assert "Hunger: 20" in captured.out
    assert "Energy: 80" in captured.out


def test_handle_interaction_feed():
    """Tests the 'feed' action."""
    pet = {"mood": "sad", "hunger": 60, "energy": 40}
    updated_pet = virtual_pet.handle_interaction("feed", pet)
    assert updated_pet["hunger"] == 30  # Hunger should decrease
    assert updated_pet["mood"] == "happy"  # Mood should change to happy


def test_handle_interaction_play():
    """Tests the 'play' action."""
    pet = {"mood": "neutral", "hunger": 30, "energy": 70}
    updated_pet = virtual_pet.handle_interaction("play", pet)
    assert updated_pet["energy"] == 50  # Energy should decrease
    assert updated_pet["hunger"] == 40  # Hunger should increase
    assert updated_pet["mood"] == "happy"


def test_handle_interaction_rest():
    """Tests the 'rest' action."""
    pet = {"mood": "neutral", "hunger": 30, "energy": 70}
    updated_pet = virtual_pet.handle_interaction("rest", pet)
    assert updated_pet["energy"] == 100  # Energy should increase
    assert updated_pet["hunger"] == 35  # Hunger should increase
    assert updated_pet["mood"] == "sleepy"


def test_save_or_load_progress_save_and_load(tmpdir):
    """Tests saving and loading pet data."""
    filename = str(tmpdir.join("test_pet.json"))  # Create a temporary file
    pet_data = {"mood": "happy", "hunger": 25, "energy": 75}

    # Save the data
    virtual_pet.save_or_load_progress(filename, pet_data)

    # Load the data
    loaded_pet_data = virtual_pet.save_or_load_progress(filename)

    assert loaded_pet_data == pet_data  # Check if the loaded data matches the original

def test_save_or_load_progress_load_no_file(capsys):
    """Tests loading when no file exists."""
    filename = "nonexistent_file.json"
    loaded_pet = virtual_pet.save_or_load_progress(filename)
    captured = capsys.readouterr()
    assert "No saved game found" in captured.out
    assert loaded_pet == {}  # Should return an empty dictionary

def test_save_or_load_progress_save_error(tmpdir, monkeypatch, capsys):
    """Tests the save function when an error occurs."""
    filename = str(tmpdir.join("test_pet.json"))
    pet_data = {"mood": "happy", "hunger": 25, "energy": 75}

    # Mock the open function to raise an exception
    def mock_open(*args, **kwargs):
        raise Exception("Mocked save error")

    monkeypatch.setattr("builtins.open", mock_open)

    # Call the save function
    result = virtual_pet.save_or_load_progress(filename, pet_data)
    captured = capsys.readouterr()

    # Assert that the error message is printed
    assert "Error saving game" in captured.out
    assert result == pet_data #Assert that the original pet is returned.

def test_save_or_load_progress_load_error(tmpdir, monkeypatch, capsys):
    """Tests the load function when an error occurs."""
    filename = str(tmpdir.join("test_pet.json"))

    # Mock the open function to raise an exception
    def mock_open(*args, **kwargs):
        raise Exception("Mocked load error")

    monkeypatch.setattr("builtins.open", mock_open)

    # Call the load function
    result = virtual_pet.save_or_load_progress(filename)
    captured = capsys.readouterr()

    # Assert that the error message is printed
    assert "Error loading game" in captured.out
    assert result == {}  # Should return an empty dictionary
