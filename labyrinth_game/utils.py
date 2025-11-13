#!/usr/bin/env python3

from .constants import ROOMS

def describe_current_room(game_state: dict) -> None:
    current_room_id = game_state['current_room']
    room = ROOMS[current_room_id]

    # Название комнаты
    print(f"== {current_room_id.upper()} ==")

    # Описание комнаты
    print(room["description"])

    # Список предметов
    items = room.get("items", [])
    if items:
        print(f"Заметные предметы:", ",".join(items))

    # Доступные выходы
    exits = room.get("exits", [])
    if exits:
        print("Выходы:", ",".join(exits))
    
    # Наличие загадки
    puzzle = room.get("puzzle", [])
    if puzzle:
        print("Кажется, здесь есть загадка (используйте команду solve).")

    print()


