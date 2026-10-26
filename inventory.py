from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.items import ITEMS
from database import remove_item, require_player, update_player


def _render(query, player):
    inventory = {k: q for k, q in player["inventory"].items() if k in ITEMS}
    lines = [
        f"{ITEMS[k]['name']} x{q} — {ITEMS[k]['description']}"
        for k, q in inventory.items()
    ]
    text = (
        "🎒 <b>Inventário</b>\n\n"
        + ("\n".join(lines) if lines else "Sua mochila está vazia.")
        + f"\n\n💰 Ouro: {player['gold']}"
    )
    rows = [
        [InlineKeyboardButton(f"Usar {ITEMS[k]['name']}", callback_data=f"itemuse_{k}")]
        for k in inventory
        if ITEMS[k]["type"] == "consumable"
    ]
    rows.append([InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="main_menu")])
    query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(rows), parse_mode=ParseMode.HTML
    )


def show_inventory(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return
    query.answer()
    _render(query, player)


def use_item(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return

    key = query.data.split("_", 1)[1]
    item = ITEMS.get(key)
    if not item or not remove_item(context, key):
        query.answer("Você não tem esse item.", show_alert=True)
        _render(query, player)
        return

    changes = {
        stat: min(player[f"max_{stat}"], player[stat] + value)
        for stat, value in item["effect"].items()
    }
    update_player(context, **changes)
    query.answer(f"{item['name']} usado!")
    _render(query, player)
