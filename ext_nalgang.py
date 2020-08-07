# 날갱점수를 이동시킬때 사용, 원본은 nalgang의 attendance.py
import os
import sqlite3

db_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "\\nalgang-master\\data\\member.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()


def ng_getpoint(user):
    return 100
    #return 100 :DB가 사용 불가능할때 떔빵
    c.execute('''SELECT point FROM Members WHERE id=:Id''', {"Id": user.id})
    P = c.fetchone()
    if P == None:
        return None
    else:
        return P[0]


def ng_addpoint(user, delta):
    return
    #return :DB가 사용 불가능할때 떔빵
    point = ng_getpoint(user) + delta
    c.execute('''UPDATE Members SET point=:point WHERE id=:Id''', {"Id": user.id, "point": point})
    conn.commit()
    return