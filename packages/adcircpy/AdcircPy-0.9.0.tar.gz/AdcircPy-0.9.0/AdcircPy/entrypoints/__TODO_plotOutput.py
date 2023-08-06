#! /usr/bin/env python
import argparse
import matplotlib.pyplot as plt
from AdcircPy import AdcircPy


def parse_args():
    global args
    parser = argparse.ArgumentParser(description="Program to see a plot of an ADCIRC output.")
    parser.add_argument("output_path",  help="ADCIRC output file path. ASCII and NetCDF output types are supported.")
    parser.add_argument("--fort14_path",  help="ADCIRC mesh file path. Required for ASCII outputs.")
    args = parser.parse_args()


def main():
    parse_args()
    output = AdcircPy.read_output(args.output_path, fort14=args.fort14_path)
    output.make_plot()
    plt.show()


if __name__ == "__main__":
    main()