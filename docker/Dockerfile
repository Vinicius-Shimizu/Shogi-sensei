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
    make -j4 normal \
        YANEURAOU_EDITION=YANEURAOU_ENGINE_NNUE_HALFKPE9 \
        TARGET_CPU=AVX2 \
        COMPILER=clang++ \
        PYTHON=python3

# copy binary
RUN cp YaneuraOu-by-gcc /build/yaneuraou

FROM debian:bookworm-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir model
COPY model/ model/
COPY --from=builder /build/yaneuraou /app/model/yaneuraou
RUN chmod +x /app/model/yaneuraou

COPY requirements.txt .
RUN python3 -m pip install --break-system-packages --upgrade pip && \
    python3 -m pip install --break-system-packages -r requirements.txt


COPY src/ src/


CMD ["python3", "src/exercise_generator.py"]