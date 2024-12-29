FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3

# poetry install
RUN python3.12 -m pip install "poetry==$POETRY_VERSION"
#RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION="$POETRY_VERSION" python3 -

# Copy all files to container
COPY . ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

# Replace profile in .env and install poetry
RUN poetry --version \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction

CMD [ "main.lambda_handler" ]
