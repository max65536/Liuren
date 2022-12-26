#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

# def next_id():
#     return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class Blog(Model):
    __table__='pan'
    id       = IntegerField(primary_key=True)
    classify = StringField(ddl='varchar(50)')
    sizhu    = StringField(ddl='varchar(50)')
    yuejiang = StringField(ddl='varchar(1)')

    classify = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(200)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)
    image=StringField(ddl='varchar(1000)')
    show=BooleanField()