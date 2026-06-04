FROM python:3.11-slim

WORKDIR /app

# install cpu-only torch first to avoid CUDA bindings
RUN pip install --no-cache-dir \
    torch==2.2.2+cpu \
    torchvision==0.17.2+cpu \
    --index-url https://download.pytorch.org/whl/cpu

COPY requirements-pipeline.txt .

RUN pip install --no-cache-dir -r requirements-pipeline.txt

COPY . .

RUN mkdir -p outputs data/events

CMD ["python", "-m", "pipeline.main_pipeline"]
