#! /bin/bash

docker build --no-cache -f Dockerfile . 2>&1 | tee build.log
