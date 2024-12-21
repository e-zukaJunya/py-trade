from debug.common.lambda_context import LambdaContext
from export_table_data.export_table_data import handler

# パラメータの生成
event = {
    # "table_name": "glzanmst",
    # "table_name": "glswmtrn",
    "table_name": "glysnmst",
    # "table_name": "ackmkmst",
    "date_from": "2023-01-01",
    "date_to": "2023-02-03",
}
context = LambdaContext("debug")

# 実行
output = handler(event, context)

print(output)
