#! /usr/bin/env python
import argparse
import matplotlib.pyplot as plt 
import numpy as np
from scipy import spatial
from AdcircPy.Outputs import HarmonicConstituentsElevationStations
from AdcircPy.Validation import COOPS

class ElevationStationsOutputPlot(object):
  
  def __init__(self):
    self._parse_args()

  def _parse_args(self):
    args = argparse.ArgumentParser(description='Program for validating tidal harmonic constituent outputs against COOPS data.')
    args.add_argument('fort51', help='Path to fort.51 file. This is the harmonic constituents station output file.') 
    args.add_argument('fort15', help='Path to the fort.15 file used for this run (optional).', nargs='?')
    self.args = args.parse_args()

if __name__ == "__main__":
  ElevationStationsOutputPlot()
