# engine/__init__.py
def initialize_gui(board_view, game_manager, main):
    """
    This function connects the board view, game manager, and main logic.
    Use this only if you're doing cross-module initialization.
    """
    board_view.set_game_manager(game_manager)
    game_manager.set_main(main)
    main.set_board_view(board_view)
