import os

import polars as pl

aaa = "a"
print(aaa)


def main():
    df = pl.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
        }
    )
    print(df)
