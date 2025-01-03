FROM public.ecr.aws/lambda/python:3.12

# Upgrade pip to avoid compatibility issues
RUN python3.12 -m ensurepip && python3.12 -m pip install --upgrade pip

# Copy only requirements.txt first to leverage Docker caching
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

# Set the working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN python3.12 -m pip install -r requirements.txt

# Copy the rest of the application files
COPY . ${LAMBDA_TASK_ROOT}

CMD [ "main.lambda_handler" ]
