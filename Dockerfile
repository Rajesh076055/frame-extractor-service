FROM python:slim

WORKDIR /app

COPY requirements.txt ./

RUN apt update && \
    apt install -y libopencv-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip  && pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "frame_extract.py"]
