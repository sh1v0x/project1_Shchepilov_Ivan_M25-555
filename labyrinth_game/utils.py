import math

from .constants import ROOMS


def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")
    
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)

def trigger_trap(game_state: dict) -> None:
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы теряете предмет: {lost_item}.")
        return
    
    roll = pseudo_random(game_state["steps_taken"], 10)
    if roll < 3:
        print("Пол рассыпается под вами. Вы падаете в темноту...")
        print("Игра окончена.")
        game_state["game_over"] = True
    else:
        print("Вы чудом удержались на краю и выжили.")

def random_event(game_state: dict) -> None:
    seed = game_state["steps_taken"]
    roll = pseudo_random(seed, 10)
    if roll != 0:
        return
    
    event_type = pseudo_random(seed + 1, 3)

    current_room_id = game_state["current_room"]
    room = ROOMS[current_room_id]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        print("На полу Вы нашли монетку.")
        room_items = room.setdefault("items", [])
        room_items.append("coin")
        print("Монетка теперь лежит в этой комнате")
    elif event_type == 1:
        print("Вы слышите какой-то шорох недалеко от вас.")
        if "sword" in inventory:
            print("Вы крепче сжали меч - существо отступает во тьму.")
    elif event_type == 2:
        if current_room_id == "trap_room" and "torch" not in inventory:
            print("Что-то щелкнуло под вашими ногами. Это может быть ловушка.")
            trigger_trap(game_state)



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
        print("Заметные предметы:", ", ".join(items))

    # Доступные выходы
    exits = room.get("exits", [])
    if exits:
        print("Выходы:", ",".join(exits))
    
    # Наличие загадки
    puzzle = room.get("puzzle", [])
    if puzzle:
        print("Кажется, здесь есть загадка (используйте команду solve).")

    print()

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

def solve_puzzle(game_state: dict) -> None:
    """Функция решения загадок"""
    current_room_id = game_state["current_room"]
    room = ROOMS[current_room_id]
    puzzle = room.get("puzzle")

    if puzzle is None:
        print("Загадок здесь нет.")
        return
    
    question, answer = puzzle

    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    if user_answer == answer.lower():
        print("Верно! Загадка решена.")
        room["puzzle"] = None

        inventory = game_state["player_inventory"]
        if current_room_id == "hall" and "treasure_key" not in inventory:
            inventory.append("treasure_key")
            print("Вы находите особый ключ: treasure_key")
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state: dict) -> None:
    """Открыть сундук сокровищ в комнате сокровищ."""
    current_room_id = game_state["current_room"]

    if current_room_id != "treasure_room":
        print("Здесь ничего не открывали.")
        return
    
    room = ROOMS[current_room_id]
    items = room.get("items", [])
    inventory = game_state["player_inventory"]

    # Победа с использованием ключа
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove("treasure_chest")
        print("Вы находите сокровище в сундуке. Вы победили!")
        game_state["game_over"] = True
        return
    
    # Победа без использования ключа
    choice = input(
        "Сундук заперт. Хотите попробовать ввести код? (да/нет)"
    ).strip().lower()

    if choice == "нет":
        print('Вы отступаете от сундука.')
        return
    
    puzzle = room.get("puzzle")
    if puzzle is None:
        print("Код утерян. Взлом невозможен.")
        return
    
    question, correct_code = puzzle
    print(question)
    code = input("Введите код:").strip()

    if code == correct_code:
        print("Замок открывается! Сундук открыт!")
        items.remove("treasure_chest")
        print("Вы нашли сокровище! Победа!")
        game_state["game_over"] = True
    else:
        print("Неверный код.")


