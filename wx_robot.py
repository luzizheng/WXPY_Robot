from wxpy import *
bot = Bot()

group_1 = bot.groups().search('图灵测试')[0]
group_2 = bot.groups().search('Family')[0]
group_3 = bot.groups().search('云世艺')[0]
group_4 = bot.groups().search('和谐文化社区')[0]

#不用艾特也可以接受消息的群组
group_free = [group_1,group_2,group_3,group_4]

# foshan_group = bot.groups().search('图灵测试')
# boss = foshan_group.search(u'Luzz')[0]
tuling = Tuling(api_key='a243e9074f3e4392aa28e0c7d5a8a8a4')

@bot.register(group_free,msg_types=TEXT)
def auto_reply_all(msg):
    if isinstance(msg.chat, Group):
    	if msg.is_at:
    		tuling.do_reply(msg)
    		print ('有人at了我')
    		print (msg)
    	elif '阿陆' in msg.text or '子铮' in msg.text or '曾哥' in msg.text or '铮哥' in msg.text or '啊陆' in msg.text:
    		tuling.do_reply(msg)
    		print ('有人提到我的名字')
    	else:
    		print ('没人提及我')
    		return
    else:
    	print ('私聊')
    	return
bot.join()