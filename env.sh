#!/bin/sh
# Adds the environments variables from file ./config/.env

for line in `sed '/^$/d' "./config/.env"`; do
    `export $line`
done
