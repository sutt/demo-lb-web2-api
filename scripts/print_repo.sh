#!/bin/bash

# tree -I "*.pyc|__init__*|__pycache__" src/

# Define the directory to search in
directory="../src/"

# Find all files in the directory excluding *.pyc, __init__*, and __pycache__ files
files=$(find "$directory" -type f ! -name "*.pyc" ! -path "*/__init__*" ! -path "*/__pycache__/*" ! -path "*.env*")

# Loop through each file
for file in $files; do
    # Print the filename with relative path
    echo "File: $file"
    echo "======================="
    # Print the contents of the file
    cat "$file"
    echo "-----------------------"
done