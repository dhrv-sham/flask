FROM python:3

WORKDIR /app

# Copy only requirements first to use Docker cache
COPY requirements.txt .

# Install dependencies in one step
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install spaCy separately to leverage caching
RUN pip install --no-cache-dir -U spacy && \
    python -m spacy download en_core_web_sm

# Copy the application files last
COPY . .

CMD ["python", "app.py"]
