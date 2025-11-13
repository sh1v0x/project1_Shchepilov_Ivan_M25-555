#!/usr/bin/env python3


def show_inventory(game_state) -> None:
    inventory = game_state.get("player_inventory", [])
    if not inventory:
        print('Ваш инвентарь пуст')
    else:
        print("Инвентарь:" ",".join(inventory))

def get_input(prompt = "> "):
    try:
        user_input = input(prompt)
        return user_input.strip()
        
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"