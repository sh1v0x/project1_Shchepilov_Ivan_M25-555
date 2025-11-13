#!/usr/bin/env python3

from .constants import ROOMS
from .utils import describe_current_room
from .player_actions import show_inventory, get_input

def main() -> None:
    game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
    }

    print('Добро пожаловать в Лабиринт сокровищ!')
    print()

    # Описание стартовой комнаты
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command_row = get_input("> ")
        command = command_row.lower().strip()

        if command == "quit":
            game_state["game_over"] = True
        elif command == "inventory":
            show_inventory(game_state)
        elif command == "look":
            describe_current_room(game_state)






if __name__ == "__main__":
    main()
