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
#   @file   test_SOFAAPI.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import *

def test_getAPIName():
    assert SOFAAPI.getAPIName() == 'pysofaconventions'

def test_getAPIVersion():

    versionString = str(SOFAVersion.SOFAVersionMajor)\
                    +"."+str(SOFAVersion.SOFAVersionMinor)\
                    +"."+str(SOFAVersion.SOFAVersionRelease)

    assert SOFAAPI.getAPIVersion() == versionString

def test_getAPIVersionMajor():
    assert SOFAAPI.getAPIVersionMajor() == SOFAVersion.SOFAVersionMajor

def test_getAPIVersionMinor():
    assert SOFAAPI.getAPIVersionMinor() == SOFAVersion.SOFAVersionMinor

def test_getAPIVersionRelease():
    assert SOFAAPI.getAPIVersionRelease() == SOFAVersion.SOFAVersionRelease

def test_getAPICopyright():
    assert SOFAAPI.getAPICopyright() == SOFAAPI.copyrightString

def test_getSpecificationsVersion():

    versionString = str(SOFAVersion.SOFASpecificationsMajor)\
                    +"."+str(SOFAVersion.SOFASpecificationsMinor)

    assert SOFAAPI.getSpecificationsVersion() == versionString

def test_getSpecificationsVersionMajor():
    assert SOFAAPI.getSpecificationsVersionMajor() == SOFAVersion.SOFASpecificationsMajor

def test_getSpecificationsVersionMinor():
    assert SOFAAPI.getSpecificationsVersionMinor() == SOFAVersion.SOFASpecificationsMinor