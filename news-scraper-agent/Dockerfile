FROM public.ecr.aws/lambda/python:3.12

# Copy all files to container
COPY . ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

# Replace profile in .env and install poetry
RUN python3.12 -m pip install --root-user-action=ignore --debug -r requirements.txt

CMD [ "main.lambda_handler" ]
