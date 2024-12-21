from typing import Any, List

import oracledb


class DBService:
    """Oracle DB操作クラス"""

    def __init__(
        self, host: str, port: int, username: str, password: str, service_name: str
    ) -> None:
        """コンストラクタ

        Parameters
        ----------
        host : str
            ホスト名
        port : int
            ポート番号
        username : str
            ユーザ名
        password : str
            パスワード
        service_name : str
            サービス名
        """
        # インスタンス変数の初期化
        dsn = oracledb.makedsn(host, port, service_name=service_name)
        self.connection = oracledb.connect(user=username, password=password, dsn=dsn)
        self.cursor = self.connection.cursor()

    def fetch_one(self, query: str, params: List[Any] = []) -> Any:
        """単一行のデータを取得

        Parameters
        ----------
        query : str
            SQLクエリ
        params : List[Any], optional
            クエリパラメータ, by default []

        Returns
        -------
        Any
            クエリ結果の単一行
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params: List[Any] = []) -> List[Any]:
        """複数行のデータを取得

        Parameters
        ----------
        query : str
            SQLクエリ
        params : List[Any], optional
            クエリパラメータ, by default []

        Returns
        -------
        List[Any]
            クエリ結果の複数行
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self) -> None:
        """データベース接続を閉じる"""
        self.cursor.close()
        self.connection.close()
