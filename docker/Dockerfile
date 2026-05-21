FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    clang \
    lld \
    python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

RUN git clone https://github.com/yaneurao/YaneuraOu.git

WORKDIR /build/YaneuraOu/source

RUN make clean && \
    make -j$(nproc) normal \
        YANEURAOU_EDITION=YANEURAOU_ENGINE_NNUE_HALFKPE9 \
        TARGET_CPU=NATIVE \
        COMPILER=clang++ \
        PYTHON=python3

RUN cp YaneuraOu-by-gcc /build/yaneuraou


FROM debian:bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    g++ \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/yaneuraou /app/yaneuraou

RUN chmod +x /app/yaneuraou

COPY requirements.txt .

RUN python3 -m pip install --break-system-packages --upgrade pip && \
    python3 -m pip install --break-system-packages -r requirements.txt

COPY alembic.ini .
COPY alembic/ alembic/
COPY start.sh .

COPY src/ src/

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]