# Utility functions for graphics

import os
import pygame
from typing import Tuple, Optional, Dict, List

def load_image(file_path: str) -> pygame.Surface:
    """
    Load an image from the given file path with error handling.
    Args:
        file_path: Path to the image file
    Returns:
        pygame.Surface: Loaded and converted image
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
            
        image = pygame.image.load(file_path).convert_alpha()
        return image
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image {file_path}: {e}")
        raise SystemExit(e)

def scale_image(image: pygame.Surface, size: Tuple[int, int]) -> pygame.Surface:
    """
    Scale an image to the specified size using smooth scaling.
    """
    try:
        return pygame.transform.smoothscale(image, size)
    except pygame.error as e:
        print(f"Error scaling image: {e}")
        return image

def create_transparent_surface(size: Tuple[int, int], 
                             color: Tuple[int, int, int, int]) -> pygame.Surface:
    """
    Create a transparent surface with the specified color and alpha.
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface

def load_piece_images(directory: str, square_size: int) -> Dict[str, pygame.Surface]:
    """
    Load all chess piece images from a directory and scale them.
    """
    images = {}
    pieces = ["king", "queen", "bishop", "knight", "rook", "pawn"]
    colors = ["white", "black"]
    
    try:
        for color in colors:
            for piece in pieces:
                file_path = os.path.join(directory, f"{color}_{piece}.png")
                if os.path.exists(file_path):
                    image = load_image(file_path)
                    images[f"{color}_{piece}"] = scale_image(
                        image, (square_size, square_size)
                    )
                else:
                    print(f"Warning: Missing piece image: {file_path}")
    except Exception as e:
        print(f"Error loading piece images: {e}")
        raise
        
    return images

class InfoPanel:
    """
    Creates and manages the information panel shown next to the chess board.
    """
    def __init__(self, screen: pygame.Surface, position: Tuple[int, int], 
                size: Tuple[int, int], square_size: int):
        """
        Initialize the info panel.
        
        Args:
            screen: Pygame screen to draw on
            position: (x, y) position of top-left corner
            size: (width, height) size of the panel
            square_size: Size of chess squares for scaling
        """
        self.screen = screen
        self.position = position
        self.size = size
        self.square_size = square_size
        
        # Colors
        self.bg_color = (50, 50, 50)
        self.text_color = (240, 240, 240)
        self.highlight_color = (70, 130, 180)
        
        # Fonts
        self.title_font = pygame.font.SysFont(None, 32)
        self.normal_font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 18)
        
        # Load piece type icons
        self.icons = self._load_icons()
        
    def _load_icons(self) -> Dict[str, pygame.Surface]:
        """Load icons for different piece types."""
        icons = {}
        
        # Icon size - 1/3 of a square
        icon_size = self.square_size // 3
        
        # Default path for icons
        icons_path = os.path.join(os.path.dirname(__file__), "../assets/icons")
        
        # Create directory if it doesn't exist
        if not os.path.exists(icons_path):
            os.makedirs(icons_path)
            
        # Try to load piece icons
        for piece_type in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
            icon_path = os.path.join(icons_path, f"{piece_type}_icon.png")
            
            try:
                icon = pygame.image.load(icon_path)
                icons[piece_type] = pygame.transform.scale(icon, (icon_size, icon_size))
            except:
                # Create default icon
                icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                
                if piece_type == "pawn":
                    pygame.draw.circle(icon, (200, 200, 200), (icon_size//2, icon_size//2), icon_size//2.5)
                elif piece_type == "knight":
                    points = [(icon_size//4, icon_size//4), (icon_size*3//4, icon_size//4), 
                              (icon_size*3//4, icon_size*3//4), (icon_size//4, icon_size*3//4)]
                    pygame.draw.polygon(icon, (200, 200, 200), points)
                elif piece_type == "bishop":
                    pygame.draw.polygon(icon, (200, 200, 200), 
                                       [(icon_size//2, icon_size//4), 
                                        (icon_size*3//4, icon_size*3//4),
                                        (icon_size//4, icon_size*3//4)])
                elif piece_type == "rook":
                    pygame.draw.rect(icon, (200, 200, 200), 
                                    (icon_size//4, icon_size//4, 
                                     icon_size//2, icon_size//2))
                elif piece_type == "queen":
                    pygame.draw.circle(icon, (200, 200, 200), 
                                      (icon_size//2, icon_size//2), 
                                      icon_size//3)
                    points = [(icon_size//2, icon_size//6), 
                              (icon_size*2//3, icon_size//3),
                              (icon_size*5//6, icon_size//2),
                              (icon_size*2//3, icon_size*2//3),
                              (icon_size//2, icon_size*5//6),
                              (icon_size//3, icon_size*2//3),
                              (icon_size//6, icon_size//2),
                              (icon_size//3, icon_size//3)]
                    pygame.draw.polygon(icon, (150, 150, 150), points)
                elif piece_type == "king":
                    pygame.draw.circle(icon, (200, 200, 200), 
                                      (icon_size//2, icon_size//2), 
                                      icon_size//3)
                    # Draw a cross
                    pygame.draw.rect(icon, (150, 150, 150), 
                                    (icon_size*2//5, icon_size//4, 
                                     icon_size//5, icon_size//2))
                    pygame.draw.rect(icon, (150, 150, 150), 
                                    (icon_size//4, icon_size*2//5, 
                                     icon_size//2, icon_size//5))
                
                icons[piece_type] = icon
                
        return icons
        
    def draw(self, game_state: str, current_turn: str, 
            selected_piece: Optional[Tuple[Tuple[int, int], Tuple[str, str]]] = None,
            captured_pieces: Optional[Dict[str, List[str]]] = None,
            last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None):
        """Draw the info panel with current game information."""
        # Draw panel background
        panel_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        pygame.draw.rect(self.screen, self.bg_color, panel_rect)
        pygame.draw.rect(self.screen, self.text_color, panel_rect, 2)
        
        # Draw title
        title = self.title_font.render("Chess Game", True, self.text_color)
        self.screen.blit(title, (self.position[0] + 10, self.position[1] + 10))
        
        # Draw current game state
        state_text = f"Game State: {game_state.capitalize()}"
        state = self.normal_font.render(state_text, True, self.text_color)
        self.screen.blit(state, (self.position[0] + 10, self.position[1] + 50))
        
        # Draw current turn
        turn_color = (255, 255, 255) if current_turn == "white" else (50, 50, 50)
        turn_bg = (0, 0, 0) if current_turn == "white" else (200, 200, 200)
        turn_rect = pygame.Rect(self.position[0] + 10, self.position[1] + 80, 20, 20)
        pygame.draw.rect(self.screen, turn_bg, turn_rect)
        pygame.draw.rect(self.screen, self.text_color, turn_rect, 1)
        
        turn_text = f"{current_turn.capitalize()}'s turn"
        turn = self.normal_font.render(turn_text, True, self.text_color)
        self.screen.blit(turn, (self.position[0] + 40, self.position[1] + 80))
        
        # Draw selected piece info if available
        if selected_piece:
            pos, piece = selected_piece
            
            # Section header
            selected_header = self.normal_font.render("Selected Piece:", True, self.text_color)
            self.screen.blit(selected_header, (self.position[0] + 10, self.position[1] + 120))
            
            # Draw piece info
            color, piece_type = piece
            piece_color = (255, 255, 255) if color == "white" else (50, 50, 50)
            piece_bg = (0, 0, 0) if color == "white" else (200, 200, 200)
            
            # Draw piece color indicator
            color_rect = pygame.Rect(self.position[0] + 20, self.position[1] + 150, 15, 15)
            pygame.draw.rect(self.screen, piece_bg, color_rect)
            pygame.draw.rect(self.screen, self.text_color, color_rect, 1)
            
            # Draw piece type icon if available
            if piece_type in self.icons:
                icon_pos = (self.position[0] + 45, self.position[1] + 147)
                self.screen.blit(self.icons[piece_type], icon_pos)
            
            # Draw piece name and position
            piece_name = f"{color.capitalize()} {piece_type.capitalize()}"
            piece_pos_text = f"Position: {chr(97 + pos[0])}{8 - pos[1]}"
            
            name_text = self.normal_font.render(piece_name, True, self.text_color)
            pos_text = self.small_font.render(piece_pos_text, True, self.text_color)
            
            self.screen.blit(name_text, (self.position[0] + 80, self.position[1] + 150))
            self.screen.blit(pos_text, (self.position[0] + 20, self.position[1] + 175))
        
        # Draw captured pieces if available
        if captured_pieces:
            # Section header
            captured_header = self.normal_font.render("Captured Pieces:", True, self.text_color)
            self.screen.blit(captured_header, (self.position[0] + 10, self.position[1] + 210))
            
            # Draw white's captures
            white_y = self.position[1] + 240
            if "black" in captured_pieces and captured_pieces["black"]:
                white_text = self.small_font.render("White captured:", True, self.text_color)
                self.screen.blit(white_text, (self.position[0] + 20, white_y))
                
                # Draw icons for each captured piece
                for i, piece_type in enumerate(captured_pieces["black"]):
                    if piece_type in self.icons:
                        x_pos = self.position[0] + 20 + (i % 4) * (self.square_size // 3 + 5)
                        y_pos = white_y + 25 + (i // 4) * (self.square_size // 3 + 5)
                        self.screen.blit(self.icons[piece_type], (x_pos, y_pos))
            
            # Draw black's captures
            black_y = white_y + 70
            if "white" in captured_pieces and captured_pieces["white"]:
                black_text = self.small_font.render("Black captured:", True, self.text_color)
                self.screen.blit(black_text, (self.position[0] + 20, black_y))
                
                # Draw icons for each captured piece
                for i, piece_type in enumerate(captured_pieces["white"]):
                    if piece_type in self.icons:
                        x_pos = self.position[0] + 20 + (i % 4) * (self.square_size // 3 + 5)
                        y_pos = black_y + 25 + (i // 4) * (self.square_size // 3 + 5)
                        self.screen.blit(self.icons[piece_type], (x_pos, y_pos))
        
        # Draw last move if available
        if last_move:
            start, end = last_move
            last_move_text = f"Last move: {chr(97 + start[0])}{8 - start[1]} → {chr(97 + end[0])}{8 - end[1]}"
            move_text = self.small_font.render(last_move_text, True, self.text_color)
            self.screen.blit(move_text, (self.position[0] + 10, self.position[1] + self.size[1] - 40))

def draw_coordinates(screen: pygame.Surface, square_size: int, 
                    font: Optional[pygame.font.Font] = None):
    """
    Draw chess coordinate labels (a-h, 1-8) around the board.
    
    Args:
        screen: Pygame screen to draw on
        square_size: Size of each chess square
        font: Font to use (creates default if None)
    """
    if font is None:
        font = pygame.font.SysFont(None, 20)
    
    text_color = (50, 50, 50)
    
    # Draw file labels (a-h)
    for i in range(8):
        label = font.render(chr(97 + i), True, text_color)
        x = i * square_size + square_size//2 - label.get_width()//2
        y = 8 * square_size + 5
        screen.blit(label, (x, y))
    
    # Draw rank labels (1-8)
    for i in range(8):
        label = font.render(str(8 - i), True, text_color)
        x = -5 - label.get_width()
        y = i * square_size + square_size//2 - label.get_height()//2
        screen.blit(label, (x, y))

def draw_promotion_dialog(screen: pygame.Surface, square_size: int, 
                         pos: Tuple[int, int], color: str, 
                         piece_images: Dict[str, pygame.Surface]) -> List[pygame.Rect]:
    """
    Draw a dialog for pawn promotion selection.
    
    Args:
        screen: Pygame screen to draw on
        square_size: Size of chess squares
        pos: (x, y) board position where promotion is happening
        color: Color of the pawn being promoted ("white" or "black")
        piece_images: Dictionary of piece images
        
    Returns:
        List[pygame.Rect]: List of clickable areas for each promotion option
    """
    # Create background
    dialog_width = square_size * 4
    dialog_height = square_size * 1.5
    
    x = pos[0] * square_size + square_size//2 - dialog_width//2
    y = pos[1] * square_size + square_size//2 - dialog_height//2
    
    # Ensure dialog stays on screen
    x = max(10, min(x, screen.get_width() - dialog_width - 10))
    y = max(10, min(y, screen.get_height() - dialog_height - 10))
    
    # Draw dialog background
    dialog_rect = pygame.Rect(x, y, dialog_width, dialog_height)
    pygame.draw.rect(screen, (240, 240, 240), dialog_rect)
    pygame.draw.rect(screen, (0, 0, 0), dialog_rect, 2)
    
    # Draw title
    font = pygame.font.SysFont(None, 24)
    title = font.render("Promote to:", True, (0, 0, 0))
    screen.blit(title, (x + 10, y + 10))
    
    # Draw piece options
    piece_types = ["queen", "rook", "bishop", "knight"]
    option_rects = []
    
    for i, piece_type in enumerate(piece_types):
        piece_key = f"{color}_{piece_type}"
        
        if piece_key in piece_images:
            # Calculate position
            piece_x = x + 20 + i * (square_size + 5)
            piece_y = y + 40
            
            # Draw piece image
            piece_rect = pygame.Rect(piece_x, piece_y, square_size, square_size)
            
            # Draw selection box
            pygame.draw.rect(screen, (200, 200, 200), piece_rect)
            pygame.draw.rect(screen, (0, 0, 0), piece_rect, 1)
            
            # Draw piece image
            screen.blit(piece_images[piece_key], piece_rect)
            
            # Add to clickable areas
            option_rects.append((piece_rect, piece_type))
    
    return option_rects
