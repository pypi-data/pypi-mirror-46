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

import threading
import pandas as pd
import six

class Parameters(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class ParameterSource(object):
    """
    Source for backtesting parameters. This class is thread safe.
    """

    def __init__(self, params):
        self.__iter = iter(params)
        self.__lock = threading.Lock()

    def getNext(self, count):
        """
        Returns the next parameters to use in a backtest.
        If there are no more parameters to try then an empty list is returned.

        :param count: The max number of parameters to return.
        :type count: int
        :rtype: list of Parameters.
        """

        assert count > 0, "Invalid number of parameters"

        ret = []
        with self.__lock:
            if self.__iter is not None:
                try:
                    while count > 0:
                        params = six.next(self.__iter)
                        # Backward compatibility when parameters don't yield Parameters.
                        if not isinstance(params, Parameters):
                            params = Parameters(*params)
                        ret.append(params)
                        count -= 1
                except StopIteration:
                    self.__iter = None
        return ret

    def eof(self):
        with self.__lock:
            return self.__iter is None


# class ResultSinc(object):
#     """
#     Sinc for backtest results. This class is thread safe.
#     """
#     def __init__(self):
#         self.__lock = threading.Lock()
#         self.__bestResult = None
#         self.__bestParameters = None
#
#     def push(self, result, parameters):
#         """
#         Push strategy results obtained by running the strategy with the given parameters.
#
#         :param result: The result obtained by running the strategy with the given parameters.
#         :type result: float
#         :param parameters: The parameters that yield the given result.
#         :type parameters: Parameters
#         """
#         with self.__lock:
#             if result is not None and (self.__bestResult is None or result > self.__bestResult):
#                 self.__bestResult = result
#                 self.__bestParameters = parameters
#
#     def getBest(self):
#         with self.__lock:
#             ret = self.__bestResult, self.__bestParameters
#         return ret


class ResultSinc(object):
    """
    Sinc for backtest results. This class is thread safe.
    """

    def __init__(self):
        self.__lock = threading.Lock()
        self.__ResultDF = pd.DataFrame()
        self.__Result = None
        self.__Parameters = None

    def push(self, result):
        """
        Push strategy results obtained by running the strategy with the given parameters.

        :param result: The result obtained by running the strategy with the given parameters.
        :type result: float
        :param parameters: The parameters that yield the given result.
        :type parameters: Parameters
        """
        with self.__lock:
            if len(result):
                df_tmp = pd.DataFrame(result)
                self.__ResultDF = self.__ResultDF.append(df_tmp)
                self.__ResultDF.reset_index(inplace=True, drop=True)

    def getBest(self, num=5):
        with self.__lock:
            self.__ResultDF.sort_values(by='Result', ascending=False, inplace=True)
            self.__ResultDF.reset_index(inplace=True, drop=True)
            ret = self.__ResultDF[['symbol', 'Result', 'SharpeRatio', 'TotalCount']]
        return ret.head(num)

    def getReslut(self):
        with self.__lock:
            ret = self.__ResultDF.copy()
            ret.sort_values(by='Result', ascending=False, inplace=True)
            ret.reset_index(inplace=True, drop=True)
            col_list = ['symbol', 'Result', 'ResultRatio', 'SharpeRatio', 'TotalCount', 'ProfitableCount',
                        'ProfitableRatio',
                        'UnprofitableCount', 'UnprofitableRatio', 'MaxDrawDown', 'MaxDrawDownDuration','params']
            k = 0
            for col in ret.columns:
                if 'param_' in col:
                    col_list.append('param_' + str(k))
                    k += 1
            ret = ret[col_list]
        return ret

    def getOrdersinfo(self):
        with self.__lock:
            df = self.__ResultDF.copy()
            ret = pd.DataFrame()
            for i in range(df.shape[0]):
                list_tmp = df.loc[i, 'orders_list']
                df_tmp = pd.DataFrame(list_tmp)
                df_tmp['symbol'] = df.at[i, 'symbol']
                df_tmp['params'] = str(df.at[i, 'params'])
                ret = ret.append(df_tmp)
            col_list = ['symbol','params','Exec_time','Action','Exec_price','Quantity','Commission']
            ret = ret[col_list]
            ret.reset_index(inplace=True, drop=True)
            # ret.sort_values(by='Result', ascending=False, inplace=True)
            # ret.reset_index(inplace=True, drop=True)
            # col_list = ['symbol', 'Result', 'ResultRatio', 'SharpeRatio', 'TotalCount', 'ProfitableCount', 'ProfitableRatio',
            #      'UnprofitableCount', 'UnprofitableRatio', 'MaxDrawDown', 'MaxDrawDownDuration']
            # k = 0
            # for col in ret.columns:
            #     if 'param_' in col:
            #         col_list.append('param_'+str(k))
            #         k +=1
            # ret = ret[col_list]
        return ret
