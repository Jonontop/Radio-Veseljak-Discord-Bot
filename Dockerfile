# Uporabimo stabilno in lahko Linux Python podobo
FROM python:3.11-slim

# Namestimo ffmpeg, ki je nujen za predvajanje zvoka
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Nastavimo delovno mapo v vsebovalniku
WORKDIR /app

# Najprej kopiramo requirements, da izkoristimo Docker predpomnilnik (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiramo preostalo kodo bota
COPY . .

# Zaženemo bota
CMD ["python", "main.py"]