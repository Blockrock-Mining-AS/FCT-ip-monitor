from FCT_nodes.node import Node
from FCT_nodes.node_collection import NodeCollection
from FCT_nodes.telegram_bot import Bot

if __name__ == '__main__':
    node_collection = NodeCollection()
    bot = Bot(token='TELEGRAM-BOT-TOKEN', chatid='chatiID')

    # List of your current nodes.
    list_of_nodes = ['IP:PORT']

    # List of users to tag @ telegram if node(s) are offline.
    list_of_users ={'Name': 'userID',
                    'Name': 'userID',
                    'Name': 'userID',
                    'Name': 'userID'}


    for i in list_of_nodes:
        node_collection.append(Node(i))

    # Retrieve and refresh node info
    node_collection.refresh_all()

    # Print
    node_collection.print_all()

    # Get info in a list of dicts
    node_info = node_collection.get_all()

    print(node_info)

    bot.send_message(node_info, list_of_users)
