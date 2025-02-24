FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install ./spacy-models-en_core_web_sm-3.2.0.tar.gz
CMD ["python" , "app.py"]
