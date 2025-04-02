import pygame
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

images = {}
pieces = ["BlackBishop", "BlackKing", "BlackKnight", "BlackPawn", "BlackQueen", "BlackRook",
          "WhiteBishop", "WhiteKing", "WhiteKnight", "WhitePawn", "WhiteQueen", "WhiteRook"]

for piece in pieces:
    key = piece.lower()  # Convert to lowercase for consistency
    images[key] = pygame.image.load(f"assets/pieces/{piece}.png")

print(images.keys())

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()