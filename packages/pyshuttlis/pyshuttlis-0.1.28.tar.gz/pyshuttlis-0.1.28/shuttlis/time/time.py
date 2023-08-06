from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Generator

import pytz


def time_now() -> datetime:
    return pytz.utc.localize(datetime.utcnow())


def from_iso_format(d: str, tz=pytz.utc) -> datetime:
    return datetime.fromisoformat(d).astimezone(tz)


@dataclass(frozen=True)
class TimeDeltaWindow:
    lower: Optional[timedelta]
    upper: Optional[timedelta]

    @classmethod
    def from_minutes(cls, lower: int, upper: int):
        lower = timedelta(minutes=lower)
        upper = timedelta(minutes=upper)
        return cls(lower, upper)

    @classmethod
    def from_days(cls, lower: int, upper: int):
        lower = timedelta(days=lower)
        upper = timedelta(days=upper)
        return cls(lower, upper)


class TimeWindowError(Exception):
    pass


@dataclass(frozen=True)
class TimeWindow:
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

    def __contains__(self, item):
        res = True
        if self.from_date is not None:
            res = res and self.from_date <= item
        if self.to_date is not None:
            res = res and item <= self.to_date
        return res

    @classmethod
    def around(cls, dt: datetime, td_window: TimeDeltaWindow):
        fr, to = None, None

        if td_window.lower is not None:
            fr = dt - td_window.lower

        if td_window.upper is not None:
            to = dt + td_window.upper

        return cls(fr, to)

    @classmethod
    def around_now(cls, td: timedelta):
        td_window = TimeDeltaWindow(td, td)
        return cls.around(time_now(), td_window)

    def dates(self) -> Generator[datetime, None, None]:
        return self._generic_incrementer(timedelta(days=1))

    def _generic_incrementer(self, td: timedelta) -> Generator[datetime, None, None]:
        if not self.from_date:
            raise TimeWindowError("No from date")

        temp_date = self.from_date

        if self.to_date:
            while temp_date <= self.to_date:
                yield temp_date
                temp_date += td
        else:
            while True:
                yield temp_date
                temp_date += td
