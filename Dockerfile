FROM python:3.9

# If using layers, copy the layer ARN instead
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "updater.py" ]  # Replace with your entrypoint script
