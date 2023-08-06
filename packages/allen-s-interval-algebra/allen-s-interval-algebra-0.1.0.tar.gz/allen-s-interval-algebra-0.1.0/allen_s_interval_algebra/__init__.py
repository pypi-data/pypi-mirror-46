from pytz import utc
from datetime import datetime as DateTime


class Interval:
    '''Implements interval algebra as defined by Allen

       @see https://en.wikipedia.org/wiki/Allen%27s_interval_algebra
    '''

    @classmethod
    def from_datetimes(
            cls, start: DateTime, end: DateTime
    ) -> 'Interval':
        return cls(start.timestamp(), end.timestamp())

    def __init__(self, start: float, end: float) -> None:
        if start < end:
            self.__start = start
            self.__end = end
        else:
            self.__start = end
            self.__end = start

    def __str__(self) -> str:
        return f'<Interval {self.__start} {self.__end}>'

    @property
    def start_as_datetime(self) -> DateTime:
        return DateTime.fromtimestamp(self.__start, tz=utc)

    @property
    def end_as_datetime(self) -> DateTime:
        return DateTime.fromtimestamp(self.__end, tz=utc)

    def precedes(self, an_interval: 'Interval') -> bool:
        return self.__end < an_interval.__start

    def preceded_by(self, an_interval: 'Interval') -> bool:
        return an_interval.precedes(self)

    def meets(self, an_interval: 'Interval') -> bool:
        return self.__end == an_interval.__start

    def met_by(self, an_interval: 'Interval') -> bool:
        return an_interval.meets(self)

    def overlaps(self, an_interval: 'Interval') -> bool:
        return (
            self.__start < an_interval.__start and
            self.__end < an_interval.__end and
            self.__end > an_interval.__start
        )

    def overlaped_by(self, an_interval: 'Interval') -> bool:
        return an_interval.overlaps(self)

    def finishes(self, an_interval: 'Interval') -> bool:
        return (
            self.__end == an_interval.__end and
            self.__start > an_interval.__start
        )

    def finished_by(self, an_interval: 'Interval') -> bool:
        return an_interval.finishes(self)

    def during(self, an_interval: 'Interval') -> bool:
        return (
            an_interval.__start < self.__start and
            self.__end < an_interval.__end
        )

    def contains(self, an_interval: 'Interval') -> bool:
        return an_interval.during(self)

    def starts(self, an_interval: 'Interval') -> bool:
        return (
            self.__start == an_interval.__start and
            self.__end < an_interval.__end
        )

    def started_by(self, an_interval: 'Interval') -> bool:
        return an_interval.starts(self)

    def equals(self, an_interval: 'Interval') -> bool:
        return (
            an_interval.__start == self.__start and
            an_interval.__end == self.__end
        )
