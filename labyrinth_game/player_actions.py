from .constants import ROOMS
from .utils import describe_current_room, random_event


def show_inventory(game_state) -> None:
    inventory = game_state.get("player_inventory", [])
    if not inventory:
        print('Ваш инвентарь пуст')
    else:
        print("Инвентарь:", ", ".join(inventory))

def get_input(prompt = "> "):
    try:
        user_input = input(prompt)
        return user_input.strip()
        
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state: dict, direction: str) -> None:
    """Перемещение игрока в выбранном направлении, если оно существует"""
    current = game_state["current_room"]
    room = ROOMS[current]

    exits = room.get("exits", {})
    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return
    
    game_state["current_room"] = exits[direction]
    game_state["steps_taken"] += 1

    describe_current_room(game_state)

    random_event(game_state)

def take_item(game_state: dict, item_name: str) -> None:
    """Функция взятия предмета"""
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    current_room = ROOMS[game_state["current_room"]]
    items = current_room.get("items", [])

    if item_name not in items:
        print("Такого предмета здесь нет.")
        return
    
    items.remove(item_name)
    game_state["player_inventory"].append(item_name)
    print(f"Вы подняли: {item_name}")

def use_item(game_state: dict, item_name: str) -> None:
    """Использование предметов"""
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return
    
    if item_name == "torch":
        print("Вы подняли факел, стало светлее вокруг.")
    elif item_name == "sword":
        print("Вы крепко схватили меч и почувствовали уверенность.")
    elif item_name == "bronze_box":
        print("Вы открываете бронзовую шкатулку...")
        if "rusty_key" not in inventory:
            print("Внутри лежит ржавый ключ. Вы кладёте его в инвентарь.")
            inventory.append("rusty_key")
        else:
            print("Шкатулка пуста.")
    else:
        print("Вы не знаете, как использовать этот предмет.")
