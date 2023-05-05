# use alpine to reduce image size
FROM python:alpine3.16 AS build

WORKDIR /app

# use a virtual environment
RUN python -m venv /usr/app/venv
ENV PATH="/app/venv/bin:$PATH"

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# for security concerns, use a non-root user
USER non-root

# use a new stage
FROM python:alpine3.16
WORKDIR /usr/app/venv
COPY --from=build /usr/app/venv ./venv

COPY .env .
COPY financial ./financial
EXPOSE 8000