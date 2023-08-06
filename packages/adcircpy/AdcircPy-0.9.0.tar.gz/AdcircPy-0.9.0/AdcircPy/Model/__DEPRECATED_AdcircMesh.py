from AdcircPy.Mesh import TrimeshSurface
from AdcircPy.Model.NodalAttributes import NodalAttributes
from AdcircPy.Model.TidalRun import TidalRun
from AdcircPy.Model.BestTrackRun import BestTrackRun


class AdcircMesh(TrimeshSurface):
    def __init__(self, x, y, elements, values, epsg, vertical_datum,
                 nodeID=None, elementID=None, description=None, fort13=None,
                 spinup_attributes=None, runtime_attributes=None,
                 datum_grid=None, **Boundaries):
        super(AdcircMesh, self).__init__(x, y, elements, values, epsg, nodeID,
                                         elementID, vertical_datum,
                                         **Boundaries)
        self._description = description
        self._init_NodalAttributes(fort13, spinup_attributes,
                                   runtime_attributes)

    def TidalRun(self, start_date, end_date, spinup_date=None,
                 constituents=None, netcdf=True, **kwargs):
        """ Instantiates an ADCIRC tidal only run. """
        return TidalRun(self, start_date, end_date, spinup_date, constituents,
                        netcdf=netcdf, **kwargs)

    def BestTrackRun(self, storm_id, start_date=None, end_date=None,
                     spinup_date=None, tides=True, netcdf=True, **kwargs):
        """
        Generates an ADCIRC hindcast run using wind data from the HURDAT2
        database.
        """
        return BestTrackRun(self, storm_id, start_date, end_date, spinup_date,
                            tides, netcdf, **kwargs)

    def generate_TAU0(self, spinup=True, runtime=True):
        self.NodalAttributes.generate_TAU0(self, spinup=spinup,
                                           runtime=runtime)

    def write_fort14(self, path):
        if self.datum != 'MSL':
            self.values = self.values + self.datum_offset
        f = open(path, 'w')
        f.write(self.description + '\n')
        f.write("{}  {}\n".format(self.elements.shape[0], self.values.size))
        for i in range(self.values.size):
            f.write("{:>10} {:15.10f} {:15.10f} {:15.10f}\n".format(
                        self.nodeID[i]+1, self.x[i], self.y[i], -
                        self.values[i]))
        # NOTE: Hard-coded for triangular elements. Multiple parts of the
        # code need to be expanded to accomodate for arbitrary geometries.
        for i in range(self.elements.shape[0]):
            f.write("{:5d}{:5d} {:5d} {:5d} {:5d}\n".format(
                                                self.elementID[i], 3,
                                                self.elements[i, 0]+1,
                                                self.elements[i, 1]+1,
                                                self.elements[i, 2]+1))
        if self.ocean_boundaries is None:
            ocean_boundaries = []
        else:
            ocean_boundaries = self.ocean_boundaries
        _sum = 0
        for i in range(len(ocean_boundaries)):
            _sum += ocean_boundaries[i].size
        f.write("{:d} = Number of open boundaries\n".format(
                                                        len(ocean_boundaries)))
        f.write("{:d} = Total number of open boundary nodes\n".format(_sum))
        if self.ocean_boundaries is not None:
            for i in range(len(self.ocean_boundaries)):
                f.write("{:d} = Number of nodes for open boundary {:d}\n"
                        .format(ocean_boundaries[i].size, i+1))
                for j in range(ocean_boundaries[i].size):
                    f.write("{:d}\n".format(ocean_boundaries[i][j]+1))
        remainingBoundaries = 0
        _sum = 0
        if self.land_boundaries is not None:
            remainingBoundaries += len(self.land_boundaries)
            for i in range(len(self.land_boundaries)):
                _sum += self.land_boundaries[i][0].size

        if self.inner_boundaries is not None:
            remainingBoundaries += len(self.inner_boundaries)
            for i in range(len(self.inner_boundaries)):
                _sum += self.inner_boundaries[i][0].size

        if self.inflow_boundaries is not None:
            remainingBoundaries += len(self.inflow_boundaries)
            for i in range(len(self.inflow_boundaries)):
                _sum += self.inflow_boundaries[i][0].size

        if self.outflow_boundaries is not None:
            remainingBoundaries += len(self.outflow_boundaries)
            for i in range(len(self.outflow_boundaries)):
                _sum += self.outflow_boundaries[i][0].size

        if self.weir_boundaries is not None:
            remainingBoundaries += len(self.weir_boundaries)
            for i in range(len(self.weir_boundaries)):
                _sum += self.weir_boundaries[i]['front_face'].size
                _sum += self.weir_boundaries[i]['back_face'].size

        if self.culvert_boundaries is not None:
            remainingBoundaries += len(self.culvert_boundaries)
            for i in range(len(self.culvert_boundaries)):
                _sum += self.culvert_boundaries[i]['front_face'].size
                _sum += self.culvert_boundaries[i]['back_face'].size
        f.write("{:d} = Number of land boundaries\n"
                .format(remainingBoundaries))
        f.write("{:d} = Total number of land boundary nodes\n".format(_sum))

        _cnt = 1
        if self.land_boundaries is not None:
            for i in range(len(self.land_boundaries)):
                f.write("{:d} {:d} = Number of nodes for land boundary {:d}\n"
                        .format(self.land_boundaries[i][0].size,
                                self.land_boundaries[i][-1], _cnt))
                _cnt += 1
                for j in range(self.land_boundaries[i][0].size):
                    f.write("{:d}\n".format(self.land_boundaries[i][0][j]+1))

        if self.inner_boundaries is not None:
            for i in range(len(self.inner_boundaries)):
                f.write("{:d} {:d}".format(self.inner_boundaries[i][0].size,
                                           self.inner_boundaries[i][-1])
                        + " = Number of nodes for closed (\"island\") "
                        + "boundary (land boundary {:d})\n".format(_cnt))
                _cnt += 1
                for j in range(self.inner_boundaries[i][0].size):
                    f.write("{:d}\n".format(self.inner_boundaries[i][0][j]+1))

        if self.inflow_boundaries is not None:
            for i in range(len(self.inflow_boundaries)):
                f.write("{:d} {:d}".format(
                                        self.inflow_boundaries[i][0].size,
                                        self.inflow_boundaries[i][-1])
                        + " = Number of nodes for inflow boundary (land "
                        + "boundary {:d})\n".format(_cnt))
                _cnt += 1
                for j in range(self.inflow_boundaries[i][0].size):
                    f.write("{:d}\n".format(self.inflow_boundaries[i][0][j]+1))

        if self.outflow_boundaries is not None:
            for i in range(len(self.outflow_boundaries)):
                f.write("{:d} {:d}".format(
                                        self.outflow_boundaries[i][0].size,
                                        self.outflow_boundaries[i][-1])
                        + " = Number of nodes for outflow boundary (land "
                        + "boundary {:d})\n".format(_cnt))
                _cnt += 1
                for j in range(self.outflow_boundaries[i][0].size):
                    f.write("{:d} {:.3f} {:.3f}\n"
                            .format(
                                self.outflow_boundaries[i][0][j]+1,
                                self.outflow_boundaries[i][1][j],
                                self.outflow_boundaries[i][2][j]))

        if self.weir_boundaries is not None:
            for i in range(len(self.weir_boundaries)):
                f.write("{:d} {:d}".format(
                                    self.weir_boundaries[i]['front_face'].size,
                                    self.weir_boundaries[i]['btype'])
                        + " = Number of node pairs for weir (land boundary "
                        + "{:d})\n".format(_cnt))
                _cnt += 1
                for j in range(self.weir_boundaries[i]['front_face'].size):
                    f.write("{:d} {:d} {:.3f} {:.3f} {:.3f}\n"
                            .format(
                             self.weir_boundaries[i]['front_face'][j]+1,
                             self.weir_boundaries[i]['back_face'][j]+1,
                             self.weir_boundaries[i]['height'][j],
                             self.weir_boundaries[i]
                             ['subcritical_flow_coefficient'][j],
                             self.weir_boundaries[i]
                             ['supercritical_flow_coefficient'][j]))

        if self.culvert_boundaries is not None:
            for i in range(len(self.culvert_boundaries)):
                f.write("{:d} {:d}".format(
                            len(self.culvert_boundaries[i]['front_face']),
                            self.culvert_boundaries[i]['btype'])
                        + " = Number of nodes pairs for culvert boundary "
                        + "(land boundary {:d})\n".format(_cnt))
                _cnt += 1
                for j in range(self.culvert_boundaries[i]['front_face'].size):
                    f.write("{:d} {:d} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}\n"
                            .format(
                             self.culvert_boundaries[i]['front_face'][j]+1,
                             self.culvert_boundaries[i]['back_face'][j]+1,
                             self.culvert_boundaries[i]['height'][j],
                             self.culvert_boundaries[i]
                             ['subcritical_flow_coefficient'][j],
                             self.culvert_boundaries[i]
                             ['supercritical_flow_coefficient'][j],
                             self.culvert_boundaries[i]
                             ['cross_barrier_pipe_height'][j],
                             self.culvert_boundaries[i]['friction_factor'][j],
                             self.culvert_boundaries[i]['pipe_diameter'][j]))
        f.close()
        if self.datum != 'MSL':
            self.values = self.values - self.datum_offset

    @classmethod
    def from_fort14(cls, fort14, epsg=4326, vertical_datum='LMSL',
                    fort13=None, spinup_attributes=None,
                    runtime_attributes=None, datum_grid=None):
        """ Initiliazes AdcircMesh class from fort14 file. """
        return cls(fort13=fort13, spinup_attributes=spinup_attributes,
                   runtime_attributes=runtime_attributes, epsg=epsg,
                   vertical_datum=vertical_datum, **cls.parse_fort14(fort14))

    @staticmethod
    def parse_fort14(path):
        fort14 = dict()
        fort14['x'] = list()
        fort14['y'] = list()
        fort14['values'] = list()
        fort14['nodeID'] = list()
        fort14['elements'] = list()
        fort14['elementID'] = list()
        # fort14['numberOfConnectedElements'] = list()
        fort14['ocean_boundaries'] = list()
        fort14['land_boundaries'] = list()
        fort14['inner_boundaries'] = list()
        fort14['inflow_boundaries'] = list()
        fort14['outflow_boundaries'] = list()
        fort14['weir_boundaries'] = list()
        fort14['culvert_boundaries'] = list()
        with open(path, 'r') as f:
            fort14['description'] = "{}".format(f.readline().strip('\n'))
            NE, NP = map(int, f.readline().split())
            _NP = len([])
            while _NP < NP:
                node_id, x, y, z = f.readline().split()
                fort14['nodeID'].append(int(node_id)-1)
                fort14['x'].append(float(x))
                fort14['y'].append(float(y))
                fort14['values'].append(float(z))
                _NP += 1
            _NE = len([])
            while _NE < NE:
                line = f.readline().split()
                fort14['elementID'].append(float(line[0]))
                # fort14['numberOfConnectedElements'].append(int(line[1]))
                if int(line[1]) != 3:
                    raise NotImplementedError('This mesh has non-triangular '
                                              + 'elements. This section of '
                                              + 'the code needs to be '
                                              + 'expanded to include this '
                                              + 'type of mesh.')
                fort14['elements'].append([int(x)-1 for x in line[2:]])
                _NE += 1
            NOPE = int(f.readline().split()[0])
            _NOPE = len([])
            f.readline()  # Number of total open ocean nodes. Not used.
            while _NOPE < NOPE:
                fort14['ocean_boundaries'].append({'nodeIndex': list()})
                NETA = int(f.readline().split()[0])
                _NETA = len([])
                while _NETA < NETA:
                    fort14['ocean_boundaries'][_NOPE]['nodeIndex'].append(
                                                int(f.readline().split()[0])-1)
                    _NETA += 1
                _NOPE += 1
            NBOU = int(f.readline().split()[0])
            _NBOU = len([])
            f.readline()
            while _NBOU < NBOU:
                NVELL, IBTYPE = map(int, f.readline().split()[:2])
                _NVELL = 0
                if IBTYPE in [0, 10, 20]:
                    fort14['land_boundaries'].append({'ibtype': IBTYPE,
                                                      'nodeIndex': list()})
                elif IBTYPE in [1, 11, 21]:
                    fort14['inner_boundaries'].append({'ibtype': IBTYPE,
                                                       'nodeIndex': list()})
                elif IBTYPE in [2, 12, 22, 102, 122]:
                    fort14['inflow_boundaries'].append({'ibtype': IBTYPE,
                                                        'nodeIndex': list()})
                elif IBTYPE in [3, 13, 23]:
                    fort14['outflow_boundaries'].append(
                                            {'ibtype': IBTYPE,
                                             'nodeIndex': list(),
                                             'barrierHeight': list(),
                                             'supercritFlowCoeff': list()})

                elif IBTYPE in [4, 24]:
                    fort14['weir_boundaries'].append(
                                            {'ibtype': IBTYPE,
                                             'frontFace': list(),
                                             'backFace': list(),
                                             'height': list(),
                                             'subcriticalFlowCoeff': list(),
                                             'supercriticalFlowCoeff': list()})
                elif IBTYPE in [5, 25]:
                    fort14['culvert_boundaries'].append(
                                            {'ibtype': IBTYPE,
                                             'frontFace': list(),
                                             'backFace': list(),
                                             'height': list(),
                                             'subcriticalFlowCoeff': list(),
                                             'supercriticalFlowCoeff': list(),
                                             'crossBarrierPipeHeight': list(),
                                             'frictionFactor': list(),
                                             'pipeDiameter': list()})
                else:
                    raise Exception('IBTYPE={}'.format(IBTYPE)
                                    + ' found in fort.14 not recongnized. ')
                while _NVELL < NVELL:
                    line = f.readline().split()
                    if IBTYPE in [0, 10, 20]:
                        fort14['land_boundaries'][-1]['nodeIndex'].append(
                                                                int(line[0])-1)
                    elif IBTYPE in [1, 11, 21]:
                        fort14['inner_boundaries'][-1]['nodeIndex'].append(
                                                                int(line[0])-1)
                    elif IBTYPE in [3, 13, 23]:
                        fort14['outflow_boundaries'][-1]['nodeIndex'].append(
                                                                int(line[0])-1)
                        fort14['outflow_boundaries'][-1]
                        ['external barrier height'].append(float(line[1]))
                        fort14['outflow_boundaries'][-1]
                        ['supercritical_flow_coeff'].append(float(line[2]))
                    elif IBTYPE in [2, 12, 22, 102, 122]:
                        fort14['iflow_boundaries'][-1]
                        ['nodeIndex'].append(int(line[0])-1)
                    elif IBTYPE in [4, 24]:
                        fort14['weir_boundaries'][-1]
                        ['frontFace'].append(int(line[0])-1)
                        fort14['weir_boundaries'][-1]
                        ['backFace'].append(int(line[1])-1)
                        fort14['weir_boundaries'][-1]
                        ['height'].append(float(line[2]))
                        fort14['weir_boundaries'][-1]
                        ['subcriticalFlowCoeff'].append(float(line[3]))
                        fort14['weir_boundaries'][-1]
                        ['supercriticalFlowCoeff'].append(float(line[4]))
                    elif IBTYPE in [5, 25]:
                        fort14['weir_boundaries'][-1]
                        ['frontFace'].append(int(line[0])-1)
                        fort14['weir_boundaries'][-1]
                        ['backFace'].append(int(line[1])-1)
                        fort14['weir_boundaries'][-1]
                        ['height'].append(float(line[2]))
                        fort14['weir_boundaries'][-1]
                        ['subcriticalFlowCoeff'].append(float(line[3]))
                        fort14['weir_boundaries'][-1]
                        ['supercriticalFlowCoeff'].append(float(line[4]))
                        fort14['weir_boundaries'][-1]
                        ['frictionFactor'].append(float(line[5]))
                        fort14['weir_boundaries'][-1]
                        ['pipeDiameter'].append(float(line[6]))
                    else:
                        Exception("Duck-typing error. "
                                  + "This exception should be unreachable.")
                    _NVELL += 1
                _NBOU += 1
        return fort14

    def _init_NodalAttributes(self, _NodalAttributes, spinup_attributes,
                              runtime_attributes):
        if isinstance(_NodalAttributes, str):
            self.NodalAttributes = NodalAttributes.from_fort13(
                                                        _NodalAttributes,
                                                        spinup_attributes,
                                                        runtime_attributes)
        elif isinstance(_NodalAttributes, NodalAttributes):
            self.NodalAttributes = _NodalAttributes
        else:
            self.NodalAttributes = NodalAttributes()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    # def make_plot(self, extent=None, axes=None, title=None, colors=256,
    #               cbar_label='elevation [m]', figsize=None, vmin=None,
    #               vmax=None, show=False):
    #   self._init_fig(axes, figsize)
    #   self._init_vmin(vmin)
    #   self._init_vmax(vmax)
    #   self._init_cmap_levels('topobathy', colors)
    #   self._init_norm()
    #   self._axes.tricontourf(self.x, self.y, self.elements, self.values,
    #                          levels=self._levels, cmap=self._cmap,
    #                          norm=self._norm, extend='both')
    #   self._auto_scaling(extent)
    #   self._init_title(title)
    #   self._init_cbar('neither')
    #   self._init_cbar_label('elevation [m]')
    #   self._auto_show(show)
