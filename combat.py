import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.enemies import ENEMIES
from data.locations import LOCATIONS
from database import add_xp, require_player, update_player

FIGHT_KB = [
    [InlineKeyboardButton("⚔️ Atacar", callback_data="combat_attack")],
    [InlineKeyboardButton("🏃 Fugir", callback_data="combat_flee")],
]
MENU = [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="main_menu")]


def _edit(query, text, rows=FIGHT_KB):
    query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(rows), parse_mode=ParseMode.HTML
    )


def _status(player, enemy):
    return (
        f"❤️ {enemy['name']}: {max(0, enemy['hp_current'])}/{enemy['hp']}\n"
        f"🧑 Sua vida: {player['hp']}/{player['max_hp']}"
    )


def hunt(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return

    loc = LOCATIONS[player["location"]]
    if loc.get("safe") or not loc.get("enemies"):
        query.answer("Nenhum inimigo aqui!", show_alert=True)
        return

    query.answer()
    enemy = dict(ENEMIES[random.choice(loc["enemies"])])
    enemy["hp_current"] = enemy["hp"]
    context.user_data["enemy"] = enemy
    _edit(query, f"⚠️ <b>{enemy['name']} apareceu!</b>\n\n{_status(player, enemy)}")


def combat_attack(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return
    enemy = context.user_data.get("enemy")
    if not enemy:
        query.answer("Nenhum inimigo!", show_alert=True)
        return

    query.answer()
    dealt = max(1, player["attack"] - enemy["defense"] + random.randint(-2, 2))
    enemy["hp_current"] -= dealt

    if enemy["hp_current"] <= 0:
        _victory(query, context, player, enemy)
        return

    taken = max(1, enemy["attack"] - player["defense"] + random.randint(-1, 1))
    update_player(context, hp=max(0, player["hp"] - taken))

    if player["hp"] <= 0:
        _defeat(query, context, player)
        return

    _edit(
        query,
        f"⚔️ Você causa {dealt} de dano!\n💥 {enemy['name']} causa {taken} de dano!\n\n"
        f"{_status(player, enemy)}",
    )


def combat_flee(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return
    enemy = context.user_data.get("enemy")
    if not enemy:
        query.answer("Nenhum inimigo!", show_alert=True)
        return

    query.answer()
    if random.random() < 0.6:
        context.user_data.pop("enemy", None)
        _edit(
            query,
            "🏃 Você fugiu com segurança!",
            [[InlineKeyboardButton("🧭 Explorar", callback_data="explore")], MENU],
        )
        return

    taken = max(1, enemy["attack"] // 2)
    update_player(context, hp=max(0, player["hp"] - taken))

    if player["hp"] <= 0:
        _defeat(query, context, player)
        return

    _edit(
        query,
        f"❌ Falhou em fugir! Você sofre {taken} de dano.\n\n{_status(player, enemy)}",
    )


def _victory(query, context, player, enemy):
    gold = random.randint(enemy["gold_min"], enemy["gold_max"])
    update_player(context, gold=player["gold"] + gold)
    leveled_up, new_level = add_xp(context, enemy["xp_reward"])
    context.user_data.pop("enemy", None)

    text = (
        f"🏆 <b>Você derrotou {enemy['name']}!</b>\n"
        f"✨ +{enemy['xp_reward']} XP\n💰 +{gold} ouro"
    )
    if leveled_up:
        text += f"\n🎉 <b>Você subiu para o nível {new_level}!</b>"

    _edit(
        query,
        text,
        [
            [InlineKeyboardButton("🔍 Caçar novamente", callback_data="hunt")],
            [InlineKeyboardButton("🧭 Explorar", callback_data="explore")],
            MENU,
        ],
    )


def _defeat(query, context, player):
    lost = player["gold"] // 4
    update_player(
        context,
        hp=max(1, player["max_hp"] // 2),
        gold=player["gold"] - lost,
        location="vila",
    )
    context.user_data.pop("enemy", None)
    _edit(
        query,
        "💀 <b>Você foi derrotado...</b>\n"
        "Acordou na Vila Segura com metade da vida.\n"
        f"💰 Perdeu {lost} de ouro.",
        [MENU],
    )
