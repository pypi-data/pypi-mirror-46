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

# import pyalgotrade.logger
# from pyalgotrade.optimizer import base
# from pyalgotrade.optimizer import xmlrpcserver
import patgroom.logger
from patgroom.optimizer import base
from patgroom.optimizer import xmlrpcserver
logger = patgroom.logger.getLogger(__name__)


class Results(object):
    """The results of the strategy executions."""
    def __init__(self, result):
        # self.__parameters = parameters
        self.__result = result

    # def getParameters(self):
    #     """Returns a sequence of parameter values."""
    #     return self.__parameters

    def getResult(self):
        """Returns the result for a given set of parameters."""
        return self.__result

def serve(barFeed, strategyParameters,nums, address, port,batchsize=5,excelfile='Result.csv',orders_info =''):
    """Executes a server that will provide bars and strategy parameters for workers to use.

    :param barFeed: The bar feed that each worker will use to backtest the strategy.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`.
    :param strategyParameters: The set of parameters to use for backtesting. An iterable object where **each element is a tuple that holds parameter values**.
    :param address: The address to listen for incoming worker connections.
    :type address: string.
    :param port: The port to listen for incoming worker connections.
    :type port: int.
    :rtype: A :class:`Results` instance with the best results found or None if no results were obtained.
    """

    paramSource = base.ParameterSource(strategyParameters)
    resultSinc = base.ResultSinc()
    s = xmlrpcserver.Server(paramSource,nums, resultSinc, barFeed, address, port,autoStop=True ,batchSize=batchsize)

    # s.setDefaultBatchSize(batchsize)
    logger.info("Starting server")
    s.serve()
    logger.info("Server finished")

    # ret = None
    # bestResult, bestParameters = resultSinc.getBest()
    # if bestResult is not None:
    #     logger.info("Best final result %s with parameters %s" % (bestResult, bestParameters.args))
    #     ret = Results(bestParameters.args, bestResult)
    # else:
    #     logger.error("No results. All jobs failed or no jobs were processed.")
    # return ret
    
    ret = None
    ret = resultSinc.getReslut()
    if ret.empty:
        print("No results. All jobs failed or no jobs were processed.")
    else:
        ret.to_csv(excelfile)
        print(resultSinc.getBest(5))
        if orders_info:
            orders = resultSinc.getOrdersinfo()
            orders.to_csv(orders_info)


    
    
    