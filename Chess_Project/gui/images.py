import pygame
import os
import json

def load_piece_images(square_size):
    """
    Load chess piece images.
    """
    images = {}
    base_path = os.path.join(os.path.dirname(__file__), "../assets/pieces")
    for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
        for color in ["white", "black"]:
            key = f"{color}_{piece}"
            path = os.path.join(base_path, f"{key}.png")
            try:
                image = pygame.transform.scale(pygame.image.load(path), 
                                               (square_size, square_size))
                images[key] = image
            except FileNotFoundError:
                print(f"Error: Missing file {path}")
    return images

def save_game_state(game_state, filename="saved_game.json"):
    """
    Save the current game state to a file.
    
    Args:
        game_state: Game state to save
        filename: Filename to save to (default: saved_game.json)
    
    Returns:
        bool: Whether the save was successful
    """
    save_path = os.path.join(os.path.dirname(__file__), "../saved_games")
    
    # Ensure directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    full_path = os.path.join(save_path, filename)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, ensure_ascii=False, indent=4)
        print(f"Game saved successfully at: {full_path}")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game_state(filename="saved_game.json"):
    """
    Load a saved game state from a file.
    
    Args:
        filename: Filename to load from (default: saved_game.json)
    
    Returns:
        dict: Loaded game state, or None if loading failed
    """
    load_path = os.path.join(os.path.dirname(__file__), "../saved_games", filename)
    
    try:
        with open(load_path, 'r', encoding='utf-8') as f:
            game_state = json.load(f)
        print(f"Game loaded successfully from: {load_path}")
        return game_state
    except FileNotFoundError:
        print(f"Save file not found: {load_path}")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None