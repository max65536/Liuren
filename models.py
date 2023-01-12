#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

# def next_id():
#     return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class DocumentModel(Model):
    __table__='pan'
    id       = IntegerField(primary_key=True)
    classify = StringField(ddl='varchar(45)')
    sizhu    = StringField(ddl='varchar(50)')
    yuejiang = StringField(ddl='varchar(1)')
    tianpan  = StringField(ddl='varchar(12)')
    dungan   = StringField(ddl='varchar(12)')
    question = StringField(ddl='varchar(100)')
    sike     = StringField(ddl='varchar(12)')
    sanchuan = StringField(ddl='varchar(12)')

    tianjiangpan  = StringField(ddl='varchar(12)')

    message_id = IntegerField(default=0)

    created_at = FloatField(default=time.time())
    image=StringField(ddl='varchar(1000)')
    huoshi=BooleanField(default=False)