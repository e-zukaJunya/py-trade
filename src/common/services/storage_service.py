from typing import List

import boto3
from botocore.client import Config

from common.constants.constants import LiteralValue
from common.utils.common_utility import CommonUtility


class StorageService:
    """S3操作クラス"""

    def __init__(self) -> None:
        """コンストラクタ"""
        self.client = boto3.client(
            "s3",
            config=Config(signature_version="s3v4"),
        )
        self.resource = boto3.resource("s3")

    def get_object(self, bucket: str, key: str) -> bytes:
        """S3からのファイル読み込み

        Parameters
        ----------
        bucket : str
            バケット名
        key : str
            オブジェクトキー

        Returns
        -------
        bytes
            読み込んだファイルのバイナリ
        """
        obj = self.client.get_object(Bucket=bucket, Key=key)
        return obj["Body"].read()

    def put_text_object(self, bucket: str, key: str, data_str: str) -> None:
        """ファイルアップロード（テキストデータ）

        Parameters
        ----------
        bucket : str
            バケット名
        key : str
            オブジェクトキー
        data_str : str
            テキストデータ
        """
        obj = self.resource.Object(bucket, key)
        obj.put(Body=data_str)

    def list_object_keys(self, bucket: str, prefix: str = "") -> List[str]:
        """S3のオブジェクトキーを一覧する

        Parameters
        ----------
        bucket : str
            バケット
        prefix : str, optional
            プレフィックス, by default ""

        Returns
        -------
        List[str]
            オブジェクトキー一覧
        """
        paginator = self.client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

        key_list: List[str] = []
        for page in page_iterator:
            # 1件もない場合はContentというKeyが無い
            if "Contents" in page:
                key_list += [
                    obj["Key"]
                    for obj in page["Contents"]
                    # ディレクトリを表すオブジェクトがあるので、それを除外
                    if obj["Key"].rfind("/") != len(obj["Key"]) - 1
                ]
        return key_list

    def delete_objects(self, bucket_name: str, keys: List[str]) -> None:
        """ファイル削除

        Args:
            bucket_name (str): バケット名
            keys (List[str]): 対象のオブジェクトキーリスト
        """
        # boto3のdelete_objectsのDelete.Objectsは配列を受けとるI/Fなのに空配列を入れるとエラーなので回避
        if len(keys) != 0:
            for chunk_keys in CommonUtility.chunk_list(
                keys, LiteralValue.UNITI_TO_DELETE_S3
            ):
                objects = [{"Key": key} for key in chunk_keys]
                self.resource.Bucket(bucket_name).delete_objects(
                    Delete={"Objects": objects},
                )

    def copy_object(
        self,
        source_bucket_name: str,
        source_obj_key: str,
        dest_bucket_name: str,
        dest_obj_key: str,
    ) -> None:
        """ファイルコピー

        Args:
            bucket_name (str): バケット名
            keys (List[str]): 対象のオブジェクトキーリスト
        """
        copy_source = {"Bucket": source_bucket_name, "Key": source_obj_key}
        self.resource.meta.client.copy(copy_source, dest_bucket_name, dest_obj_key)
