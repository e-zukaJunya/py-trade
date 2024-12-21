class LambdaContext:
    """テスト実行用のLambda Context"""

    def __init__(self, function_name: str):
        """コンストラクタ"""
        self.function_name = function_name
        self.aws_request_id = "aws_request_id"
