class ParamFile(object):
    def __init__(self, input_file):
        self._read_file(input_file)

    def _read_file(self, input_file):
        for line in open(input_file):
            li = line.strip()
            if not li.startswith("%"):
                self._readline(line.strip())

    def _readline(self, line):
        if line.endswith(".txt"):
            pass  # some files contain references to other filenames
        else:
            l = [x.strip() for x in line.split(":", 1)]
            setattr(self, l[0], float(l[1]))

def keyword_value(line):
    """ strips a line to extract the value"""
    return line.split(":")[1].strip()