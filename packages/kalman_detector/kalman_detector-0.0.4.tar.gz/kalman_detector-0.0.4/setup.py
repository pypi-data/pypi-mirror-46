#!/usr/bin/env python

from distutils.core import setup

setup(name='kalman_detector',
      version='0.0.4',
      description='Detect radio bursts with variying intensity',
      long_description='''This module implements the kalman detector score along with the equivalent cumulative fourier
       score. Score is designed to receive X(f), a sequence of "amplitudes" (where f is an arbitrary indexed parameter)
       and decide between: 
       H0: X(f) = N(f)  pure gaussian noise
       H1: X(f) = A(f) + N(f) where A(f) is a smooth gaussian field with a low-pass power spectra where the smoothness parameter
       unknown. 
       Was originally written for detecting Fast Radio Bursts, but can be used to many other types of signals including 
       AGN light curves. 
       If used for scientific publication, please write to bzackay@gmail.com for citing information 
       (paper would be out soon)''',
      author='Barak Zackay',
      author_email='bzackay@gmail.com',
      url='https://bitbucket.org/bzackay/kalman_detector',
      packages=['kalman_detector'],
      requires=['numpy', 'scipy', 'numba', 'matplotlib'])
