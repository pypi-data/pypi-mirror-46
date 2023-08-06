# time handler for equation cipher

import datetime
import time


class TimeConverter(object):
    """
    Class to convert the date object in the required form.
    """
    FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

    def datetime_to_epoch(self, date_obj: datetime) -> float:
        """
        Converts the datetime object into epoch time.
        i.e. milliseconds elapsed from the 1-1-1970.
        :param date_obj: <date type: datetime>
        :return: <data type: float>
        """
        return date_obj.timestamp()

    def epoch_to_datetime(self, epoch: float) -> datetime:
        """
        Convert epoch time to datetime object.
        :param epoch: <data type: float>
        :return: <data type: datetime>
        """
        local_time_string = time.strftime(self.FORMAT,
                                          time.localtime(epoch))

        return datetime.datetime.strptime(local_time_string,
                                          self.FORMAT)
