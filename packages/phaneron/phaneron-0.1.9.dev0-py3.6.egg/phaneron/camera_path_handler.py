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


class CameraPathHandler(object):

    """ Circuit Explorer """
    def __init__(self, control_points, nb_steps_per_sequence, smoothing_size):
        """
        Create a new Camera Path Handler instance
        """
        self._control_points = control_points
        self._nb_steps_per_sequence = nb_steps_per_sequence
        self._smoothing_size = smoothing_size

        self._smoothed_key_frames = list()

        self._build_path()

    def __str__(self):
        """Return a pretty-print of the class"""
        return "Camera Path Handler"

    def _build_path(self):
        origins = list()
        directions = list()
        ups = list()
        for s in range(len(self._control_points)):

            p0 = self._control_points[s]
            p1 = self._control_points[(s + 1) % len(self._control_points)]

            for i in range(self._nb_steps_per_sequence):
                origin = [0, 0, 0]
                direction = [0, 0, 0]
                up = [0, 0, 0]

                t_origin = [0, 0, 0]
                t_direction = [0, 0, 0]
                t_up = [0, 0, 0]
                for k in range(3):
                    t_origin[k] = \
                        (p1['origin'][k] - p0['origin'][k]) / \
                        float(self._nb_steps_per_sequence)
                    t_direction[k] = \
                        (p1['direction'][k] - p0['direction'][k]) / \
                        float(self._nb_steps_per_sequence)
                    t_up[k] = \
                        (p1['up'][k] - p0['up'][k]) / \
                        float(self._nb_steps_per_sequence)

                    origin[k] = p0['origin'][k] + t_origin[k] * float(i)
                    direction[k] = p0['direction'][k] + t_direction[k] * float(i)
                    up[k] = p0['up'][k] + t_up[k] * float(i)

                origins.append(origin)
                directions.append(direction)
                ups.append(up)

        nb_frames = len(origins)
        for i in range(nb_frames):
            o = [0, 0, 0]
            d = [0, 0, 0]
            u = [0, 0, 0]
            for j in range(int(self._smoothing_size)):
                index = (i + j) % nb_frames
                for k in range(3):
                    o[k] = o[k] + origins[index][k]
                    d[k] = d[k] + directions[index][k]
                    u[k] = u[k] + ups[index][k]
            self._smoothed_key_frames.append([
                (o[0] / self._smoothing_size,
                 o[1] / self._smoothing_size,
                 o[2] / self._smoothing_size),
                (d[0] / self._smoothing_size,
                 d[1] / self._smoothing_size,
                 d[2] / self._smoothing_size),
                (u[0] / self._smoothing_size,
                 u[1] / self._smoothing_size,
                 u[2] / self._smoothing_size)])

    def get_nb_frames(self):
        return len(self._smoothed_key_frames)

    def get_key_frame(self, frame):
        if frame < len(self._smoothed_key_frames):
            return self._smoothed_key_frames[frame]
        else:
            raise KeyError;


def main():
    camera_key_frames = [
        {'direction': [0.4464535260825596, -0.31344617366155064, -0.8381114157827599],
         'origin': [-0.3431969846327868, 1.0919918939720272, 2.082903879772819],
         'up': [0.07470689889906587, 0.9464263169085163, -0.3141593638901529]},
        {'direction': [-0.4467646010767981, -0.081873824160088, -0.8908973387220844],
         'origin': [2.1088376099768977, 0.7046066660433434, 2.7914318045623223],
         'up': [-0.01708089275302226, 0.9964028077835931, -0.08300414293113119]},
        {'direction': [-0.4467646010767983,
                       -0.08187382416008794,
                       -0.8908973387220843],
         'origin': [1.1342840455928969, 0.7954079483705041, 3.451511834403204],
         'up': [-0.017080892753022246, 0.9964028077835931, -0.08300414293113116]}]

    cph = CameraPathHandler(camera_key_frames, 100, 10)
    print(cph.get_key_frame(10))


if __name__ == '__main__':
    main()