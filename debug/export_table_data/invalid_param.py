from debug.common.lambda_context import LambdaContext
from export_table_data.export_table_data import handler

# パラメータの生成
event = {
    "table_name": "invalid_table_name",
    # "date_from": "2021-07-09",
    "date_from": "20210709",
    # "date_to": "2021-07-09",
    "date_to": "20210709",
}
context = LambdaContext("debug")

# 実行
output = handler(event, context)

print(output)
