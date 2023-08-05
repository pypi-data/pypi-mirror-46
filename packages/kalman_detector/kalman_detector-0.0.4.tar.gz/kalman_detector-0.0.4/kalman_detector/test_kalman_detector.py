import unittest
import numpy as np
import scipy.stats
import kalman_detector
from matplotlib import pyplot as plt
import glob



class TestKalmanDetector(unittest.TestCase):


    def test_sensitivity_up_down(self):

        A = np.concatenate([np.concatenate([np.ones(10), np.zeros(10)]) for i in range(40)])
        std_vec = np.sin(0.1*np.arange(len(A))) + 2

        optimal_snr = np.sum(A**2/std_vec**2)**0.5

        snr_sum = np.sum(A/std_vec**2) / np.sum(1/std_vec**2)**0.5
        print("expected significance naive:", scipy.stats.norm.logsf(snr_sum))
        print("optimal_snr:", optimal_snr)

        sig_ts, coeffs = kalman_detector.kalman_detector.kalman_prepare_coeffs(std_vec, n_trial = 10000)

        sig_kalman = []
        sig_naive = []


        for i in range(1000):
            noise = np.random.normal(0,std_vec)
            signal = A+noise
            snr_naive = np.sum(signal/std_vec**2) / np.sum(1/std_vec**2)**0.5
            sig_naive.append(scipy.stats.norm.logsf(snr_naive))
            sig_kalman.append(kalman_detector.kalman_detector.kalman_significance(signal, std_vec, sig_ts, coeffs))

        fig = plt.figure()
        ax = plt.gca()
        ax.hist(sig_naive, 30)
        ax.hist(sig_kalman, 30)

        fig2 = plt.figure()
        ax2 = plt.gca()
        ax2.hist((np.array(sig_naive) + np.array(sig_kalman))/scipy.stats.norm.logsf(optimal_snr),30)

    def test_sin(self):

        A = np.abs((1.5+np.sum([np.random.random()*np.sin(np.random.random()*2*np.pi+np.random.random()*np.arange(400)/4) for i in range(4)],axis=0))*0.6)
        std_vec = np.sin(0.1 * np.arange(len(A))) + 2

        optimal_snr = np.sum(A ** 2 / std_vec ** 2) ** 0.5

        snr_sum = np.sum(A / std_vec ** 2) / np.sum(1 / std_vec ** 2) ** 0.5
        print("expected significance naive:", scipy.stats.norm.logsf(snr_sum))
        print("optimal significance:", scipy.stats.norm.logsf(optimal_snr))

        sig_ts, coeffs = kalman_detector.kalman_detector.kalman_prepare_coeffs(std_vec,[10,3,1,0.3,0.1,0.03,0.01,0.003,0.001], n_trial=100000)

        sig_kalman = []
        sig_naive = []
        optimal_sig_list = []

        for i in range(1000):
            noise = np.random.normal(0, std_vec)
            signal = A + noise
            snr_naive = np.sum(signal / std_vec ** 2) / np.sum(1 / std_vec ** 2) ** 0.5
            sig_naive.append(scipy.stats.norm.logsf(snr_naive))
            optimal_sig_list.append(scipy.stats.norm.logsf(
                np.sum(A*signal/std_vec**2)/ np.sum(A**2 / std_vec ** 2) ** 0.5))
            sig_kalman.append(kalman_detector.kalman_detector.kalman_significance(signal, std_vec, sig_ts, coeffs))

        fig = plt.figure()
        ax = plt.gca()
        ax.hist(sig_naive, 30)
        ax.hist(sig_kalman, 30)

        fig2 = plt.figure()
        ax2 = plt.gca()
        ax2.hist((np.array(sig_naive) + np.array(sig_kalman)) / np.array(optimal_sig_list), 30)
        ax2.hist((np.array(sig_naive)) / np.array(optimal_sig_list), 30)










