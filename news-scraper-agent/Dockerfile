FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/var/task

# poetry install
RUN pip install "poetry==$POETRY_VERSION"

# Copy all files to container
COPY . /var/task/

WORKDIR /var/task

# Replace profile in .env and install poetry
RUN sed -i 's/PROFILE="local"/PROFILE="dev"/g' .env \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction

CMD [ "main.lambda_handler" ]
