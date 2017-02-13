#!/usr/bin/python

from app import model, app, db
import hashlib

if __name__ == "__main__":
    user = model.Users ()
    user.user_id = 'blackish'
    user.passwd = hashlib.md5 ( 'not4all' ).hexdigest ()
    db.session.add ( user )
    db.session.commit ()
