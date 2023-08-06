#! /usr/bin/env python
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from AdcircPy.Validation import COOPS
from AdcircPy import AdcircPy

class TidalConstituentStationValidation(object):
  def __init__(self):
    self._parse_args()
    self._init_fort51()
    self._validate_coops_stations()
    self._make_amplitude_plots()
    # self._make_phase_plots()

  def _parse_args(self):
    args = argparse.ArgumentParser(description='Program for validating tidal harmonic constituent outputs against COOPS data.')
    args.add_argument('fort51', help='Path to the harmonic constituents station output file.') 
    args.add_argument('fort15', help='Path to the fort.15 file. Required only if not using netcdf output.', nargs='?') 
    self.args = args.parse_args()

  def _init_fort51(self):
    self.fort51 = AdcircPy.read_output(self.args.fort51, fort15=self.args.fort15)

  def _validate_coops_stations(self):
    coops_stations = {'keys' : list(), 'coops_id' : list()}
    for station in self.fort51.keys():
      _id = station.split()
      coops_id = [x for x in _id if len(x)==7 and x!='0000000' and x.isdigit()]
      if len(coops_id)>0:
        coops_stations['keys'].append(station)
        coops_stations['coops_id'].append(coops_id.pop())
    self.coops = COOPS.HarmonicConstituents(coops_stations['coops_id'])
    final_keys = list()
    for station in self.coops.keys():
      if self.coops[station] is not None:
        idx = coops_stations['coops_id'].index(station)
        final_keys.append(coops_stations['keys'][idx])
    self.amplitudes = dict()
    self.phases = dict()
    for station in final_keys:
      for component in self.fort51[station]['data'].keys():
        station_id = coops_stations['coops_id'][coops_stations['keys'].index(station)]
        if component in self.coops[station_id].keys():
          if component not in self.amplitudes.keys():
            self.amplitudes[component] = {'coops':list(), 'adcirc':list()}
            self.phases[component] = {'coops':list(), 'adcirc':list()}
          self.amplitudes[component]['coops'].append(self.coops[station_id][component]['amplitude'])
          self.amplitudes[component]['adcirc'].append(self.fort51[station]['data'][component]['amplitude'])
          self.phases[component]['coops'].append(self.coops[station_id][component]['phase'])
          self.phases[component]['adcirc'].append(self.fort51[station]['data'][component]['phase'])

  def _init_save_dir(self):
    os.makedirs()

  def _make_amplitude_plots(self):
    sns.set(style="darkgrid", color_codes=True)
    sns.set_context("talk")
    for component in self.amplitudes.keys():
      x = np.asarray(self.amplitudes[component]['coops'])
      y = np.asarray(self.amplitudes[component]['adcirc'])
      _max = 100
      middle_line = np.linspace(0, 1.1*_max, num=1.1*_max)
      plt.plot(middle_line, middle_line, linestyle='--', color='grey', alpha=0.75)
      sns.regplot(x, y, fit_reg=False, ci=None)
      plt.title(component)
      plt.axis('scaled')
      plt.axis([0, 1.1*np.max([x.max(), y.max()]), 0, 1.1*np.max([x.max(), y.max()])])
      plt.gca().set(xlabel='COOPS', ylabel='ADCIRC')
      plt.gcf().set_size_inches(10.5, 10.5)
      plt.gcf().savefig(component+'.png',bbox_inches='tight')
      plt.close(plt.gcf())

  def _make_phase_plots(self):
    for component in self.phases.keys():
      plt.scatter(self.phases[component]['coops'], self.phases[component]['adcirc'])
      plt.title(component)
      plt.axis('scaled')
      plt.show()
      plt.close(plt.gcf())


if __name__ == '__main__':
  TidalConstituentStationValidation()