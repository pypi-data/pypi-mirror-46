# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
# import xmlrpc.client
# import pickle
import time
import socket
import random
import multiprocessing
import collections
from patgroom import broker

from six.moves import xmlrpc_client

import patgroom.logger
from patgroom import barfeed
from patgroom.optimizer import serialization
from patgroom.stratanalyzer import returns, sharpe, drawdown, trades


def call_function(function, *args, **kwargs):
    return function(*args, **kwargs)


def call_and_retry_on_network_error(function, retryCount, *args, **kwargs):
    ret = None
    while retryCount > 0:
        retryCount -= 1
        try:
            ret = call_function(function, *args, **kwargs)
            return ret
        except socket.error:
            time.sleep(random.randint(1, 3))
    ret = call_function(function, *args, **kwargs)
    return ret


class Worker(object):
    def __init__(self, address, port, workerName=None):
        url = "http://%s:%s/PyAlgoTradeRPC" % (address, port)
        self.__server = xmlrpc_client.ServerProxy(url, allow_none=True)
        self.__logger = patgroom.logger.getLogger(workerName)
        if workerName is None:
            self.__workerName = socket.gethostname()
        else:
            self.__workerName = workerName

    def getLogger(self):
        return self.__logger

    def getInstrumentsAndBars(self):
        ret = call_and_retry_on_network_error(self.__server.getInstrumentsAndBars, 10)
        # print(ret)
        # ret = pickle.loads(ret.data)
        ret = serialization.loads(ret)
        return ret

    def getBarsFrequency(self):
        ret = call_and_retry_on_network_error(self.__server.getBarsFrequency, 10)
        ret = int(ret)
        return ret

    def getNextJob(self):
        ret = call_and_retry_on_network_error(self.__server.getNextJob, 10)
        # ret = pickle.loads(ret.data)
        ret = serialization.loads(ret)
        return ret

    def pushJobResults(self, jobId, result):
        # jobId = pickle.dumps(jobId)
        # result = pickle.dumps(result)
        # parameters = pickle.dumps(parameters)
        # workerName = pickle.dumps(self.__workerName)
        jobId = serialization.dumps(jobId)
        result = serialization.dumps(result)
        # parameters = serialization.dumps(parameters)
        workerName = serialization.dumps(self.__workerName)
        call_and_retry_on_network_error(self.__server.pushJobResults, 10, jobId, result, workerName)

    def __processJob(self, job, barsFreq, instruments, bars):
        bestResult = None
        parameters = job.getNextParameters()  # 获取一个参数集合
        bestParams = parameters
        retlist = []
        # print(parameters)
        if parameters is None:
            print('参数为空！')
        while parameters is not None:
            # Wrap the bars into a feed.
            feed = barfeed.OptimizerBarFeed(barsFreq, instruments, bars)
            # Run the strategy.
            self.getLogger().info("Running strategy with parameters %s" % (str(parameters)))
            result = None
            try:
                result = self.runStrategy(feed, *parameters)
                # self.pushJobResults(job.getId(), result, parameters)
            except Exception as e:
                self.getLogger().exception("Error running strategy with parameters %s: %s" % (str(parameters), e))
            self.getLogger().info("Finished by parameters %s" % (str(parameters)))
            # self.getLogger().info("Result %s" % result)
            # if bestResult is None or result > bestResult:
            #     bestResult = result
            #     bestParams = parameters
            # Run with the next set of parameters.
            if result:
                result['symbol'] = parameters[0]
                result['params'] = parameters
                for i in range(len(parameters) - 1):
                    result['param_' + str(i)] = parameters[i + 1]
                retlist.append(result)
            parameters = job.getNextParameters()

        # assert (len(retlist) > 0)
        if len(retlist) > 0:
            self.pushJobResults(job.getId(), retlist)
        # self.pushJobResults(job.getId(), bestResult, bestParams)

    # Run the strategy and return the result.
    def runStrategy(self, feed, parameters):
        raise Exception("Not implemented")

    def run(self):
        try:
            self.getLogger().info("Started running")
            # Get the instruments and bars.
            instruments, bars = self.getInstrumentsAndBars()
            barsFreq = self.getBarsFrequency()

            # Process jobs
            job = self.getNextJob()
            time.sleep(2)
            while job is not None:
                self.__processJob(job, barsFreq, instruments, bars)
                job = self.getNextJob()
            self.getLogger().info("Finished running")
        except Exception as e:
            self.getLogger().exception("Finished running with errors: %s" % (e))

'''
2018-10-4 输出订单执行详细信息
'''
class orderResult(object):
    def __init__(self, strat):
        self.__dateTimes = set()
        self.__barSubplots = {}
        self.__orders = collections.OrderedDict()
        self.__logger = patgroom.logger.getLogger('OrderDetail')
        strat.getBroker().getOrderUpdatedEvent().subscribe(self.onOrderEvent)

    def getLogger(self):
        return self.__logger

    def onOrderEvent(self, broker_, orderEvent):
        order = orderEvent.getOrder()
        execInfo1 = order.getExecutionInfo()

        if orderEvent.getEventType() in (
                broker.OrderEvent.Type.PARTIALLY_FILLED,
                broker.OrderEvent.Type.FILLED):
            action = order.getAction()
            execInfo = orderEvent.getEventInfo()
            order_list = {}
            if action in [broker.Order.Action.BUY, broker.Order.Action.BUY_TO_COVER]:
                # self.getLogger().info('订单信息-买入:%s - %s - %s - %s' % (execInfo.getDateTime(), str(execInfo.getPrice()),
                #                                      str(execInfo.getQuantity()), str(execInfo.getCommission())))

                order_list['Exec_time']=execInfo.getDateTime()
                order_list['Action'] = 'BUY'
                order_list['Quantity'] = execInfo.getQuantity()
                order_list['Exec_price'] = execInfo.getPrice()
                order_list['Commission'] = execInfo.getCommission()
                orders_list.append(order_list)

            elif action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
                # self.getLogger().info('订单信息-卖出:%s - %s - %s - %s' % (execInfo.getDateTime(), str(execInfo.getPrice()),
                #                                      str(execInfo.getQuantity()), str(execInfo.getCommission())))
                order_list['Exec_time']=execInfo.getDateTime()
                order_list['Action'] = 'Sell'
                order_list['Quantity'] = execInfo.getQuantity()
                order_list['Exec_price'] = execInfo.getPrice()
                order_list['Commission'] = execInfo.getCommission()
                orders_list.append(order_list)


def worker_process(strategyClass, address, port, workerName):
    class MyWorker(Worker):
        def runStrategy(self, barFeed, *args, **kwargs):
            global orders_list
            orders_list = list()
            strat = strategyClass(barFeed, *args, **kwargs)
            '''
            start by groom
            '''
            retAnalyzer = returns.Returns()
            strat.attachAnalyzer(retAnalyzer)
            sharpeRatioAnalyzer = sharpe.SharpeRatio()
            strat.attachAnalyzer(sharpeRatioAnalyzer)
            drawDownAnalyzer = drawdown.DrawDown()
            strat.attachAnalyzer(drawDownAnalyzer)
            tradesAnalyzer = trades.Trades()
            strat.attachAnalyzer(tradesAnalyzer)

            orderResult(strat)
            '''
            end by groom
            '''
            strat.run()

            if tradesAnalyzer.getProfitableCount() > 0:
                profits = tradesAnalyzer.getProfits()
                ProfitableRatio = round(profits.mean(), 2)
                ProfitableStd = round(profits.std(), 2)
            else:
                ProfitableRatio = 0
                ProfitableStd = 0

            if tradesAnalyzer.getUnprofitableCount() > 0:
                losses = tradesAnalyzer.getLosses()
                UnprofitableRatio = round(losses.mean(), 2)
                UnprofitableStd = round(losses.std(), 2)
            else:
                UnprofitableRatio = 0
                UnprofitableStd = 0

            # return strat.getResult()
            return {
                'Result': round(strat.getResult(), 2),  # 最终资金
                'ResultRatio': round(retAnalyzer.getCumulativeReturns()[-1], 2),  # 回报率
                'SharpeRatio': round(sharpeRatioAnalyzer.getSharpeRatio(0.05), 2),  # 夏普比率
                'MaxDrawDown': round(drawDownAnalyzer.getMaxDrawDown() * 100, 2),  # 最大回测
                'MaxDrawDownDuration': drawDownAnalyzer.getLongestDrawDownDuration(),  # 最大回测时间
                'TotalCount': tradesAnalyzer.getCount(),  # 总交易笔数
                'ProfitableCount': tradesAnalyzer.getProfitableCount(),  # 正收益交易笔数
                'UnprofitableCount': tradesAnalyzer.getUnprofitableCount(),  # 负收益交易笔数
                'ProfitableRatio': ProfitableRatio,  # 平均收益
                'ProfitableStd': ProfitableStd,  # 平均收益方差
                'UnprofitableRatio': UnprofitableRatio,  # 平均损失
                'UnprofitableStd': UnprofitableStd,  # 平均损失方差
                'orders_list':orders_list   # 订单成交信息
            }

            # Create a worker and run it.

    w = MyWorker(address, port, workerName)
    w.run()


def run(strategyClass, address, port, workerCount=None, workerName=None):
    """Executes one or more worker processes that will run a strategy with the bars and parameters supplied by the server.

    :param strategyClass: The strategy class.
    :param address: The address of the server.
    :type address: string.
    :param port: The port where the server is listening for incoming connections.
    :type port: int.
    :param workerCount: The number of worker processes to run. If None then as many workers as CPUs are used.
    :type workerCount: int.
    :param workerName: A name for the worker. A name that identifies the worker. If None, the hostname is used.
    :type workerName: string.
    """

    assert (workerCount is None or workerCount > 0)
    if workerCount is None:
        workerCount = multiprocessing.cpu_count()

    workers = []
    # Build the worker processes.
    for i in range(workerCount):
        workers.append(multiprocessing.Process(target=worker_process, args=(strategyClass, address, port, workerName)))

    # Start workers
    for process in workers:
        process.start()

    # Wait workers
    for process in workers:
        process.join()
