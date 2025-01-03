import os
import argparse
import logging
import sys
import subprocess
import re

CLUES_OUTPUT = "/work/clues.txt"

def compare_files(file1, file2):
    """Compare the content of two files."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            if f1.read() == f2.read():
                return True
            else:
                return False
    except Exception as e:
        logging.info("runtime exception no file written")
        raise Exception("")

def isError(err):
    error_pattern = r"error:.*"
    # Check if the output contains any error messages
    errors = re.findall(error_pattern, err)
    if errors:
        return True
    return False

if __name__ == "__main__":
    clues = ""
    logging.basicConfig(
        filename=sys.argv[0][:-3] + ".log",
        level=logging.INFO,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--language", help="the compilers language")
    parser.add_argument("-i","--input",help="input file")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-f", "--file", help="the name of the file where the response should be")
    parser.add_argument("-s", "--source",help="source file to be run")
    parser.add_argument("-c", "--clean", action='store_true', help= "delete files after evaluating")
    args = parser.parse_args()
    try:
        if not len(args.language) > 0:
            logging.info("No language was specified")
            raise Exception("No language was specified")
        if not len(args.file) > 0:
            logging.info("No file for responses was specified")
            raise Exception("No file for responses was specified")
        if not os.path.isfile(os.path.normpath(os.path.abspath(args.input))):
            logging.info("No input file was specified")
            raise Exception("No input file was specified")
        if not os.path.isfile(os.path.normpath(os.path.abspath(args.output))):
            logging.info("No output file was specified")
            raise Exception("No output file was specified")
        if not os.path.isfile(os.path.normpath(os.path.abspath(args.source))):
            logging.info("No source file was specified")
            raise Exception("No source file was specified")
        if args.language == "python":
            command = ["python", args.source]
            p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            _, err = p.communicate()
            if len(err) > 0:
                logging.info(f"runtime errors {err} {65}")
                raise Exception("")
            if compare_files(args.output, args.file):
                clues = "Accepted"
            else:
                clues = "Wrong Answer"
        elif args.language == "java":
            command = ["./runJava.sh", args.source]
            p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            _, err = p.communicate()
            if len(err) > 0:
                logging.info(f"runtime errors {err} {76}")
                raise Exception("")
            if compare_files(args.output, args.file):
                clues = "Accepted"
            else:
                clues = "Wrong Answer"
        elif args.language == "c/c++":
            command = ["./runC.sh", args.source]
            p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            ot, err = p.communicate()
            if isError(str(err, 'utf-8')):
                logging.info(f"runtime errors {err} {87}")
                raise Exception("")
            if compare_files(args.output, args.file):
                clues = "Accepted"
            else:
                clues = "Wrong Answer"
        with open(CLUES_OUTPUT, "w") as fout:
            fout.write(clues)
            
    except Exception as e:
        with open(CLUES_OUTPUT, "w") as fout:
            fout.write("Runtime exception.\n")
            fout.write(str(e))
    finally:
        if args.clean:
            p = subprocess.Popen(["/bin/sh","-c",f"rm {args.file} {args.input} {args.output} {args.source}"])
            p.wait()
