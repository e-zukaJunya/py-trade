# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.11-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

# ryeをインストール
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash

# 作業ディレクトリを設定
WORKDIR /app

# プロジェクトの依存関係をインストール
COPY pyproject.toml .python-version requirements* README.md ./
RUN rye sync
