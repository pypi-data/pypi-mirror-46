#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2015 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Docstring for gerberfiles
"""

import os
from gerber.pcb import PCB
from gerber.render import theme
from gerber.render import GerberCairoContext


def render_gerber_images(directory, outfolder, outfname):
    outfpath = os.path.join(outfolder, outfname)
    pcb = PCB.from_directory(directory)

    top = pcb.top_layers
    bottom = pcb.bottom_layers
    copper = pcb.copper_layers
    outline = pcb.outline_layer

    if outline:
        top = [outline] + top
        bottom = [outline] + bottom
        copper = [outline] + copper + pcb.drill_layers

    renderer = GerberCairoContext()

    renderer.render_layers(
        layers=top, theme=theme.THEMES['default'],
        max_height=1080, max_width=1920,
        filename='{0}.top.png'.format(outfpath)
    )
    renderer.render_layers(
        layers=bottom, theme=theme.THEMES['default'],
        max_height=1080, max_width=1920,
        filename='{0}.bottom.png'.format(outfpath)
    )
    renderer.render_layers(
        layers=copper, theme=theme.THEMES['Transparent Multilayer'],
        max_height=1080, max_width=1920,
        filename='{0}.devel.png'.format(outfpath)
    )
