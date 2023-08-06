#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Cyrille Favreau <cyrille.favreau@gmail.com>
#
# This file is part of pyPhaneron
# <https://github.com/favreau/pyPhaneron>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.


class GraphExplorer(object):

    """ GraphExplorer """
    def __init__(self, client):
        """
        Create a new Graph instance
        """
        self._client = client.rockets_client

    def __str__(self):
        """Return a pretty-print of the class"""
        return "GraphExplorer"

    def load_positions_from_file(self, path, mesh_file='', radius=1.0, scale=[1.0, 1.0, 1.0]):
        """
        Loads node positions from file
        :param path: Path of the file where positions are stored
        :param mesh_file: Path of the mesh file to be placed at each position
        :param radius: Radius of the sphere used to represent the node
        :param scale: Scaling to use for the positions
        :return: Result of the request submission
        """
        xs = []
        ys = []
        zs = []
        with open(path) as f:
            for l in f:
                x, y, z = l.split()
                xs.append(float(x))
                ys.append(float(y))
                zs.append(float(z))

        params = dict()
        params['x'] = xs * scale[0]
        params['y'] = ys * scale[1]
        params['z'] = zs * scale[2]
        params['radius'] = radius
        params['meshFile'] = mesh_file
        self._client.request('positions', params=params)

    def create_random_connectivity(self, min_distance=0, max_distance=1e6, density=1):
        """
        Creates random connectivity between nodes
        :param min_distance: Minimum distance between nodes to be connected
        :param max_distance: Maximum distance between nodes to be connected
        :param density: Nodes to skip between every new connection
        :return: Result of the request submission
        """
        params = dict()
        params['minLength'] = min_distance
        params['maxLength'] = max_distance
        params['density'] = density
        return self._client.request('randomConnectivity', params=params)

    def load_connectivity_from_file(self, path, matrix_id, dimension_range=(1, 1e6)):
        """
        :param path: Path to the h5 file containing the connectivity data
        :param matrix_id: Id of the matrix used to create the connections
        :param dimension_range: Range of dimensions
        :return: Result of the request submission
        """
        params = dict()
        params['filename'] = path
        params['matrixId'] = matrix_id
        params['minDimension'] = dimension_range[0]
        params['maxDimension'] = dimension_range[1]
        return self._client.request('connectivity', params=params)

    def initialize_morphing(self, model_id, nb_steps=1000):
        """
        :param model_id: Id of the model
        :param nb_steps: Number of morphing steps
        :return: Result of the request submission
        """
        params = dict()
        params['modelId'] = model_id
        params['nbSteps'] = nb_steps
        return self._client.request('initializeMorphing', params=params)

    def set_morphing_step(self, model_id, step):
        """
        :param model_id: Id of the model
        :param nb_steps: Number of morphing steps
        :return: Result of the request submission
        """
        params = dict()
        params['modelId'] = model_id
        params['step'] = step
        return self._client.request('setMorphingStep', params=params)
