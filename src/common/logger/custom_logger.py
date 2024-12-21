import json
from logging import ERROR, INFO, Formatter, StreamHandler, getLogger

from common.constants.messages import Msgs
from common.utils.datetime_utility import DatetimeUtility


class CustomJsonFormatter(Formatter):
    """ログフォーマット用クラス"""

    def format(self, record):
        """ログ出力フォーマットの定義"""
        msg = record.__dict__.get("log_message")
        format_dict = {
            # ログレベル
            "Level": record.levelname,
            # ログ本文
            "Message": msg,
            # APIやバッチの名称（論理名でなく何かの物理名で取るのが良い）
            "ProcessName": record.__dict__.get("process_name"),
            # 実行要求を一意に識別するID
            "Uid": record.__dict__.get("uid"),
            # 本システムのログであることを示すコード
            "SysCode": record.__dict__.get("sys_code"),
            # 出力日時
            "Time": record.__dict__.get("time"),
            # 最終コミットハッシュ
            # CIパイプラインを組んでいないとこの値を流し込むのは難しいため無し(可能になったらすぐ復活できるようコメントアウト)
            # "LatestCommit": record.__dict__.get("latest_commit"),
        }

        # コンソールで人間が見やすい用とロボットが解析しやすい用の2種類出力
        return f"{json.dumps(format_dict, ensure_ascii=False)}"


class CustomLogger:
    """ロガー"""

    def __init__(self, log_level: str, sys_code: str):
        """コンストラクタ

        Parameters
        ----------
        log_level : str
            ログレベル
        """

        # loggerオブジェクトの宣言
        self.logger = getLogger()

        # 親Loggerオブジェクトにログ出力イベントを渡さないように設定(カスタムロガーで出力したログをrootロガーで再度出力しない)
        self.logger.propagate = False

        # loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
        self.logger.setLevel(log_level)

        # handlerの生成
        sh = StreamHandler()

        # handlerにログ出力フォーマットを設定
        formatter = CustomJsonFormatter()
        sh.setFormatter(formatter)

        # loggerにhandlerをセット
        self.logger.addHandler(sh)

        # ログ出力用固定値
        self.sys_code = sys_code
        self.process_name = None
        self.uid = None
        # self.latest_commit = os.environ["LATEST_COMMIT"]

    def set_default_value(self, process_name: str, uid: str):
        """ログ出力用固定値のセット

        Parameters
        ----------
        process_name : str
            処理名
        uid : str
            実行時に一意なID
        """

        self.process_name = process_name
        self.uid = uid

    def output_log(self, log_level: int, msg: str):
        """ログ出力

        Parameters
        ----------
        log_level : int
            ログレベル
        msg : str
            ログメッセージ
        """
        log_content = {
            "sys_code": self.sys_code,
            "process_name": self.process_name,
            "uid": self.uid,
            "log_message": msg,
            "time": str(DatetimeUtility.get_datetime_now()),
            # "latest_commit": self.latest_commit,
        }

        self.logger.log(log_level, msg)
        self.logger.log(log_level, "", extra=log_content)

    def start(self):
        """開始ログ"""
        self.output_log(INFO, Msgs.START(self.process_name))

    def end(self):
        """終了ログ"""
        self.output_log(INFO, Msgs.END(self.process_name))

    def common_error(self, error_message: str, stack_trace: str):
        """共通エラーログ

        Parameters
        ----------
        error_message : str
            ログ本文
        stack_trace : str
            スタックトレース
        """
        # ステップが失敗した旨を出力
        self.output_log(ERROR, Msgs.ERROR(self.process_name))
        # エラーメッセージとスタックトレースを出力
        self.output_log(ERROR, f"{error_message}\n{stack_trace}")
