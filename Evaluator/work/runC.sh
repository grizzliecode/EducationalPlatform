#!/bin/sh

# Check if the source file path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_c_or_cpp_file>"
    exit 1
fi

# Extract file path and name
SOURCE_FILE="$1"
FILE_NAME=$(basename -- "$SOURCE_FILE")
EXECUTABLE="${FILE_NAME%.*}"

pwd > echo
# Compile the C/C++ file
echo "Compiling $SOURCE_FILE..."
g++ "$SOURCE_FILE" -o "$EXECUTABLE"
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Run the compiled program
echo "Running $EXECUTABLE..."
./"$EXECUTABLE"
