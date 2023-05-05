# use alpine to reduce image size
FROM python:alpine3.16 AS build

WORKDIR /app

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# use a new stage
FROM python:alpine3.16
WORKDIR /app
COPY --from=build /usr/local/ /usr/local/

COPY .env .
COPY financial ./financial
EXPOSE 5000
COPY --from=build /usr/local/ /usr/local/