ARG FUNCTION_DIR="/function"

FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

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

# Copy function code
COPY . ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

# Install the runtime interface client
RUN pip3 install  \
    --target ${FUNCTION_DIR} \
    awslambdaric
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/usr/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]
