import os


def linuxize_newlines(input_name, output_name):
    """
    Makes a copy of a file and ensure Unix newline characters.

    :param str input_name: name of the file to process
    :param str output_name: name of the file copy with Unix newlines
    """
    with open(input_name, "rb") as infile:
        lines = infile.readlines()
        with open(output_name, "wb") as outfile:
            for line in lines:
                line = line[:-3] + os.linesep.encode()
                outfile.write(line)
