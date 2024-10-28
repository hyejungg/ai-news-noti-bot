ARG FUNCTION_DIR="/function"

FROM mcr.microsoft.com/playwright/python:v1.48.0-noble-arm64

RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# extract dependencies to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --group main

# Copy function code
COPY . ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}/requirements.txt

WORKDIR ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip3 install  \
    --target ${FUNCTION_DIR} \
    awslambdaric
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/usr/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]