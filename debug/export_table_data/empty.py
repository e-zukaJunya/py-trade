from debug.common.lambda_context import LambdaContext
from export_table_data.export_table_data import handler

# パラメータの生成
event = {}
context = LambdaContext("debug")

# 実行
output = handler(event, context)

print(output)
