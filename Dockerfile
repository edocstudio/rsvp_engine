FROM public.ecr.aws/lambda/python:3.13

ENV GSHEET_KEY=
ENV DYNAMODB_TABLE=
ENV SQS_URL=
ENV GCP_CRED_PATH=
ENV SALT=
ENV TIME_FORMAT=
ENV TIME_ZONE=

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .creds .creds
COPY common common
COPY config config

COPY main.py .

CMD [ "main.lambda_handler" ]