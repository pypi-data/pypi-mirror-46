# -*- coding: utf-8 -*-
"""
Description: 
Author     : Groom
Time       : 2018/10/9
File       : mysql.py
Version    : V0.1
"""

from mysql.connector import errorcode
from mysql.connector.cursor import MySQLCursorDict
from mysql.connector.pooling import MySQLConnectionPool
# class mysql_conf():
#     DB_HOST = ""
#     DB_PORT = 3306
#     DB_NAME = ""
#     DB_USER = ""
#     DB_PWD = ""
#     DB_CHAR = ""
#     DB_MIN_CACHED = 200
#     DB_MAX_CACHED = 200
#     DB_MAX_SHARED = 3000
#     DB_MAX_CONNECYIONS = 10000
#     DB_BLOCKING = True
#     DB_MAX_USAGE = 0
#     DB_SET_SESSION = None

class MYSQL(object):
    __pool = None

    def __init__(self,host='',port=3306,database='',user='',password='',poolsize=5):
        self.__conn = MYSQL.__getConn(host,port,database,user,password,poolsize)
        self.__cursor = self.__conn.cursor()

    @staticmethod
    def __getConn(host='',port=3306,database='',user='',password='',poolsize=5):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        # if MYSQL.__pool is None:
        #     __pool = PooledDB(creator=mysql, mincached=1, maxcached=20,
        #                       host=mysql_conf.DB_HOST, port=mysql_conf.DB_PORT,
        #                       user=mysql_conf.DB_USER, passwd=mysql_conf.DB_PWD,
        #                       db=mysql_conf.DB_NAME, use_unicode=False,
        #                       charset=mysql_conf.DB_CHAR,
        #                       cursorclass=MySQLCursorDict)
        # return __pool.connection()
        dbconfig = {
            'host': host,
            'port': port,
            "database": database,
            "user": user,
            "password": password,
            "charset": 'utf8'
        }
        if MYSQL.__pool is None:
            __pool = MySQLConnectionPool(pool_name="mypool",
                                         pool_size=poolsize,
                                         **dbconfig)
        return __pool.get_connection()

    def query(self, sql):
        exec_info = 'False'
        try:
            exec_info = self.__cursor.execute(sql)
        except Exception as e:
            print(e)
        if exec_info is None:
            reslut = self.__cursor.fetchall()
            return reslut
        else:
            return False

    def createTable(self, TABLES):
        for name, ddl in TABLES.items():
            try:
                print("创建表:{}: ".format(name), end='-------')
                self.__cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("表已经存在！")
                    return False
                else:
                    print(err.msg)
                    return False
            else:
                print("{}表创建成功。".format(name))
                self.__conn.commit()
                return True

    def insertMany(self, sql, datavalues):
        try:
            exec_info = self.__cursor.executemany(sql, datavalues)
        except Exception as e:
            print(e)
            return False
        self.__conn.commit()
        return True

    def insertOne(self, sql, datavalue):
        try:
            exec_info = self.__cursor.execute(sql, datavalue)
        except Exception as e:
            print(e)
            return False
        self.__conn.commit()
        return True

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self.__conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self.__conn.commit()
        else:
            self.__conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self.__cursor.close()
        self.__conn.close()

    def insertRunLog(self, datavalue):
        sql = ("INSERT INTO runlog "
               "(time, type, message) "
               "VALUES (%s, %s, %s)")
        try:
            self.insertOne(sql, datavalue)
        except Exception as e:
            print(e)

    def insertSignales(self, datavalue):
        sql = ("INSERT INTO signales "
               "(symbol, strategy, signal_time, signal_type, cur_price) "
               "VALUES (%s, %s, %s, %s, %s)")
        try:
            self.insertOne(sql, datavalue)
        except Exception as e:
            print(e)

    def get_cursor(self):
        return self.__cursor


if __name__ == "__main__":
    TABLES = {}
    TABLES['test'] = (
        "CREATE TABLE `test` ("
        "  `emp_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `name` varchar(14) NOT NULL,"
        "  `gender` enum('M','F') NOT NULL,"
        "  `hire_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_id`)"
        ") ENGINE=InnoDB")

    insert_sql = ("INSERT INTO test "
                  "(emp_id, name, gender, hire_date) "
                  "VALUES (%(emp_id)s, %(name)s, %(gender)s, %(hire_date)s)")
    insert_sql2 = ("INSERT INTO test "
                   "(name, gender, hire_date) "
                   "VALUES (%s, %s, %s)")
    data = [
        {'emp_id': 3,
         'name': 'z003',
         'gender': 'M',
         'hire_date': '2018-9-1'
         },
        {'emp_id': 4,
         'name': 'z004',
         'gender': 'F',
         'hire_date': '2018-9-2'
         },
    ]
    data2 = [
        ('z001', 'M', '2018-9-1'),
        ('z002', 'F', '2018-9-2'),
    ]
    testdb = MYSQL(host="127.0.0.1",port=3306,database='trading',user='coin_user1',password='coinuser1')
    sql = 'select * from runlog limit 10'

    # info = testdb.createTable(TABLES)
    #info = testdb.insertMany(insert_sql2, data2)
    info2 = testdb.query(sql)
    #print(info)
    print(info2)
