#!/bin/sh

# Check if the source file path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_java_file>"
    exit 1
fi

# Extract file path and name
JAVA_FILE="$1"
FILE_NAME=$(basename -- "$JAVA_FILE")
CLASS_NAME="${FILE_NAME%.*}"

# Compile the Java file
echo "Compiling $JAVA_FILE..."
javac "$JAVA_FILE"
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Run the compiled Java program
echo "Running $CLASS_NAME..."
java "$CLASS_NAME"
