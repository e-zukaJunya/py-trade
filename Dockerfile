# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.12-slim

RUN ls

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ryeをインストール
# RUN curl -sSf https://rye.astral.sh/get | bash

# # 環境変数を設定
# ENV PATH="/root/.rye/bin:$PATH"

# 作業ディレクトリを設定
WORKDIR /app

# プロジェクトの依存関係をインストール
# COPY pyproject.toml poetry.lock ./
# RUN rye sync
