FROM python:3.12-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache gcc g++ make openjdk17
RUN mkdir /work
COPY /work /work
WORKDIR /work
CMD [ "tail", "-f", "/dev/null" ]