# syntax=docker/dockerfile:1  
FROM python:3.12-slim  
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    python3-tk tk \
    libx11-6 libxrender1 libxext6 libxfixes3 libxi6 libxrandr2 libxinerama1 libgl1 \        
    fonts-dejavu-core tini \        
    && rm -rf /var/lib/apt/lists/*  
WORKDIR /app
RUN pip install --no-cache-dir customtkinter
COPY . .
VOLUME ["/app/data"]
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "main.py"]