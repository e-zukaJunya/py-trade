from typing import Any, Dict

# メッセージ定義


class Msgs:
    """
    メッセージ本体
    """

    def START(process: str):
        return f"{process} 開始"

    def END(process: str):
        return f"{process} 終了"

    def ERROR(process: str):
        return f"{process} 失敗"

    def PARAM_IS(param: Dict[str, Any]):
        return f"起動パラメータ: {param}"

    def INVALID_DATE_FORMAT(date_format: str):
        return f"Invalid date format. Input should be '{date_format}'"

    def DATA_COUNT(length: str):
        return f"データ件数: {length}"


class Words:
    """
    単語
    """

    TANGO = "単語"
