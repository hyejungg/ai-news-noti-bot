FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/var/task

# Copy all files to container
COPY . /var/task/

WORKDIR /var/task

RUN pip3 install -r requirements.txt

CMD [ "main.lambda_handler" ]
