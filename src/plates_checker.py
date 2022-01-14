#!/usr/bin/python
import datetime
import os.path
import sqlite3
from alert_mail_sender import AlertMailSender

def process_plates(plates_list: list):
    try:
        print(plates_list)
        db = sqlite3.connect("data/plates.db", )
        cur = db.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS plates(id INTEGER PRIMARY KEY AUTOINCREMENT, plate TEXT, owner TEXT,\
            updated TEXT, creation TEXT, known INT, cntr INT, quality INT)""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS observations(id INTEGER PRIMARY KEY AUTOINCREMENT, \
             image TEXT, confidence REAL, ts TEXT, plate_id INT)""")
        db.commit()
        for plate in plates_list:
            cur.execute("SELECT id,cntr,owner FROM plates WHERE plate=?", (plate['plate'],))
            res = cur.fetchall()

            if len(res) > 0:
                observation = (plate['confidence'],
                               datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                               res[0][0],
                               plate['file'],)
                print(observation)
                cur.execute("INSERT INTO observations(confidence, ts, plate_id, image) VALUES" + str(observation))
                cur.execute("UPDATE plates SET updated = \""+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                            + "\", cntr = " + str(res[0][1]+1) + " WHERE id = " + str(res[0][0]))
                db.commit()
                if res[0][2] == "UNKWN":
                    AlertMailSender(plate['plate']).\
                        send_alert_mail_with_attachment(os.path.join("data/images", plate['file']))
            else:
                cur.execute("INSERT INTO plates(plate,creation,updated,known,quality,cntr,owner) VALUES(\"" +
                            plate['plate'] + "\",\"" +
                            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "\",\"" +
                            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + "\"," +
                            "0,100,1,\"UNKWN\")")
                db.commit()
                observation = (plate['confidence'],
                               datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                               cur.lastrowid,
                               plate['file'],)
                cur.execute("INSERT INTO observations(confidence, ts, plate_id, image) VALUES" + str(observation))
                db.commit()
                print("New plate inserted: " + plate['plate'])
                AlertMailSender(plate['plate']).\
                    send_alert_mail_with_attachment(os.path.join("data/images", plate['file']))
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        db.close()
    except FileNotFoundError as e:
        print(e)
