#!/bin/bash

OPENFAAS_URL="http://130.127.133.102:31112/function/image-classifier"  # Your OpenFaaS function URL
IMAGE_FILE="download.jpg"  # Path to the image file

for i in {1..500}; do
  curl -X POST "$OPENFAAS_URL" -H "Content-Type: image/jpeg" --data-binary @"$IMAGE_FILE" &
done
wait