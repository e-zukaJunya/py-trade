import os
import re
import json
import string
from typing import Any, Callable, Dict, Optional

import requests

from common.models.environments import Environments


class CommonUtility:
    @classmethod
    def get_envs(cls, obj: Optional[Dict[str, str]] = None) -> Environments:
        """環境変数をdataclassとして固めて取得

        Returns:
            Environments: 環境変数オブジェクト
        """
        # 辞書の指定があればその辞書から(Glueのargumentsの場合など)
        # 無ければ環境変数から取得
        tmp_envs = os.environ if obj is None else obj

        envs = Environments(
            LOG_LEVEL=tmp_envs["LOG_LEVEL"],
            SYS_CODE=tmp_envs["SYS_CODE"],
            ENV=tmp_envs["ENV"],
            DB_SECRET_ID=tmp_envs["DB_SECRET_ID"],
            OUTPUT_BUCKET=tmp_envs["OUTPUT_BUCKET"],
            DB_HOST=tmp_envs["DB_HOST"],
            DB_PORT=tmp_envs["DB_PORT"],
            DB_SERVICE_NAME=tmp_envs["DB_SERVICE_NAME"],
        )
        return envs

    @classmethod
    def get_db_credentials(cls, runtime_env: str, secret_id: str) -> Dict[str, str]:
        """Secrets ManagerからDBの認証情報を取得

        Args:
            secret_id (str): Secrets ManagerのSecretId

        Returns:
            Dict[str, str]: DBの認証情報
        """
        if runtime_env == "local":
            # localの場合、環境変数から取得
            return {
                "DB_USER": os.environ["DB_USER"],
                "DB_PASSWORD": os.environ["DB_PASSWORD"],
            }
        else:
            # local以外の場合、Secrets Managerから取得
            secret_url = (
                f"http://localhost:2773/secretsmanager/get?secretId={secret_id}"
            )
            response = requests.get(
                secret_url,
                headers={
                    "X-Aws-Parameters-Secrets-Token": os.environ.get(
                        "AWS_SESSION_TOKEN"
                    )
                },
            )
            if response.status_code == 200:
                res_json = response.json()
                secret_data = json.loads(res_json["SecretString"])
                return {
                    "DB_USER": secret_data["DB_USER"],
                    "DB_PASSWORD": secret_data["DB_PASSWORD"],
                }
            else:
                raise Exception(f"Failed to retrieve secret: {response.text}")

    @classmethod
    def pascal_to_snake(cls, s: str) -> str:
        """パスカルケースをスネークケースに変換

        Parameters
        ----------
        s : str
            パスカルケース文字列

        Returns
        -------
        str
            スネークケース文字列
        """
        return re.sub("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", s).lower()

    @classmethod
    def snake_to_pascal(cls, s: str) -> str:
        """スネークケースをパスカルケースに変換

        Parameters
        ----------
        s : str
            スネークケース文字列

        Returns
        -------
        str
            パスカルケース文字列
        """
        return string.capwords(s.replace("_", " ")).replace(" ", "")

    @classmethod
    def convert_dict_key(cls, d: Dict, conv: Callable[[str], str]) -> Dict:
        """辞書のキーのケースを変換

        Parameters
        ----------
        d : Dict
            変換対象の辞書
        conv : Callable[[str], str]
            ケースを変換するメソッド

        Returns
        -------
        dict
            変換後の辞書
        """

        def convert_value(cls, v: Any) -> Any:
            """辞書の値がlistやdictだった場合、中のキーを変換する処理

            Parameters
            ----------
            v : Any
                辞書のvalue

            Returns
            -------
            Any
                変換後のvalue
            """
            return (
                cls.convert_dict_key(v, conv)
                if isinstance(v, dict)
                else [convert_value(e) for e in v]
                if isinstance(v, list)
                else v
            )

        return {conv(k): convert_value(v) for k, v in d.items()}

    @classmethod
    def chunk_list(cls, lst: list, chunk_size: int) -> list:
        """リストを引数の件数でチャンク処理を行う

        Parameters
        ----------
        lst : list
            リスト
        chunk_size : int
            チャンク件数

        Returns
        -------
        list
            チャンク処理したリスト
        """
        return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

    @classmethod
    def get_values_from_const_class(cls, c: type) -> list:
        """クラスのメンバの値のみリストとして取得
        固定値を定義したクラスから値を一覧するときに使用する想定

        Args:
            c (type): classそのもの

        Returns:
            list: 固定値の値リスト
        """
        return [value for name, value in vars(c).items() if not name.startswith("__")]
