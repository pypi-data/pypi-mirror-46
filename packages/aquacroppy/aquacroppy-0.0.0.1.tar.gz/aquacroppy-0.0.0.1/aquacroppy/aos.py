import logging
import arrow
from .utils import ParamFile, keyword_value
import numpy as np
import pandas as pd

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


class AOS:
    """
    Python port of the AquaCropOS codebase for the WAVES lab at UCSB
    """

    def __init__(self, in_dir):
        """Defining initial values to the class variables. The AOS class is 
        written to loosely mimic the data structures of the original Matlab 
        implementation"""
        self.elapsed = 0
        self.running = False
        self.start = None
        self.end = None
        self.off_season = None
        self.total_days = 0
        self.weather_struct = None
        self.soil_struct = None
        self.crop_struct = None

        # Populating class variables to real values
        self.read_inputs(in_dir)

    def read_inputs(self, in_dir):
        """Read each input file. Populating the AOS object with attributes like
        those of AOS_InitializeStruct in the Matlab code.

        Function called from within __init__. Must be called before run()

        :param in_dir: input directory that contains all the input files

        :returns: True
        """
        # TODO: write this as an abstract class & raise 'not implemented error'
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError

        logging.debug("Reading Inputs")
        self.define_run_time(in_dir + "/Clock.txt")
        self.weather_struct = self.read_weather_inputs(in_dir + "/Weather.txt")
        self.soil_struct = self.read_soil_inputs(
            in_dir=in_dir,
            soil_file="/Soil.txt",
            soil_profile_file="/SoilProfile.txt"
        )
        self.crop_struct = self.read_crop_inputs(in_dir, "/CropMix.txt")
        return True

    def define_run_time(self, path_to_clock_file):
        """Simplified method to read from the Clock file to define simulation
           run time

           :param path_to_clock_file: tells us where to find the file
           :pre-condition: 4 time based attibutes are initialized to None
           :post-condition: 4 time based attributes are set for this object
               start
               end
               off_season
               total_days
           """
        logging.debug("  Defining run time")
        input_file = open(path_to_clock_file, "r")
        for line in input_file:
            if line.count("SimulationStartTime"):
                start = keyword_value(line)
            if line.count("SimulationEndTime"):
                end = keyword_value(line)
            if line.count("OffSeason"):
                self.off_season = keyword_value(line)
        input_file.close()

        self.start = arrow.get(start, "YYYY-MM-DD")
        self.end = arrow.get(end, "YYYY-MM-DD")
        assert start < end
        self.total_days = (self.end - self.start).days
        logging.debug("    %s days", str(self.total_days))

    def read_weather_inputs(self, path_to_weather_file):
        """Read from weather input file to populate the dataframe"""
        logging.debug("  Reading weather")
        weather = np.loadtxt(
            path_to_weather_file,
            delimiter="\t",
            comments="%",
            dtype={
                "names": (
                    "day",
                    "month",
                    "year",
                    "minTemp",
                    "maxTemp",
                    "Precipitation",
                    "ReferenceET",
                ),
                "formats": ("i", "i2", "i4", "f8", "f8", "f8", "f8"),
            },
        )
        return weather

    def read_soil_inputs(self, in_dir, soil_file, soil_profile_file):
        """ Reads from various soil files to setup the data structure needed
        for the simulation

        :pre-condition: self.soil_struct = None
        :post-condition: self.soil_struct = Utils.param_file with a pandas
        dataframe describing the soil composition.
        """
        logging.debug("  Reading soil")

        # General Soil file
        Soil = ParamFile(in_dir + soil_file)

        # Soil Profile
        profile = np.loadtxt(
            in_dir + soil_profile_file,
            delimiter="\t",
            comments="%",
            dtype={"names": ("soil", "dz", "type"),
                   "formats": ("i", "f4", "i")},
        )
        Layers = pd.DataFrame(profile)
        Layers["dzsum"] = Layers.dz.cumsum()
        Soil.Comp = Layers
        return Soil

    def read_crop_inputs(self, in_dir, cropmix_file):
        logging.debug("  Reading crop mix")
        CropMix = ParamFile(in_dir + cropmix_file)
        return CropMix

    def termination(self):
        """Check to see if the the simulated days elapsed matches total days to
        simulate
           :param: None
           :returns: Boolean
           """
        return self.total_days == self.elapsed

    def __str__(self):
        return "AOS simulating " + str(self.elapsed)

    def _perform_time_step(self):
        """Increment the elapsed time simulation
        This is the most involved step

        for example:
          %% Get weather inputs for current time step %%
          Weather = AOS_ExtractWeatherData();

          %% Get model solution %%
          [NewCond,Outputs] = AOS_Solution(Weather);

          %% Update initial conditions and outputs %%
          AOS_InitialiseStruct.InitialCondition = NewCond;
          AOS_InitialiseStruct.Outputs = Outputs;

          %% Check model termination %%
          AOS_CheckModelTermination();

          %% Update time step %%
          AOS_UpdateTime();
        """
        if (self.elapsed % 200) == 0:
            logging.debug(self)
            # Solution goes here
            # refer to chapter 1 in handbook
            # for explanations of variables
            # involved in solution calculations
        self.elapsed += 1

    def finish(self):
        """Finish method to write outputs"""
        logging.debug("Finishing AOS")
        self.running = False

    def run(self):
        """Run the model according to the input parameters"""
        self.running = True
        while self.termination() is False:
            self._perform_time_step()
        self.finish()
