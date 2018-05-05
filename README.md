# FCT IP monitoring

## Description
Retrieves FCT node info from the control panel, and sends this info
to a chosen telegram group/user.

## Dependencies
Python modules:
- BeautifulSoup4
- requests
- htmls

## Installation
### Creating a telegram bot
To be able to use this script properly you'll need to setup a telegram bot.
The info received from the nodes will be sent to your chosen group/user
on telegram through Telegram's infrastructure.

To register a telegram bot you need to first create a personal Telegram
account, this can be done [here](web.telegram.org). After registering,
you can create a new Telegram Bot by using BotFather. Go to
[telegram.me/botfather](https://telegram.me/botfather) and start a conversation
by sending the following command:

    /newbot

You should receive a reply asking you to choose a name for the bot. After
doing so BotFather will ask you to pick a username for the bot, the username
has to end with "bot". You will then receive a token, which in the main.py file
is referred to as TELEGRAM-BOT-TOKEN. Save this somewhere safe.

Make your desired group chat with the users you want to be part of the monitoring team and invite your bot the group, send a test command like:

    /test @<YOUR-BOT-USERNAME>

Visit the following URL in the browser:

    https://api.telegram.org/bot<TELEGRAM-BOT-TOKEN>/getUpdates

You should see something similar to:

    "message":{"message_id":4,"from":{"id":401234137,"is_bot":false,"first_name":"laende","last_name":"","username":"laende"},"chat":{"id":-229628212,"title":"GroupChatName","type":"group","all_members_are_administrators":true},"date":1525451147,"text":"/test @FCT_for_example_only_bot","entities":[{"offset":0,"length":5,"type":"bot_command"},{"offset":6,"length":25,"type":"mention"}]}}]}

For this case the "id":-229628245 is the groupchats ID. save this. To get the userID for every member in the group, they have to mention the bot in the chat.
The userID is also listed in the JSON result.

Thats it, now you got everything setup for the telegram bot.


### Installing the Python modules
clone the repository and install the mentioned dependencies with:

    pip install BeautifulSoup4
    pip install requests
    pip install htmls

## Usage
Navigate to the repository and open the main.py file.

    nano main.py

Edit the following lines:

    # Initiate telegram bot with your bot token and chatID
    bot = Bot(token='TELEGRAM-BOT-TOKEN', chatid='chatiID')

    # List of your current nodes.
    list_of_nodes = ['IP:PORT']

    # List of users to tag @ telegram if node(s) are offline.
    list_of_users ={'Name': 'userID',
                    'Name': 'userID',
                    'Name': 'userID',
                    'Name': 'userID'}

Example of edit:

    # Initiate telegram bot with your bot token and chatID
    bot = Bot(token='123456789:ABCDEFGHiJ-gasTrdan1-abcdsK-abcthsc',
              chatid='12345678')

    # List of your current nodes.
    list_of_nodes = ['1.2.3.4:9999',
                     '1.2.3.5:9999']

    # List of users to tag @ telegram if node(s) are offline.
    list_of_users ={'Ola': '12345678',
                    'Nordmann': '12345578'}

Save and exit. Run it with:

    nohup /path/to/main.py &

Now in your telegram group you can send the following commands:

    /nodes - lists info of all your nodes in your node list.
    /ack - The bot will send notifications and tag users if a node is down. Use this command to pause notifications for 15 minutes.
    /help - list the mentioned commands.

From the /nodes command, you should receive a message similar to:

    Node: http://IP:PORT
    Status: ONLINE
    Version: 5.0.0
    Git build e549cfbfbc3cc35b411231234632c1aaaf47f503
    Sync [%]: 100.0
    My height: 27550
    Leader height: 27551
    Complete height: 27550
    Type: Audit
    Chain ID: 888888dc16a02e27f184353ac046e8ca2e052be873809af3dc86907bdhga51

    Nodes online: 1/1






