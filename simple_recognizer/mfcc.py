#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Siegfried-A. Gevatter <siegfried@gevatter.com>
# Released under the ISC License.
#
# This file contains code by "alf." from StackOverflow, released
# under the CC-BY-SA Unported.

import math
import numpy
from scipy.fftpack import dct
from scipy.io import wavfile

def freqToMel(freq):
    return 1127.01048 * math.log(1 + freq / 700.0)

def melToFreq(mel):
    return 700 * (math.exp(freq / 1127.01048 - 1))

def melFilterBank(blockSize, numCoefficients, minHz=0, maxHz=22000):
    numBands = int(numCoefficients)
    maxMel = int(freqToMel(maxHz))
    minMel = int(freqToMel(minHz))

    # Create a matrix for triangular filters, one row per filter
    filterMatrix = numpy.zeros((numBands, blockSize))

    melRange = numpy.array(xrange(numBands + 2))

    melCenterFilters = melRange * (maxMel - minMel) / (numBands + 1) + minMel

    # each array index represent the center of each triangular filter
    aux = numpy.log(1 + 1000.0 / 700.0) / 1000.0
    aux = (numpy.exp(melCenterFilters * aux) - 1) / 22050
    aux = 0.5 + 700 * blockSize * aux
    aux = numpy.floor(aux)
    centerIndex = numpy.array(aux, int)

    for i in xrange(numBands):
        start, centre, end = centerIndex[i:i + 3]
        k1 = numpy.float32(centre - start)
        k2 = numpy.float32(end - centre)
        up = (numpy.array(xrange(start, centre)) - start) / k1
        down = (end - numpy.array(xrange(centre, end))) / k2

        filterMatrix[i][start:centre] = up
        filterMatrix[i][centre:end] = down

    return filterMatrix.transpose()

def MFCC(signal):
    complexSpectrum = numpy.fft.fft(signal)
    powerSpectrum = abs(complexSpectrum) ** 2
    filteredSpectrum = numpy.dot(powerSpectrum, melFilterBank(2048, 13))
    logSpectrum = numpy.log(filteredSpectrum)
    dctSpectrum = dct(logSpectrum, type=2)
    liftered = dctSpectrum[:13]
    return liftered

def rootMeanSquare(signal):
    rms = math.sqrt(sum(signal**2) / len(signal))
    return rms

def zeroCrossingRate(signal):
    signal = filter(None, signal)
    zcr = len(numpy.nonzero(numpy.diff(numpy.sign(signal)))[0])
    zcr = float(zcr) / len(signal)
    return zcr

def featureScaleVectors(vectors, first_col, last_col):
    for i in range(first_col, last_col):
        _min = min(vectors[:,i])
        _max = max(vectors[:,i])
        vectors[:,i] -= _min
        vectors[:,i] /= (_max - _min)
    return vectors

def wavToFeatures(filename, blockSize=2048, shiftSize=1024):
    sampleRate, signal = wavfile.read(filename)
    assert sampleRate == 44100

    vectors = []
    hamming = numpy.hamming(blockSize)
    #prev_frame = signal[0:blockSize]
    #prev2_frame = signal[blockSize:2*blockSize]
    #for i in range(2*blockSize, len(signal)-blockSize, shiftSize):
    for i in range(0, len(signal)-blockSize, shiftSize):
        frame = signal[i:i+blockSize] * hamming
        feature_vector = list(MFCC(frame))
        # 1st derivative (finite differences)
        #feature_vector.extend(list(MFCC(frame - prev_frame)))
        # 2nd derivative
        #feature_vector.extend(list(MFCC(frame - 2*prev_frame + prev2_frame)))
        feature_vector.append(rootMeanSquare(frame))
        feature_vector.append(zeroCrossingRate(frame))
        vectors.append(numpy.array(feature_vector))
        #prev2_frame = prev_frame
        #prev_frame = frame

    vectors = numpy.array(vectors)
    return featureScaleVectors(vectors, vectors.shape[1]-2, vectors.shape[1])
