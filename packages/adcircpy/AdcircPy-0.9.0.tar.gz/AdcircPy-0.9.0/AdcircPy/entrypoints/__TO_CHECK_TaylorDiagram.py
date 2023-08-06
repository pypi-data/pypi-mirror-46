import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from AdcircPy.Outputs import Maxele
from AdcircPy.Validation import TaylorDiagram
from AdcircPy.Validation.USGS import HighWaterMarks


class TaylorDiagramEntrypoint(object):

    def __init__(self):
        self.__parse_args()
        self.__init_HWM()
        self.__init_maxele()
        rejected_stations = set()
        models = list()
        for i, maxele in enumerate(self.maxele):
            models.append(list())
            for station in self.HWM.keys():
                if station not in rejected_stations:
                    value, reject = self.__check_reject(maxele, station)
                    models[i].append(value)
                    if reject:
                        rejected_stations.add(station)
                else:
                    models[i].append(value)
        for station in rejected_stations:
            self.HWM.pop(station)
        HWM = list()
        for station in self.HWM.keys():
            HWM.append(self.HWM[station]['elev_ft']/3.28084)
        HWM = np.asarray(HWM)
        models = [np.asarray(model) for model in models]
        anynan = ~np.any(np.isnan(np.vstack(models).T), axis=1)
        models = [model[np.where(anynan)] for model in models]
        taylor_data = [(model.std(ddof=1), np.corrcoef(HWM, model)[0, 1])
                       for model in models]
        refstd = HWM.std(ddof=1)
        dia = TaylorDiagram(refstd,
                            fig=plt.figure(figsize=(9, 9)),
                            rect=111,
                            label="Reference")
        dia.add_sample(refstd, 1., True,
                       label='Ref',
                       marker='*',
                       markersize=6)
        for i, (stddev, corrcoef) in enumerate(taylor_data):
            dia.add_sample(stddev, corrcoef, False,
                           marker='*', markersize=6,
                           label=self.args.legend[i])
        plt.show()

    def __parse_args(self):
        parser = argparse.ArgumentParser(
            description="Program to generate a Taylor Diagram.")
        parser.add_argument("event_name", help="Event name and year, "
                            + "for example, Sandy2012")
        parser.add_argument("datum_grid")
        parser.add_argument("maxele", nargs='+')
        parser.add_argument('--legend', nargs='*')
        parser.add_argument('--fort14', help="Path to mesh file. "
                            + "Required if maxele file is ASCII.")
        parser.add_argument('--csv', help="Use CSV file for High Water Marks "
                            + "instead of USGS REST server.")
        self.args = parser.parse_args()
        if self.args.legend is not None:
            if len(self.args.legend) != len(self.args.maxele):
                raise Exception("If legend entries are provided, "
                                + "they must match the same number of provided"
                                + " input files.")
        else:
            self.args.legend = list()
            for i, maxele in enumerate(self.args.maxele):
                self.args.legend("model {}".format(i))

    def __init_HWM(self):
        if self.args.csv is not None:
            self.HWM = HighWaterMarks.from_csv(self.args.csv)
        else:
            self.HWM = HighWaterMarks.from_event_name(self.args.event_name)

    def __init_maxele(self):
        self.maxele = list()
        for maxele in self.args.maxele:
            if Maxele.is_netcdf(maxele):
                self.maxele.append(Maxele.from_netcdf(
                                    maxele, datum_grid=self.args.datum_grid))
            else:
                if self.args.fort14 is None:
                    raise IOError("A mesh file is required if the maxele file "
                                  + "is ASCII format.")
                self.maxele.append(Maxele.from_ascii(
                                    maxele,
                                    self.args.fort14,
                                    datum_grid=self.args.datum_grid))

    def __check_reject(self, maxele, station):
        x = self.HWM[station]['longitude']
        y = self.HWM[station]['latitude']
        element = maxele.get_element_containing_coord((x, y))
        # first check: at least one element contains the point
        if element is None:
            return np.nan, True
        # second check: the element is not a masked element
        tree = cKDTree(np.vstack([maxele.x[element],
                                  maxele.y[element]]).T)
        _, indexes = tree.query([x, y], k=3)
        for value in maxele.values[element][indexes]:
            if np.ma.is_masked(value) is True:
                return np.nan, True
        return maxele.values[indexes][0], False


def main():
    TaylorDiagramEntrypoint()


if __name__ == '__main__':
    main()

"""
export PREFIX_DIR=/ddnas/jreniel/ADCIRC/HSOFS/Sandy2012/CoastalAct && \
TaylorDiagram Sandy2012 /ddnas/jreniel/ADCIRC/HSOFS/hsofs_nomad_msl2navd88.grd \
$PREFIX_DIR/02_HWRF_4cases/a52_SAN_ATM2OCN_v2.0/rt_20180510_h13_m02_s21r175/maxele.63.nc \
$PREFIX_DIR/02_HWRF_4cases/a53_SAN_ATM_WAV2OCN_v2.0/rt_20180510_h13_m23_s44r792/maxele.63.nc \
$PREFIX_DIR/03_HWRF_land_mask_update/a50_SAN_ATM2OCN_v2.1_new_hwrf_land_mask/rt_20181128_h12_m48_s00r528/maxele.63.nc \
$PREFIX_DIR/03_HWRF_land_mask_update/a70_SAN_ATM_WAV2OCN_v2.1_new_hwrf_land_mask/rt_20181128_h12_m47_s34r744/maxele.63.nc \
--legend "PreHWRF ATM2OCN" "PreHWF ATMWAV2OCN" "UpdHWRF ATM2OCN" "UpdHWRF ATMWAV2OCN" && \
unset PREFIX_DIR
""" 