import pygame

def animate_move(screen, start_pos, end_pos, piece_image, board, images, board_view):
    """Animate a move from start_pos to end_pos."""
    start_x = start_pos[0] * 100
    start_y = start_pos[1] * 100
    end_x = end_pos[0] * 100
    end_y = end_pos[1] * 100

    dx = end_x - start_x
    dy = end_y - start_y
    frames = 30  # Number of frames for the animation
    x, y = start_x, start_y

    for i in range(frames):
        x += dx / frames
        y += dy / frames
        
        # Redraw the board (without the moving piece)
        board_view.render(board, images)  # Use the passed board_view instance
        screen.blit(piece_image, (x, y))  # Draw the piece at the animated position
        pygame.display.flip()
        pygame.time.delay(10)  # Add a small delay for smoother animation