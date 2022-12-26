import logging
import aiomysql
def log(sql,args=()):
    logging.info('SQL:%s' %sql)

async def create_pool(loop,**kw):
    logging.info('create database: connecting pool...')
    global __pool
    __pool= await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )    

async def destroy_pool():
    global __pool
    if __pool is not None :
        __pool.close()
        await __pool.wait_closed()

async def execute(sql,args,autocommit=True):
    log(sql)
    with(await __pool)as conn:
        if not autocommit:
            await conn.begin()
        try:
            cur= await conn.cursor()
            await cur.execute(sql.replace('?','%s'),args)
            affected=cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
        # SQL语句的占位符是?，而MySQL的占位符是%s
            await cur.execute(sql.replace('?','%s'),args or ())
            if size:
                rs= await cur.fetchmany(size)
            else:
                rs=await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' %len(rs))
        return rs

def create_args_string(num):
    lol=[]
    for n in range(num):
        lol.append('?')
    return (','.join(lol))


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

# StringField, BooleanField, FloatField, TextField
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None,primary_key=False,default=0):
        super().__init__(name, 'int', primary_key, default)

class FloatField(Field):
    """docstring for FloatField"""
    def __init__(self, name=None,primary_key=False,default=0.0):
        super().__init__(name,'float',primary_key,default)

class TextField(Field):
    def __init__(self, name=None,primary_key=False,default=None):
        super().__init__(name,'text',False,default)

def create_args_string(num):
    args=[]
    for n in range(num):
        args.append('?')
    return (','.join(args))

class Model(object):
    def __init__(self,**kw):
        host = 'localhost'
        port = 3306
        db = 'liuren'
        user = 'root'
        password = 'root'

        self.dataBase = mysql.connector.connect(
        host =host,
        user =user,
        passwd =password,
        database="liuren"
        )
        self.cursorObject = self.dataBase.cursor()

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object have no attribution %s"%key)

    def __setattr__(self,key,value):
        self[key]=value

    def getValue(self,key):
        return getattr(self,key,None)

    def getValueOrDefault(self,key):
        value=getattr(self,key,None)
        if value is None:
            field=self.__mappings__[key]
            if field.default is not None:
                value=field.default() if callable(field.default) else field.default
                #???????
                logging.debug('using default value for %s:%s'%(key,str(value)))
                setattr(self,key,value)
        return value

    #获取表里符合条件的所有数据,类方法的第一个参数为该类名
    @classmethod
    async def find(cls,pk):
        'find object by primaryKey'
        rs=await select('%s where `%s`=?'%(cls.__select__,cls.__primary_key__),[pk],1)
        if len(rs)==0:
            return None
        return cls(**rs[0])

    async def select(sql,args,size=None):
        log(sql,args)
        global __pool
        async with __pool.get() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
            # SQL语句的占位符是?，而MySQL的占位符是%s
                await cur.execute(sql.replace('?','%s'),args or ())
                if size:
                    rs= await cur.fetchmany(size)
                else:
                    rs=await cur.fetchall()
            await cur.close()
            logging.info('rows returned: %s' %len(rs))
            return rs        

    @classmethod
    async def findAll(cls, where=None, args=None,**kw):
        'find objects by where clause'
        sql=[cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args=[]
        orderBy=kw.get('orderBy',None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit=kw.get('limit')
        if limit is not None:
            sql.append('limit')
            if isinstance(limit,int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit,tuple) and len(limit)==2:
                sql.append('?,?')
                args.extend(limit)#extend 用来连接 list
            else:
                raise ValueError('Invalid limit value %s'% str(limit))
        rs=await select(' '.join(sql),args)
        return[cls(**r) for r in rs]
        # rs=[]
        # if len(kw)==0:
        #     rs=await select(cls.__select__,None)
        # else:
        #     args=[]
        #     values=[]
        #     for k,v in kw.items():
        #         args.append('%s=?'%k)
        #         values.append(v)
        #     # print('%s where %s'%(cls.__select__,'and'.join(args),values))
        # return rs
    @classmethod
    async def findNumber(cls,selectField,where=None,args=None):
        'find number by select and where'
        #反单引号在SQL语句中表示库、表、字段等名称
        #selectField='count(1)'或者'count(*)'、'count(id)'
        #_num_给查询结果命名
        sql=['select %s _num_ from `%s`'%(selectField,cls.__table__)]
        # sql=: ['select count(id) _num_ from `blogs`']
        if where:
            sql.append('where')
            sql.append(where)
        rs=await select(' '.join(sql),args,1)
        if len(rs)==0:
            return None
        print(rs)
        return rs[0]['_num_']

    async def remove(self):
        args=[self.getValue(self.__primary_key__)]
        rs=await execute(self.__delete__,args)
        if rs!=1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rs)

    async def update(self):
        args=list(map(self.getValue,self.__fields__))
        #'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)

        #update `blogs` set `content`=?, `user_id`=?, `created_at`=?, `user_image`=?, `name`=?, `summary`=?, `user_name`=? where `id`=?
        args.append(self.getValueOrDefault(self.__primary_key__))
        print('save"%s'%args)
        rows=await execute(self.__update__,args)
        if rows!=1:
            print(self.__insert__)
            logging.warning('failed to insert record: affected rows:%s'%rows)

    async def save(self):
        args=list(map(self.getValueOrDefault,self.__fields__))
        # print('save"%s'%args)
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows=await(execute(self.__insert__,args))
        if rows!=1:
            print(self.__insert__)
            logging.warning('failed to insert record: affected rows:%s'%rows)


    def __select__(self, primaryKey, escaped_fields, tableName):
        sql = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        return sql
    
    def __insert__(self, primaryKey, escaped_fields, tableName):
        sql = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
    
    def __update__(self, primaryKey, tableName, fields):
        pass
        # sql = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
    
    def __delete__(self, tableName, primaryKey):
        sql = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)            