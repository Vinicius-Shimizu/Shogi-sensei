FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    clang \
    lld \
    python3

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

FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY eval ./eval
COPY --from=builder /build/yaneuraou /app/yaneuraou
RUN chmod +x /app/yaneuraou
COPY /src ./src
CMD ["uvicorn", "src.engine_service:app", "--host", "0.0.0.0", "--port", "8080"]