import traceback
from typing import Callable

from common.logger.custom_logger import CustomLogger


def common_decorator(logger: CustomLogger):
    """引数を受け取るためのラッパー

    Parameters
    ----------
    logger : CustomLogger
        ロガー
    """

    def _common_decorator(func: Callable):
        """共通処理

        Parameters
        ----------
        func : Callable
            これをデコレータとして利用している関数自体
        """

        def wrapper(*args, **kwargs):
            try:
                # メインの処理の実行
                return func(*args, **kwargs)
            except Exception as e:
                # 共通例外処理
                logger.common_error(e, traceback.format_exc())
                # フロー自体は例外が起きたら異常終了させたいため、ここでraise
                raise (e)
            finally:
                # 共通終了処理
                logger.end()

        return wrapper

    return _common_decorator
