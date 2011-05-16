from config import *
from utils import *
from irc import *
import re

def bhottu_init():
    dbExecute('''create table if not exists nickplus (
              nickplusID int auto_increment primary key,
              name varchar(255),
              points int,
              unique(name) )''')

def nickPlus(parsed):
    if parsed['event'] == 'PRIVMSG':
        message = parsed['event_msg']
        nick = parsed['event_nick']
        uname = re.search('^\w+(?=\+{2})', message)
        pointnum = None
        if uname is not None:
            uname = uname.group()
            log('nickPlus(): message: ' + message)
            log('nickPlus(): nick: ' + nick)
            log('nickPlus(): uname: ' + uname)
            uname = uname.replace('++', '').rstrip()
            if uname == nick:
                sendMessage(nick, 'Plussing yourself is a little sad, is it not?')
                return
            uname = uname.replace('++', '')
            try:
                pointnum = int(dbQuery('SELECT points FROM nickplus WHERE name=%s', [uname])[0][0])
            except:
                log('nickPlus(): Something went wrong!')
            if pointnum is not None:
                sendMessage(CHANNEL, 'incremented by one')
                pointnum += 1
                dbExecute('UPDATE nickplus set points=%s WHERE name=%s', [pointnum, uname])
                log('nickPlus(): Incremented by 1 ' + uname)
            elif pointnum == None:
                sendMessage(CHANNEL, 'Added record')
                dbExecute('INSERT INTO nickplus (name, points) VALUES (%s, %s)', [uname, 1])
                log('nickPlus(): Incremented by 1 ' + uname)


def queryNick(parsed):
    if parsed['event'] == 'PRIVMSG':
        message = parsed['event_msg']
        nick = parsed['event_nick']
        combostring = NICK + ", tell me about "
        if combostring in message:
            uname = message.split(combostring)[1].replace('++', '')
            log('queryNick(): Querying DB with: ' + uname)
            try:
                pointnum = int(dbQuery('SELECT points FROM nickplus WHERE name=%s', [uname])[0][0])
                sendMessage(CHANNEL, '%s, Points for %s = %s' % (nick, uname, pointnum))
            except:
                pass


def NickScore(parsed):
    nickPlus(parsed)
    queryNick(parsed)