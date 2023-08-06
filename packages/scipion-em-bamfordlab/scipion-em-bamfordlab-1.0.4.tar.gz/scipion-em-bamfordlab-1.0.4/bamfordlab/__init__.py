# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se)
# *
# * SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os

import pyworkflow.em
from pyworkflow.utils import Environ

from bamfordlab.constants import ETHAN, ETHAN_HOME, V1_2


_logo = "bamford_logo.gif"
_references =['Kivioja2000']


class Plugin(pyworkflow.em.Plugin):
    _homeVar = ETHAN_HOME
    _pathVars = [ETHAN_HOME]
    _supportedVersions = [V1_2]

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(ETHAN_HOME, 'ethan-1.2')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch Ethan. """
        environ = Environ(os.environ)

        environ.update({
            'PATH': Plugin.getHome()},
            position=Environ.BEGIN)

        return environ

    @classmethod
    def getProgram(cls):
        return os.path.join(Plugin.getHome(), ETHAN)

    @classmethod
    def isVersionActive(cls):
        return cls.getActiveVersion().startswith(V1_2)

    @classmethod
    def defineBinaries(cls, env):
        env.addPackage('ethan', version='1.2',
                       tar='ethan-1.2.tgz',
                       commands=[('make', 'ethan')],
                       default=True)


pyworkflow.em.Domain.registerPlugin(__name__)
