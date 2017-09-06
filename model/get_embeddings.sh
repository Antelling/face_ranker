#!/usr/bin/env bash

sudo cp test_images/* /var/lib/docker/volumes/faces/_data/test

sudo docker run --mount source=faces,target=/app bamos/openface /bin/bash
sudo docker exec gracious_mclean python /app/get_embeddings.py /app/test

sudo cp /var/lib/docker/volumes/faces/_data/test.json test.json

sudo chown anthony test.json

python3 get_predictions.py