from flask import request, render_template
import telebot
import time
import os


def hello():
    return "Hello, World!"


def content():
    return '''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            '''


def configure_routes(app, bot):
    @app.route("/")
    def index():
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=os.getenv("URL"))

        return render_template("index.html", hello=hello(), content=content())

    @app.route('/webhook', methods=['POST'])
    def webhook():
        update = telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200
