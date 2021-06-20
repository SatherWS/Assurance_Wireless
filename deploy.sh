#!/bin/bash

git add .
git commit -m "commit deployed to aws"
git push
eb deploy

# reset instance for whatever reason

