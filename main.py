import time

from FCT_nodes.node import Node
from FCT_nodes.node_collection import NodeCollection
from FCT_nodes.telegram_bot import Bot


def main():
    node_collection = NodeCollection()
    bot = Bot(token='TELEGRAM-BOT-TOKEN',
              chatid='chatID')
    # List of your current nodes.
    list_of_nodes = ['IP:PORT, '
                     'IP:PORT']

    # List of users to tag @ telegram if node(s) are offline.
    list_of_users = {'Name': 'userID',
                     'Name2': 'userID'}

    for i in list_of_nodes:
        node_collection.append(Node(i))

    last_update_id = None
    while True:
        # Get new messages @ telegram
        telegram_updates = bot.get_updates(last_update_id)
        # Get node info.
        node_collection.refresh_all()
        node_updates = node_collection.get_all()

        try:
            if len(telegram_updates["result"]) > 0:
                last_update_id = bot.get_last_update_id(telegram_updates) + 1
                bot.handle_updates(telegram_updates, node_updates)
        except Exception as e:
            print(e)

        # If node down, alert maintenance team @telegram
        nodes_down = []
        for i in node_updates:
            if i['Status'] == "OFFLINE":
                nodes_down.append(i['Node'])
        if len(nodes_down) != 0:
            bot.node_down(nodes_down, list_of_users)

        time.sleep(1)

if __name__ == '__main__':
    main()

