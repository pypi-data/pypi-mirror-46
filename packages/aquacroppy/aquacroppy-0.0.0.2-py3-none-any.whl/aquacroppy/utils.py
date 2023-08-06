class ParamFile(object):
    def __init__(self, input_file):
        self._read_file(input_file)

    def _read_file(self, input_file):
        """Reads lines of an input file that are not comments"""
        for line in open(input_file):
            li = line.strip()
            if not li.startswith("%"):
                self._readline(line.strip())

    def _readline(self, line):
        """Sets attributes of a dynamic class (guessing the type)"""
        lineItems= [x.strip() for x in line.split(":", 1)]

        if line.endswith(".txt"):
            pass  # some files contain references to other filenames
        elif "/" in line:
            setattr(self, lineItems[0], str(lineItems[1]))
        else:
            setattr(self, lineItems[0], float(lineItems[1]))

    def _parse_date(self, line):
        l = [x.strip() for x in line.split(":", 1)]
        return(l[0],l[1])
        setattr(self,l[0], str(l[1]))

def keyword_value(line):
    """ strips a line to extract the value"""
    return line.split(":")[1].strip()

class Crops(ParamFile):
    """For this model, there are 2 top level parameters and one or more Crops.

    The Crops object is the container for the crop information.
    Each crop has an associated name and several parameter files.
    """

    def __init__(self, cropmix, croprotation):
        super().__init__(cropmix)
        # Proceed something like the following
        # for crops in cropmix:
        #    Initialize a Crop object
        #    add crop to collection

class Crop(ParamFile):
    def __init__(self, name, input_file, irrigation_file):
        super().__init__(input_file)
        # In AquaCrop, each crop struct has 89 fields of varying types
        # Should we do the same here?
