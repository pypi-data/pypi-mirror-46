# !usr\bin\env python
# -*- coding:utf-8 -*-

"""
pass
"""

import time as _time
from warnings import filterwarnings as _filterwarnings
from os.path import split as _split
_filterwarnings('ignore')

# public variables
timelist_transform_unit_year = 0
timelist_transform_unit_month = 1
timelist_transform_unit_day = 2
timelist_transform_unit_hour = 3
timelist_transform_unit_minute = 4
timelist_transform_unit_second = 5


# functions
def AGTimeList():

    """
    :return: the TimeList object
    """

    time1 = list(_time.localtime())[:6]
    _ = str(_time.time())
    i = _.find('.')
    i = _[i + 1:i + 4]
    for index in range(3):
        time1.append(int(i[index]))
    time_list = TimeList(time1[0],
                         time1[1],
                         time1[2],
                         time1[3],
                         time1[4],
                         time1[5],
                         time1[6],
                         time1[7],
                         time1[8])
    return time_list


def Now():

    """
    :return: the time now
    """

    time1 = _time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime())
    return time1


# classes
class TimeList:

    """
    It's a list of time.
    """

    def __init__(self,
                 year=0,
                 month=0,
                 day=0,
                 hour=0,
                 minute=0,
                 second=0,
                 zero_point_one_second=0,
                 zero_point_zero_one_second=0,
                 zero_point_zero_zero_one_second=0):

        """
        :param year:
        :param month:
        :param day:
        :param hour:
        :param minute:
        :param second:
        :param zero_point_one_second:
        :param zero_point_zero_one_second:
        :param zero_point_zero_zero_one_second:
        """

        try:
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
            int(second)
            int(zero_point_one_second)
            int(zero_point_zero_one_second)
            int(zero_point_zero_zero_one_second)
        except ValueError:
            raise TimeListError

        if (year < 0
                or month > 12
                or month < 0
                or day > 30
                or day < 0
                or hour > 24
                or hour < 0
                or minute > 60
                or minute < 0
                or second > 60
                or second < 0
                or zero_point_one_second > 10
                or zero_point_zero_one_second > 10
                or zero_point_zero_zero_one_second > 10
                or zero_point_one_second < 0
                or zero_point_zero_one_second < 0
                or zero_point_zero_zero_one_second < 0):
            raise TimeListError("An invalid time.")
        self._list = [year, month, day, hour, minute, second,
                      zero_point_one_second, zero_point_zero_one_second, zero_point_zero_zero_one_second]

    def __add__(self, other):

        """
        :return: list(time and time)
        """

        try:
            time1 = []
            for i in range(9):
                t = self._list[i] + other._list[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def __iadd__(self, other):

        """
        :return: list(time and time)
        """

        try:
            time1 = []
            for i in range(9):
                t = self._list[i] + other._list[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def __len__(self):

        """
        :return: len(self.list)
        """

        return len(self._list)

    def __getitem__(self, item):

        """
        :param item: the index of self._list
        :return: self._list[item]
        """

        return self._list[item]

    def __str__(self):

        """
        :return: str(self.list)
        """

        return str(self._list)

    def __repr__(self):

        """
        :return: str(self.list)
        """

        return str(self._list)

    def TransformToFloatTime(self, unit):

        """
        Transform the TimeList object to the float of unit what you want.
        :param unit: The unit what you want to transform.
        :return: The result of transform.
        """

        try:
            int(unit)
        except ValueError:
            raise TimeListError('An Invalid unit.')

        if not -1 < unit < 6:
            raise TimeListError('An Invalid unit.')

        if unit == 5:
            second = self._list[5]
            second += self._list[4] * 60
            second += self._list[3] * 60 * 60
            second += self._list[2] * 60 * 60 * 24
            second += self._list[1] * 60 * 60 * 24 * 30
            second += self._list[0] * 60 * 60 * 24 * 30 * 12
            return second

        elif unit == 4:
            minute = self._list[4]
            minute += self._list[5] / 60
            minute += self._list[3] * 60
            minute += self._list[2] * 60 * 24
            minute += self._list[1] * 60 * 24 * 30
            minute += self._list[0] * 60 * 24 * 30 * 12
            return minute

        elif unit == 3:
            hour = self._list[3]
            hour += self._list[5] / 60 / 60
            hour += self._list[4] / 60
            hour += self._list[2] * 24
            hour += self._list[1] * 24 * 30
            hour += self._list[0] * 24 * 30 * 12
            return hour

        elif unit == 2:
            day = self._list[2]
            day += self._list[5] / 60 / 60 / 24
            day += self._list[4] / 60 / 24
            day += self._list[3] / 24
            day += self._list[1] * 30
            day += self._list[0] * 30 * 12
            return day

        elif unit == 1:
            month = self._list[1]
            month += self._list[5] / 60 / 60 / 24 / 30
            month += self._list[4] / 60 / 24 / 30
            month += self._list[3] / 24 / 30
            month += self._list[2] / 30
            month += self._list[0] * 12

        elif unit == 0:
            year = self._list[0]
            year += self._list[5] / 60 / 60 / 24 / 30 / 12
            year += self._list[4] / 60 / 24 / 30 / 12
            year += self._list[3] / 24 / 30 / 12
            year += self._list[2] / 30 / 12
            year += self._list[1] / 12
            return year

    def DifferenceBetweenNowTime(self):

        """
        :return: the difference between self._list and the time now
        """

        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]
        time2 = _time.localtime()
        time2 = list(time2)[:6]
        for index in range(3):
            time2.append(int(i[index]))
        a = str(self._list)
        a = a.replace('[', '')
        a = a.replace(']', '')
        a = a.replace(',', '')
        a = a.replace(' ', '')
        a = int(a)
        b = str(time2)
        b = b.replace('[', '')
        b = b.replace(']', '')
        b = b.replace(',', '')
        b = b.replace(' ', '')
        b = int(b)
        c = a > b
        time = []
        if c:
            for index in range(9):
                num = self._list[index] - time2[index]
                if True:
                    if num < 0:
                        num = int(self._list[index] + Timer.ratio[index] - time2[index])
                        self._list[index - 1] -= 1
                time.append(num)
        else:
            for index in range(9):
                num = time2[index] - self._list[index]
                if True:
                    if num < 0:
                        num = int(time2[index] + Timer.ratio[index] - self._list[index])
                        time[index - 1] -= 1
                time.append(num)

        return time


class Timer:

    """
    Define the Timer class.
    """

    is_start = False
    is_stop = True
    time = []
    ratio = [0, 12, 30, 24, 60, 60, 10, 10, 10]

    def __str__(self):

        """
        :return: self.time -> list
        self.time = [x, x, x, x, x, x]
        self.time[0] is years
        self.time[1] is months
        self.time[2] is days
        self.time[3] is hours
        self.time[4] is minutes
        self.time[5] is seconds
        self.time[6] is 0.1 seconds
        self.time[7] is 0.01 seconds
        self.time[8] is 0.001 seconds
        """

        return str(self.time)

    def __add__(self, other):

        """
        :return: TimeList Object
        """

        try:
            time1 = []
            for i in range(9):
                t = self.time[i] + other.time[i]
                time1.append(t)
            if time1[8] >= 10:
                r = time1[8] // 10
                time1[7] += r
                time1[8] %= 10
            if time1[7] >= 10:
                r = time1[7] // 10
                time1[6] += r
                time1[7] %= 10
            if time1[6] >= 10:
                r = time1[6] // 10
                time1[5] += r
                time1[6] %= 10
            if time1[5] >= 60:
                r = time1[5] // 60
                time1[4] += r
                time1[5] %= 60
            if time1[4] >= 60:
                r = time1[4] // 60
                time1[3] += r
                time1[4] %= 60
            if time1[3] >= 24:
                r = time1[3] // 24
                time1[2] += r
                time1[3] %= 24
            if time1[2] >= 30:
                r = time1[2] // 30
                time1[1] += r
                time1[2] %= 30
            if time1[1] >= 12:
                r = time1[1] // 12
                time1[0] += r
                time1[1] %= 12
            return time1
        except (AttributeError, IndexError):
            raise UnknownError

    def __repr__(self):

        """
        :return: self.time -> list
        self.time = [x, x, x, x, x, x]
        self.time[0] is years
        self.time[1] is months
        self.time[2] is days
        self.time[3] is hours
        self.time[4] is minutes
        self.time[5] is seconds
        self.time[6] is 0.1 seconds
        self.time[7] is 0.01 seconds
        self.time[8] is 0.001 seconds
        """

        return str(self.time)

    def Start(self):

        """
        Start the timer.
        """

        if not self.is_stop:
            raise StartTimerError("You've turned on the Timer!")
        self.time = []
        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]
        self.timer_start = _time.localtime()
        self.timer_start = list(self.timer_start)[:6]
        for index in range(3):
            self.timer_start.append(int(i[index]))
        self.is_start = True
        self.is_stop = False

    def Stop(self):

        """
        Stop the timer.
        """

        if self.is_stop:
            raise StopTimerError("You've stopped the Timer!")
        _ = str(_time.time())
        i = _.find('.')
        i = _[i + 1:i + 4]
        self.timer_stop = _time.localtime()
        self.timer_stop = list(self.timer_stop)[:6]
        for index in range(3):
            self.timer_stop.append(int(i[index]))
        self.is_stop = True
        self.is_start = False
        for index in range(9):
            num = self.timer_stop[index] - self.timer_start[index]
            if True:
                if num < 0:
                    num = int(self.timer_stop[index] + self.ratio[index] - self.timer_start[index])
                    self.time[index - 1] -= 1
            self.time.append(num)
        self.time = TimeList(self.time[0],
                             self.time[1],
                             self.time[2],
                             self.time[3],
                             self.time[4],
                             self.time[5],
                             self.time[6],
                             self.time[7],
                             self.time[8])

    def IsRunning(self):

        """
        :return: self.is_start -> bool
        """

        return self.is_start

    def GetTime(self):

        """
        :return: time -> TimeList Object
        """

        if not self.time:
            raise GetTimeError("You didn't turned on the timetools!")
        return self.time


class Error(Exception):

    """
    Base class for exceptions in this module.
    """

    def __init__(self, reason=""):

        """
        Define the property: self.reason.
        """

        self.reason = reason

    def __str__(self):

        """
        :return: self.reason
        """

        return self.reason

    def __repr__(self):

        """
        :return: self.reason
        """

        return self.reason


class StartTimerError(Error):

    pass


class StopTimerError(Error):

    pass


class GetTimeError(Error):

    pass


class UnknownError(Error):

    pass


class TimeListError(Error):

    pass

