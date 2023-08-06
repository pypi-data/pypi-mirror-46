# -*- coding: utf-8 -*-
"""
Description: 
Author     : Groom
Time       : 2018/10/9
File       : exchange_to_mysql.py
Version    : V0.1
"""

import pandas as pd

pd.set_option('expand_frame_repr', False)
import time, datetime
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine, schema
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

import collections
from patgroom.utils import dt
from patgroom import resamplebase
from patgroom.database import mysql_pool
from patgroom.exchange_api.bitfinex2API import BitfinexV2API

bfx2 = BitfinexV2API()

# info = bfx2.candles(symbol=symbol.split('/')[0].upper(), TimeFrame=timeframe, Section='hist', start=since)

TABLES = {}

kline_1m_table_temple2 = '(`index` int(10) NOT NULL AUTO_INCREMENT,' \
                         '`symbol` varchar(16),' \
                         '`timestamp` varchar(13),' \
                         '`open` float,' \
                         '`high` float,' \
                         '`low` float,' \
                         '`close` float,' \
                         '`vol` float,' \
                         '`date` datetime,' \
                         '`verify` BOOL,PRIMARY KEY(`index`)) ENGINE=InnoDB'
insert_data_temple2 = '(symbol,timestamp,open,high,close,vol)' \
                      'VALUES (%(symbol)s,%(timestamp)s,%(open)s,%(high)s,%(close)s,%(vol)s)'

add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")


def is_exist_table(cursor, table_name):
    try:
        cursor.execute('select symbol from ' + table_name + 'limit 3')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            return True
        else:
            return err.msg
    else:
        return False


def create_table(cursor, table_name, ddl):
    try:
        print(r'[%s]创建表结构-%s' % (dt.fmt_now(), table_name), end=' ')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(r'[%s]%s表已经存在！' % (dt.fmt_now(), table_name))
        else:
            print(err.msg)
    else:
        print('%s表创建成功！' % table_name)


def insert_table(cnx, cursor, table_name, ddl, data):
    try:
        cursor.execute(ddl, data)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print(r'[%s]数据已经保存到表%s' % (dt.fmt_now(), table_name))


def get_kline_data(symbol='EOS/USDT', timeframe='1m', since='', end=None, limit=1000):
    df = pd.DataFrame(columns=['symbol', 'timestamp', 'Open', 'High', 'Low', 'Close', 'Vol'])
    # print('timeframe:%s' % timeframe)
    # print('since:%s' % since)
    df_temp = pd.DataFrame(
        bfx2.candles(symbol=symbol.split('/')[0].upper(), TimeFrame=timeframe, Section='hist', start=since, sort=1),
        columns=['timestamp', 'Open', 'Close', 'High', 'Low', 'Vol'])
    # bfx2.candles('EOS', TimeFrame='1h', Section='hist', start='', end='', limit=1000)
    df_temp.insert(0, 'symbol', symbol)
    df = df.append(df_temp, sort=True)
    if df.empty:
        print(r'[%s]%s数据下载失败' % (dt.fmt_now(), symbol))
        df = pd.DataFrame()
        return df
    else:
        df = df[df['timestamp'] < end]
        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Close'] = df['Close'].astype(float)
        df['Vol'] = df['Vol'].astype(float)
        df['date'] = df['timestamp'].map(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x / 1000)))
        df = df.sort_values(by='timestamp', ascending=True, inplace=False)
        df = df.reset_index(drop=True)
        return df


def bfx_sopt_data(db_conf, exchange, symbol='EOS/USDT', timeframe='1m', sleeptimes=10):
    engine_str = 'mysql+mysqlconnector://' + db_conf.user + ':' + db_conf.passwd + '@' + db_conf.host + ':' + db_conf.port + '/' + db_conf.db
    engine = create_engine(engine_str)
    db_client = mysql_pool.MYSQL(host=db_conf.host, port=db_conf.port, database=db_conf.db, user=db_conf.user,
                                 password=db_conf.passwd)

    cursor = db_client.get_cursor()
    table_name = exchange + '_spot_' + symbol.split('/')[0].lower() + '_' + symbol.split('/')[
        1].lower() + '_' + timeframe
    frequency_type = timeframe[-1]
    frequency_times = timeframe[:-1]
    if frequency_type == 'm':
        frequency = 60 * int(frequency_times)
    elif frequency_type == 'h':
        frequency = 60 * 60 * int(frequency_times)
    elif frequency_type == 'D':
        frequency = 24 * 60 * 60 * int(frequency_times)

    try:
        cursor.execute('select max(`timestamp`) from ' + table_name)
        print(r'[%s]%s表已经存在' % (dt.fmt_now(), table_name))
    except mysql.connector.Error as err:
        if err.errno == 1146:
            print(r'[%s]%s表不存在，正在创建表结构:' % (dt.fmt_now(), table_name))
            ddl = 'CREATE TABLE ' + table_name + kline_1m_table_temple2
            create_table(cursor, table_name, ddl)
            max_recount = None
        else:
            print(err.msg)
            print(err.errno)
    else:
        max_recount = cursor.fetchall()[0][0]
    if max_recount != None:
        since_stamp = int(max_recount)
    else:
        since_stamp = 1498838400000  # 2017-07-01 00:00:00
        print(r'[%s]%s为空表，正尝试从2017-07-01获取数据！' % (dt.fmt_now(), table_name))
    # now_stamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
    now_data_stamp = int(datetime.datetime.timestamp(dt.get_current_datatime(frequency))) * 1000
    since = since_stamp + 60 * 1000
    while since - now_data_stamp < 0:
        df = get_kline_data(symbol=symbol, timeframe=timeframe, since=since, end=now_data_stamp)
        if not df.empty:
            df.to_sql(table_name, engine, if_exists='append', index=False)
            if df['timestamp'].max() == since:
                since = since + frequency * 1000 * 900
            else:
                since = df['timestamp'].max() + frequency * 1000
            print(r'[%s]%s表更新%s条记录' % (dt.fmt_now(), table_name, df.shape[0]))
        else:
            print(r'[%s]%s表本周期没有数据' % (dt.fmt_now(), table_name))
            # since = since + frequency * 1000 * 900
            since = now_data_stamp
        time.sleep(sleeptimes)
    print(r'[%s]%s表更新完成' % (dt.fmt_now(), table_name))
    # 去重数据
    sql_str1 = 'delete from ' + table_name + \
               ' where `timestamp` in ' \
               '(select `timestamp` from ' \
               '(select `timestamp` from ' \
               + table_name + \
               ' group by `timestamp` HAVING count(`timestamp`)>1) as t2)' \
               ' and `index` not in ' \
               '(select `index` from ' \
               '(select MAX(`index`) as `index` from ' \
               + table_name + \
               ' group by `timestamp` HAVING count(`timestamp`)>1) as t3)'
    engine.execute(sql_str1)
    time.sleep(10)


class db_conf():
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.db = database
        self.user = user
        self.passwd = password



# save_all_data()

#
# def my_listener(event):
#     if event.exception:
#         logging.error("任务出错了！")
#
#
# if __name__ == '__main__':
#
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s -- %(levelname)s %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S',
#                         filename='get_kline_exchange.log',
#                         filemode='a')
#
#     # get_data()
#     # exit()
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(get_data, 'interval', minutes=120,
#                       # args=(symbols, spot_id, spot_api),
#                       id='bitfinex_spot', max_instances=5)
#     scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
#     scheduler._logger = logging
#     scheduler.start()
#
#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             # time.sleep(15 * 60)  # 其他任务是独立的线程执行
#             time.sleep(5 * 60)  # 其他任务是独立的线程执行
#             print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end='')
#             print('    sleep......')
#             # logging.info('   sleep......')
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()
#         print('Exit The Job!')
#         logging.info('Exit The Job!')
