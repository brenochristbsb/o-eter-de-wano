def get_player(context):
    return context.user_data.get("player")


def update_player(context, **kwargs):
    player = get_player(context)
    if player is not None:
        player.update(kwargs)
    return player


def require_player(update, context):
    player = get_player(context)
    if not player:
        update.callback_query.answer(
            "Use /start para criar seu personagem.", show_alert=True
        )
    return player


def add_xp(context, amount):
    player = get_player(context)
    player["xp"] += amount
    leveled_up = False

    while player["xp"] >= player["level"] * 100:
        player["xp"] -= player["level"] * 100
        player["level"] += 1
        player["max_hp"] += 10
        player["max_mp"] += 5
        player["attack"] += 2
        player["defense"] += 1
        leveled_up = True

    if leveled_up:
        player["hp"] = player["max_hp"]
        player["mp"] = player["max_mp"]
    return leveled_up, player["level"]


def remove_item(context, item_id, qty=1):
    inventory = get_player(context)["inventory"]
    if inventory.get(item_id, 0) < qty:
        return False
    inventory[item_id] -= qty
    if inventory[item_id] <= 0:
        del inventory[item_id]
    return True
