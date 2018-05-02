# -*- coding: utf-8 -*-

import telepot

class Bot(object):
    def __init__(self, token, chatid):
        self._chatID = chatid
        self._bot = telepot.Bot(token)

    def send_message(self, data, users):
        online_nodes_count = 0
        tag_users = ['Maintenance team, you''re up!\n']
        for i in data:
            if i['Status'] == "ONLINE":
                online_nodes_count += 1
                message = str("Node: " + i['Node'] + "\n"
                              "Status: " + i['Status'] + "\n"
                              "Type: " + i['Type'] + "\n"
                              "Version: " + i['Version'] + "\n"
                              "Sync [%]: " + str(i['Sync'])
                              )
                self._bot.sendMessage(chat_id=self._chatID, text=message, parse_mode='HTML')
            else:
                message = str("Node: " + i['Node'] + "\n"
                              "Status: " + i['Status'] + "\n"
                              "Type: " + i['Type'] + "\n"
                              "Version: " + i['Version'] + "\n"
                              "Sync [%]: " + str(i['Sync']))
                self._bot.sendMessage(chat_id=self._chatID, text=message, parse_mode='HTML')

                for key, value in users.items():
                    temp = '<a href="tg://user?id=' + value + '">' + key + '</a>\n'
                    tag_users.append(temp)
                tag_users = ''.join(tag_users)
                self._bot.sendMessage(chat_id=self._chatID, text=tag_users, parse_mode='HTML')

        node_count_message = "Nodes online: {}/{} \n ------------------------------------------------" .format(online_nodes_count,
                                                                                                 len(data))
        self._bot.sendMessage(chat_id=self._chatID, text=node_count_message, parse_mode='HTML')