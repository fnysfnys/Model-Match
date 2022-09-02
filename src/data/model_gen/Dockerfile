FROM python:3.8
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./src ./src
COPY ./model .
COPY ./api.py .
COPY ./config.json .
COPY ./model_data.json .
CMD python3 -m uvicorn --host 0.0.0.0 api:app
