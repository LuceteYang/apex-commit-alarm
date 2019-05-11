# coding: utf-8
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

import datetime
import random
import smtplib

from github import Github



message_list = [
    u'커밋좀;',
    u'저기여, 커밋인데여. 오늘 커밋 안하세여?',
    u'커밋은 하고 자야지?',
    u'커밋하세에ㅔㅔㅔㅔㅁㅁㅁ!!!!빼애ㅐㅣ애애애액!!!!!!!!!',
    u'커밋해야 한다(수화기를 들며)',
    u'커밋 컴 윗 미 컴윗',
    u'Make Commit log Great Again',
    u'1 Day 1 Commit (찡긋)'
]

def send_mail(msg):
    parser = SafeConfigParser()
    parser.read('gmail.ini')

    gmail_sender = parser.get('gmail', 'gmail_sender')
    gmail_passwd = parser.get('gmail', 'gmail_passwd')

    TO = gmail_sender
    SUBJECT = 'Github Commit Alarm MAIL'
    TEXT = msg

    # Gmail Sign In
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    BODY = BODY.encode("utf-8")
    try:
        server.sendmail(gmail_sender, [TO], BODY)
    except Exception as inst:
        print('error sending mail',inst)

    server.quit()

def get_github_account_info():
    parser = SafeConfigParser()
    parser.read('github.ini')

    username = parser.get('github', 'username')
    password = parser.get('github', 'password')

    return username, password


def get_today_commit_events(user):
    today = datetime.datetime.today()
    today_date = datetime.datetime(today.year, today.month, today.day)
    today_date_ko = today_date - datetime.timedelta(hours=9)

    commit_events = []

    for event in user.get_events():
        if event.created_at > today_date_ko:
            if event.type in ['CreateEvent','PushEvent', 'PullRequestEvent']:
                commit_events.append(event)
        else:
            break

    return commit_events


def handle(event, context):
    username, password = get_github_account_info()

    client = Github(username, password)

    today_commit_events = get_today_commit_events(client.get_user(username))

    if len(today_commit_events) == 0:
        send_mail(random.choice(message_list))
    else:
        send_mail('today commit count : %s' % len(today_commit_events))
    return {
        'message' : 'Hello World'
    }