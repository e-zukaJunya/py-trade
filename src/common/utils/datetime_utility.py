from datetime import datetime
from typing import List

from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo


class DatetimeUtility:
    """日付操作クラス"""

    tz = ZoneInfo("Asia/Tokyo")
    """このシステムにおけるタイムゾーン"""

    @classmethod
    def get_datetime_now(cls) -> datetime:
        """現在日時(JST)を返却する

        Returns
        -------
        datetime
            現在日時(JST)
        """
        return datetime.now(tz=cls.tz)

    @classmethod
    def get_continuous_days(
        cls, oldest_date: datetime, latest_date: datetime
    ) -> List[datetime]:
        """連続日付の生成

        Args:
            oldest_date (datetime): 最も古い日付
            latest_date (datetime): 最も新しい日付

        Returns:
            List[datetime]: 連続した日付のリスト
        """

        diff = latest_date - oldest_date
        l_date = [oldest_date + relativedelta(days=i) for i in range(diff.days)]
        l_date.append(latest_date)

        return l_date

    @classmethod
    def get_continuous_months(
        cls, oldest_date: datetime, latest_date: datetime
    ) -> List[datetime]:
        """連続した月の日付の生成

        Args:
            oldest_date (datetime): 最も古い日付
            latest_date (datetime): 最も新しい日付

        Returns:
            List[datetime]: 連続した月の日付のリスト
        """
        # 日数の差分から連続日付を生成
        diff = latest_date - oldest_date
        l_date = [oldest_date + relativedelta(days=i) for i in range(diff.days)]
        l_date.append(latest_date)

        # すべて1日にし、一意化(順番がバラバラになるのでソート)
        l_year_month = [datetime(item.year, item.month, 1) for item in l_date]
        l_unique_year_month = sorted(list(set(l_year_month)))

        return l_unique_year_month

    @classmethod
    def check_date(cls, date_str: str, format: str = "%Y%m%d") -> bool:
        """日付形式チェック

        Args:
            date_str (str): 日付文字列
            format (str, optional): 日付の書式。 Defaults to '%Y%m%d'。

        Returns:
            bool: 日付として変換できるかどうか
        """
        try:
            # 日付型に変換
            datetime.strptime(date_str, format)
            # 日付型に変換できた場合、Trueを返却
            return True

        except ValueError:
            # 日付型に変換できない場合、Falseを返却
            return False
