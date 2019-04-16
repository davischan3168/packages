from wxpy import *
import sys
import os
bot = Bot(cache_path=True)
def frds(name):
    tmp=bot.friends().search(name)[0]
    return tmp

def grds(name):
    tem=bot.groups.search(name)[0]
    return tem
@bot.register()
def print_others(msg):
    print(msg)
"""
# 回复 my_friend 发送的消息
@bot.register(my_friend)
def reply_my_friend(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)
 
# 回复发送给自己的消息，可以使用这个方法来进行测试机器人而不影响到他人
@bot.register(bot.self, except_self=False)
def reply_self(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)
 
# 打印出所有群聊中@自己的文本消息，并自动回复相同内容
# 这条注册消息是我们构建群聊机器人的基础
@bot.register(Group, TEXT)
def print_group_msg(msg):
    if msg.is_at:
        print(msg)
        msg.reply(meg.text)

# 发送文本
my_friend.send('Hello, WeChat!')
# 发送图片
my_friend.send_image('my_picture.png')
# 发送视频
my_friend.send_video('my_video.mov')
# 发送文件
my_friend.send_file('my_file.zip')
# 以动态的方式发送图片
my_friend.send('@img@my_picture.png')
"""
