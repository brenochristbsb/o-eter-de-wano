
import logging
import os
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from config import BOT_TOKEN
from combat import combat_attack, combat_flee, hunt
from explore import enter_location, locked_location, rest, show_explore
from inventory import show_inventory, use_item
from lore import show_lore
from menu import main_menu
from start import choose_class, choose_nation, start
from status import show_status

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

PORT = int(os.environ.get("PORT", "10000"))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK - O Eter de Wano")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


def start_http_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


def soon_handler(update, context):
    if update.callback_query:
        update.callback_query.answer(
            "Em breve! Ainda estamos construindo esta área.",
            show_alert=True,
        )


def main():
    if not BOT_TOKEN:
        raise SystemExit("Defina BOT_TOKEN nas variáveis de ambiente.")

    Thread(target=start_http_server, daemon=True).start()

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(choose_nation, pattern=r"^nation_.+$"))
    dp.add_handler(CallbackQueryHandler(choose_class, pattern=r"^class_.+$"))
    dp.add_handler(CallbackQueryHandler(main_menu, pattern=r"^main_menu$"))
    dp.add_handler(CallbackQueryHandler(show_explore, pattern=r"^explore$"))
    dp.add_handler(CallbackQueryHandler(enter_location, pattern=r"^go_.+$"))
    dp.add_handler(CallbackQueryHandler(locked_location, pattern=r"^locked$"))
    dp.add_handler(CallbackQueryHandler(rest, pattern=r"^rest$"))
    dp.add_handler(CallbackQueryHandler(hunt, pattern=r"^hunt$"))
    dp.add_handler(CallbackQueryHandler(combat_attack, pattern=r"^combat_attack$"))
    dp.add_handler(CallbackQueryHandler(combat_flee, pattern=r"^combat_flee$"))
    dp.add_handler(CallbackQueryHandler(show_status, pattern=r"^status$"))
    dp.add_handler(CallbackQueryHandler(show_inventory, pattern=r"^inventory$"))
    dp.add_handler(CallbackQueryHandler(use_item, pattern=r"^itemuse_.+$"))
    dp.add_handler(CallbackQueryHandler(show_lore, pattern=r"^lore$"))
    dp.add_handler(CallbackQueryHandler(soon_handler))

    logging.info("Bot O Eter de Wano iniciado.")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
