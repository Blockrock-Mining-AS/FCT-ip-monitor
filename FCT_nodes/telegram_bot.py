# -*- coding: utf-8 -*-
from datetime import datetime

import requests


class Bot(object):
    def __init__(self, token, chatid):
        self._chatID = chatid
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.content = None
        self.success = 0
        self.update_ids = []
        self.ack_time = None
        self.diff = 0
        self.WAIT_TIME = 900
        self.last_update = 0
        self.nodes_down = False

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        try:
            resp = requests.get(self.api_url + method, params)
            result_json = resp.json()
            self.success = 1
            return result_json
        except Exception as e:
            print(e)
            self.success = 0

    def get_last_update_id(self, updates):
        for update in updates["result"]:
            self.update_ids.append(int(update["update_id"]))
        return max(self.update_ids)

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return text, chat_id

    def node_down(self, list_of_nodes, list_of_users):
        if self.nodes_down:
            pass
        else:
            self.nodes_down = True

        self.last_update = datetime.now()

        if self.ack_time is None:
            tag_users = ['Maintenance team, you\'re up! Following node(s) are OFFLINE:\n']
            for i in list_of_nodes:
                tag_users.append("{} \n".format(i))
                for key, value in list_of_users.items():
                    temp = '<a href="tg://user?id=' + value + '">' + key + '</a>\n'
                    tag_users.append(temp)
                tag_users = ''.join(tag_users)
                self.send_message(self._chatID, tag_users, parse_mode='HTML')
        else:
            self.diff = (self.last_update - self.ack_time).total_seconds()
            if self.diff < 900:
                pass
            else:
                self.ack_time = None

    def handle_updates(self, telegram_updates, node_updates):
        for update in telegram_updates["result"]:
            if 'unedited_message' in update:
                text = update['unedited_message']["text"]
            elif 'message' in update:
                text = update['message']["text"]
            elif 'edited_message' in update:
                text = update['edited_message']["text"]

            if text == "/nodes":
                online_nodes_count = 0
                message = []
                for i in node_updates:
                    temp = str("Node: " + str(i['Node']) + "\n"
                                "Status: " + i['Status'] + "\n"
                                "Type: " + i['Type'] + "\n"
                                "Version: " + str(i['Version']) + "\n"
                                "Git build " + str(i['Git build']) + "\n"
                                "Sync [%]: " + str(i['Sync']) + "\n"
                                "My height: " + str(i['My height']) + "\n"
                                "Leader height: " + str(i['Leader height']) + "\n"
                                "Complete height: " + str(i['Complete height']) + "\n"
                                "Chain ID: " + str(i['Chainid'])) + "\n\n"
                    message.append(temp)
                    if i['Status'] == "ONLINE":
                        online_nodes_count += 1

                node_count_message = "Nodes online: {}/{}\n".format(online_nodes_count, len(node_updates))
                message.append(node_count_message)
                message = ''.join(message)
                self.send_message(self._chatID, message)

            elif text == "/ack":
                if self.nodes_down:
                    if self.ack_time is None:
                        self.ack_time = datetime.now()
                        message = "Acknowledged, pausing notifications for {} minutes.".format(self.WAIT_TIME/60)
                        self.send_message(self._chatID, message)
                    else:
                        message = "Already acknowledged, resetting timer to {} minutes again.".format(self.WAIT_TIME/60)
                        self.send_message(self._chatID, message)
                else:
                    self.send_message(self._chatID, "No nodes down, nothing to ack.")

            elif text == "/help":
                self.send_message(self._chatID, "The following commands are available:\n\n /nodes - lists info of all nodes\n\n"
                                                "/ack - aknowledges notifications and pauses notifications"
                                                " for 15 minutes when a node is offline ", 'HTML')

    def send_message(self, chat_id, text, parse_mode=None):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
