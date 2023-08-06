#! /usr/bin/env python
import argparse
import matplotlib.pyplot as plt 
import numpy as np
from scipy import spatial
from AdcircPy.Outputs import HarmonicConstituentsElevationStations
from AdcircPy.Validation import COOPS

class TidalConstituentsStationsPlot(object):
  
  def __init__(self):
    self._parse_args()
    self._init_fort51()
    self._init_COOPS()
    self._make_plot()

  def _parse_args(self):
    args = argparse.ArgumentParser(description='Program for validating tidal harmonic constituent outputs against COOPS data.')
    args.add_argument('fort51', help='Path to fort.51 file. This is the harmonic constituents station output file.') 
    args.add_argument('fort15', help='Path to the fort.15 file used for this run (optional).')
    args.add_argument('--save-directory', '-sd', help='Directory where to save files.')
    args.add_argument('--show', help='Flag to show the file')
    self.args = args.parse_args()

  def _init_fort51(self):
    self.fort51 = HarmonicConstituentsElevationStations(self.args.fort51, self.args.fort15)

  def _init_COOPS(self):
    self.COOPS = COOPS.HarmonicConstituents(self.fort51.keys())

  def _make_plot(self):
    for station in self.fort51.keys():
      plt.subplot(111)
      x=list()
      y1=list()
      y2=list()
      ticklabels=list()
      ticklocs=list()
      for i, constituent in enumerate(self.fort51.constituents):
        if constituent in self.COOPS[station].keys():  
          frequency = (self.fort51[station][constituent]['orbital_frequency']/(2*np.pi))*(60.*60.*24.)
          coops = self.COOPS[station][constituent]['amplitude']
          adcirc = self.fort51[station][constituent]['amplitude']
          bottombar=np.min([coops, adcirc])
          topbar=np.max([coops, adcirc])
          if bottombar==adcirc:
            bottomColor='blue'
            topColor='red'
          else:
            bottomColor='red'
            topColor='blue'
          if bottombar>0:
            ax1 = plt.bar(frequency, bottombar, log=True, align='center',
                                            width=0.01,
                                            color=bottomColor)
            ax2 = plt.bar(frequency, topbar, log=True, align='center',
                                            bottom=bottombar,
                                            width=0.01,
                                            color=topColor)
          elif bottombar==0 and topbar>0:
            plt.bar(frequency, topbar, log=True, align='center',
                                                 color=topColor,
                                                 width=0.01)
          ticklocs.append(frequency)
          ticklabels.append(constituent)
      plt.xscale('log')
      plt.gca().set_xticks(ticklocs)
      plt.gca().set_xticklabels(ticklabels)
      plt.gca().set_title('station id: {}'.format(station))
      plt.legend([ax1, ax2], ['Coops', 'Adcirc'])
      if self.args.show==True:
        plt.show()
      if self.args.save_directory is not None:
        plt.gcf().savefig()
      plt.close(plt.gcf())

if __name__ == "__main__":
  TidalConstituentsStationsPlot()
