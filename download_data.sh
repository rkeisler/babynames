#!/usr/bin/env bash
mkdir data
cd data
curl https://www.ssa.gov/oact/babynames/names.zip -o names.zip
unzip names.zip
rm names.zip
cd ../
