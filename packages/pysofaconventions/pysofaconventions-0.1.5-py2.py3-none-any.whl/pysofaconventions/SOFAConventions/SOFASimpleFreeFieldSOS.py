# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Copyright (c) 2018, Eurecat / UPF
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   @file   SOFASimpleFreeFieldSOS.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import warnings

from pysofaconventions import SOFAFile, SOFAWarning


class SOFASimpleFreeFieldSOS(SOFAFile):
    conventionVersionMajor = 1
    conventionVersionMinor = 0

    def isValid(self):
        """
        Check for convention consistency
        It ensures general file consistency, and also specifics for this convention.
        - 'DataType' == 'SOS'
        - 'SOFAConventions' == 'SimpleFreeFieldSOS'
        - 'RoomType' == 'free field'
        - Mandatory attribute 'DatabaseName'
        - E == 1
        - N must be multiple of 6

        :return:    Boolean
        :raises:    SOFAWarning with error description, in case
        """

        # Check general file validity
        if not SOFAFile.isValid(self):
            return False

        # Ensure specifics of this convention

        # # Attributes
        if not self.isSOSDataType():
            warnings.warn('DataType is not "SOS", got: "{}"'.format(
                self.getGlobalAttributeValue('DataType')), SOFAWarning)
            return False

        if not self.getGlobalAttributeValue('SOFAConventions') == 'SimpleFreeFieldSOS':
            warnings.warn('SOFAConventions is not "SimpleFreeFieldSOS", got: "{}"'.format(
                self.getGlobalAttributeValue('SOFAConventions')), SOFAWarning)
            return False

        if not self.getGlobalAttributeValue('RoomType') == 'free field':
            warnings.warn('RoomType is not "free field", got: "{}"'.format(self.getGlobalAttributeValue('RoomType')),
                          SOFAWarning)
            return False

        if not self.hasGlobalAttribute('DatabaseName'):
            warnings.warn('Missing required Global Attribute "DatabaseName"', SOFAWarning)
            return False

        # # Dimensions
        if not self.getDimensionSize('E') == 1:
            warnings.warn('Number of emitters (E) is not "1", got "{}"'.format(self.getDimensionSize('E')),
                          SOFAWarning)
            return False

        if not (self.getDimensionSize('N') % 6 == 0):
            warnings.warn('Number of coefficients (N) is not multiple of "6", got "{}"'.format(self.getDimensionSize('N')),
                          SOFAWarning)
            return False

        return True
