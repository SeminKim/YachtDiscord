import os
import sqlite3
import time

db_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "\\nalgang-master\\data\\member.db"
if not os.path.isfile(db_path):
    raise FileNotFoundError
conn = sqlite3.connect(db_path)
c = conn.cursor()


def ng_getpoint(user):
    c.execute('''SELECT point FROM Members WHERE id=:Id''', {"Id": user.id})
    P = c.fetchone()
    if P == None:
        return None
    else:
        return P[0]


def ng_addpoint(user, delta):
    with open('data/log.txt', 'a') as f:
        f.write(f'{delta} point added to {user}, now {ng_getpoint(user)}, executed at {time.ctime()}\n')
    point = ng_getpoint(user) + delta
    c.execute('''UPDATE Members SET point=:point WHERE id=:Id''', {"Id": user.id, "point": point})
    conn.commit()

    return


def ng_movepoint(sender, receiver, point):
    ng_addpoint(receiver, point)
    ng_addpoint(sender, -1 * point)


# test code
"""
def ng_getpoint(user):
    return 100


def ng_addpoint(user, delta):
    return


def ng_movepoint(sender, receiver, point):
    ng_addpoint(receiver, point)
    ng_addpoint(sender, -1 * point)
"""
