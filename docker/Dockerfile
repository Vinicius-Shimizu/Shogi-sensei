FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# =============================
# 🔧 Dependências sistema
# =============================
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    clang \
    lld \
    && rm -rf /var/lib/apt/lists/*

# =============================
# 🧠 Build da engine
# =============================
RUN git clone https://github.com/yaneurao/YaneuraOu.git && \
    cd YaneuraOu/source && \
    sed -i 's/YANEURAOU_ENGINE_NNUE/YANEURAOU_ENGINE_NNUE_HALFKP_VM_256X2_32_32/' Makefile && \
    make -j4 build ARCH=x86-64-modern

# =============================
# 📦 Python deps
# =============================
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# =============================
# 📁 Código
# =============================
COPY src/ src/

# =============================
# 🚀 Execução
# =============================
CMD ["python", "src/test.py", "--model", "/app/src/yaneuraou"]