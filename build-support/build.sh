#!/usr/bin/env bash

cd $(git rev-parse --show-toplevel)


bash -c "\
  cd apple-pie-api \
    && pipenv lock -r > requirements.txt \
"
./pants package apple-pie-api:pex_binary


bash -c "\
  cd randmoji-api \
    && pipenv lock -r > requirements.txt \
"
./pants package randmoji-api:pex_binary
