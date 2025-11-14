#!/usr/bin/env python3

from .utils import describe_current_room
from .player_actions import (
    show_inventory, 
    get_input,
    move_player,
    take_item,
    use_item,
)

def process_command(game_state: dict, command_line: str) -> None:
    """Обработка команд"""
    parts = command_line.strip().split()
    if not parts:
        return
    
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    match cmd:
        case "look":
            describe_current_room(game_state)

        case "inventory":
            show_inventory(game_state)

        case "go":
            if arg is None:
                print("Укажите направление: go north / go east / ...")
            else:
                move_player(game_state, arg)
        
        case "take":
            if arg is None:
                print("Укажите предмет: take torch / take sword / ...")
            else:
                take_item(game_state, arg)

        case "use":
            if arg is None:
                print("Укажите предмет: use torch / use sword / ...")
            else:
                use_item(game_state, arg)

        case "quit" | "exit":
            game_state["game_over"] = True

        case _:
            print("Неизвестная команда.")



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
        process_command(game_state, command_row)





if __name__ == "__main__":
    main()
