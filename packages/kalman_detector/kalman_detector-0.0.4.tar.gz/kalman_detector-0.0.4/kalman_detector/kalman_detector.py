import numpy as np
import scipy.stats

# If numba does not exist, replace jit by an empty decorator
try:
    from numba import jit
except ImportError:
    print("Warning: Numba is not found. Kalman code would be much slower")
    def jit(func, *args, **kwargs):
        return func

VERBOSE = False

def _pdb(*message):
    if VERBOSE:
        print(message)

def kalman_significance(spec, spec_std, sig_ts=[], coeffs=[]):
    """
    Calculates the kalman significance for given 1d spec and per-channel error.


    :param spec: 1d numpy array with the spectrum of the candidate burst.
    :param spec_std: numpy array with the estimated per-channel std.
    :param sig_ts: list of trial transition probabilities to be used. if non is given,
           [0.3, 0.1, 0.03, 0.01] is used
    :param coeffs: coefficients for the tail distribution of the kalman detector.
    If no coeffs input, it will calculate with random number generation.
    :return:
    """


    if not len(sig_ts):
        sig_ts = [x*np.median(spec_std) for x in [3, 1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]]
    if not len(coeffs):
        sig_ts, coeffs = kalman_prepare_coeffs(spec_std, sig_ts)

    assert len(sig_ts) == len(coeffs)

    _pdb("Calculating max Kalman significance for {0} channel spectrum".format(len(spec)))

    significances = []
    for i, sig_t in enumerate(sig_ts):
        score = kalman_filter_detector(spec, spec_std, sig_t)
        coeff = coeffs[i]
        x_coeff, const_coeff = coeff
        significances.append(x_coeff * score + const_coeff)

    # return prob in units of nats = ln(P(D|H1)/P(D|H0)). ignore negative probs
    return -max(0, np.max(significances) * np.log(2))


@jit(nopython=True)
def kalman_filter_detector(spec, spec_std, sig_t, amp_0=0., sig_0=None):
    """
    Core calculation of Kalman estimator of input 1d spectrum data.
    spec/spec_std are 1d spectra in same units.
    sig_t sets the smoothness scale of model (A) change.
    Number of changes is sqrt(nchan)*sig_t/mean(spec_std).
    Frequency scale is 1/sig_t**2
    A_0/sig_0 are initial guesses of model value in first channel.
    Returns score, which is the likelihood of presence of signal.

    :param spec:
    :param spec_std:
    :param sig_t:
    :param amp_0:
    :param sig_0:
    :return:
    """

    # likelihood calc expects zero mean spec
    specmean = 0.
    nonzero = 0
    for i in range(len(spec)):
        specmean += spec[i]
        if spec[i] != 0.:
            nonzero += 1
    if nonzero:
        specmean /= nonzero
    for i in range(len(spec)):
        if spec[i] != 0.:
            spec[i] -= specmean

    if sig_0 is None:
        sig_0 = np.median(spec_std)

    cur_mu, cur_state_v = amp_0, sig_0 ** 2
    cur_log_l = 0.
    H_0_log_likelihood = 0.
    for i in range(len(spec)):
        if (spec[i] != 0.) and (spec_std[i] != 0.):
            cur_z = spec[i]
            cur_spec_v = spec_std[i]**2
            # computing consistency with the data
            cur_log_l += -(cur_z-cur_mu)**2 / (cur_state_v + cur_spec_v + sig_t**2)/2 - \
                         0.5*np.log(2*np.pi*(cur_state_v + cur_spec_v + sig_t**2))

            # computing the best state estimate
            cur_mu = (cur_mu / cur_state_v + cur_z/cur_spec_v) / (1/cur_state_v + 1/cur_spec_v)
            cur_state_v = cur_spec_v * cur_state_v / (cur_spec_v + cur_state_v) + sig_t**2
            H_0_log_likelihood += -(spec[i]*spec[i] / (spec_std[i]*spec_std[i]) / 2) - 0.5*np.log(2*np.pi * spec_std[i]*spec_std[i])
            
    return cur_log_l - H_0_log_likelihood



def kalman_prepare_coeffs(spec_std, sig_ts=None, n_trial=10000):
    """
    Measure kalman significance distribution in pure gaussian noise random data.
    Will measure the coefficients of the exponential tail of the distribution.
    If a list of sig_t is given, it returns the coefficients for each individual sig_t

    :param spec_std: 1d per-channel standard deviation to be used.
                     Zeros will be flagged. Best for zeros to be
                     similar to those of real spectrum to be used.
    :param sig_ts: Transition std for the intrinsic markov process.
                   Can be single float or list of values.
    :param n_trial: number of gaussian noise instances to be used.
    :return: tuple (sig_ts, coeffs)
    """

    # Are spec_std values ok?
    if not np.any(spec_std):
        _pdb("spectrum std all zeros. Not estimating coeffs.")
        return sig_ts, []
#    elif len(np.where(spec_std == 0.)[0]) > 0:
#        _pdb("Replacing {0} noise spectrum channels with median noise".format(len(np.where(spec_std == 0.)[0])))
#        spec_std = np.where(spec_std == 0, np.median(spec_std), spec_std)

    # ignore zeros, as is done in detector function for real data
    spec_std = spec_std[np.where(spec_std != 0.)]

    # calculate sig_ts
    if sig_ts is None:
        sig_ts = np.array([x*np.median(spec_std) for x in [0.3, 0.1, 0.03, 0.01]])
    elif isinstance(sig_ts, float):
        sig_ts = np.array([sig_ts])
    elif isinstance(sig_ts, list):
        sig_ts = np.array(sig_ts)
    else:
        _pdb("Not sure what to do with sig_ts {0}".format(sig_ts))

    assert isinstance(sig_ts, np.ndarray)

    if not np.all(np.nan_to_num(sig_ts)):
        print("sig_ts are nans. Not estimating coeffs.")
        return sig_ts, []

    _pdb("Measuring Kalman significance distribution for sig_ts {0}".format(sig_ts))

    coeffs = []
    for sig_t in sig_ts:
        n_channels = len(spec_std)
        random_scores = []
        for i in range(n_trial):
            random_spec = np.random.normal(0, spec_std, size=n_channels)
            random_spec -= random_spec.mean()
            random_scores.append(kalman_filter_detector(random_spec, spec_std, sig_t))

        # Approximating the tail of the distribution as an  exponential tail (probably is justified)
        coeffs.append(np.polyfit([np.percentile(random_scores, 100 * (1 - 2 ** (-i))) for i in range(3, 10)],
                                 range(3, 10), 1))

    return sig_ts, coeffs

def get_matched_filtered_spectra(data, start_ind, end_ind):

    # Avg energies:
    avg = data[start_ind:end_ind, :].sum(axis=-1) / data.shape[-1]
    return np.dot(data[start_ind:end_ind, :], avg)


def get_best_start_end_indices_and_significance(data, max_burst_width_ind):

    chi2_arr = data.sum(axis=-1)/data.std(axis=-1)**2

    best_significance = 0
    best_start_ind = None
    best_end_ind = None
    cumsum_chi2 = np.cumsum(chi2_arr)
    for start_ind in range(len(chi2_arr)):
        for end_ind in range(start_ind,min(len(chi2_arr),start_ind + max_burst_width_ind)):
            N_dof = end_ind - start_ind
            score = cumsum_chi2[end_ind] - cumsum_chi2[start_ind]
            significance = -scipy.stats.chi2.logsf(score, N_dof)

            if significance >= best_significance:
                best_start_ind = start_ind
                best_end_ind = end_ind
                best_significance = significance

    return best_start_ind, best_end_ind, significance


def secondary_spectrum_cumulative_chi2_score(sig):
    """
    Would compute the cumulative-chi2 test statistic on sig.
    Assumes the signal is composed of i.i.d N(E,1) variables ($E$ would be ignored)
    Would return the following statistical test between:
    H0: sig(f) ~ N(E,1)
    H1: sig(f) ~ N(E,1) + FRB with A(f) that have secondary spectrum (DFT(A(f)) with freq cutoff ff0

    :param sig: vector of measured A(f) of the candidate FRB
    :return: significance = max_f0 of ln(P(sig|H1,ff0)/P(sig|H0))
    """

    fsig = np.abs(np.fft.rfft(sig))**2

    score_arr = np.cumsum(fsig[1:]/(len(sig)/2))
    significance_arr = np.zeros_like(score_arr)
    for ind,score in enumerate(score_arr):
        significance_arr[ind] = scipy.stats.chi2.logsf(score, 2*(ind+1))

    if np.max(-significance_arr) == np.inf:
        print(score_arr[:25])
    return np.max(-significance_arr)



def compare_statistics_freq_time(data, boxcar_width=None, kalman_transition_sigma_list=[], n_random=10000, add_noise=True,
                         verbose = False):
    """
    This function would compute:
        the best boxcar snr for the input data.
        the significance you get with the kalman score.
        the significance you get with the cumulative chi2 score.

    :param data: 2d array, [freq, time] in units of power. Assumed dedispersed and calibrated
    :param boxcar_width: size of boxcar to use. would be automatically determined if None.
    :param kalman_transition_sigma_list: trial stds to try with the Kalman filter empty list would auto-choose.
    :param n_random: numnber of random monte-carlo kalman operations to do for the coeffs.
    :param add_noise: in order to quantify importance, you can feed with an FRB, turn this flag, and
                      random noise would be added to put the signal at snr=8.
    :return: snr_best_boxcar, snr_total_kalman, snr_cumulative_chi2
    """
    EPS = 1e-10
    data_new = data[:] - np.mean(data, axis=1)[:, None]
    if boxcar_width is None:
        data_tmp = np.zeros(data_new.shape)
        snr_best = 0
        boxcar_width = 0
        for i in range(50):
            data_tmp += np.roll(data_new,i, axis=1)
            channel_stds = np.std(data_tmp, axis=1) + EPS
            snr_sequence = np.sum(data_tmp / (channel_stds ** 2)[:, None], axis=0) / np.sum(
                1 / channel_stds[channel_stds>EPS] ** 2) ** 0.5
            event_snr = np.max(snr_sequence)
            if event_snr >= snr_best:
                snr_best = event_snr
                boxcar_width = i+1
        if verbose:
            print(f"Chosen boxcar width:{boxcar_width+1}")


    data_new = np.sum([np.roll(data,i,axis=1) for i in range(boxcar_width)], axis=0)


    channel_stds = np.std(data_new, axis=1) + EPS


    channel_means_repeated = np.mean(data_new, axis=1).repeat(len(data_new[0])).reshape(data_new.shape)
    print(channel_means_repeated.shape)
    data_new = data_new - np.mean(data_new, axis=1)[:, None]
    # Inverse variance detection of the
    MIN_STD = 0.5 * np.median(channel_stds)
    snr_sequence = np.sum((data_new/(channel_stds**2)[:,None])[channel_stds>MIN_STD],axis=0) / np.sum(1/channel_stds[channel_stds>MIN_STD]**2)**0.5

    good_ind = np.argmax(snr_sequence)
    snr_best = snr_sequence[good_ind]

    if verbose:
        print(f"Inverse variance weighting detection SNR: {snr_best}")
    on_spectra = data_new[channel_stds>MIN_STD, good_ind]
    channel_stds = channel_stds[channel_stds>MIN_STD]


    if add_noise:
        # Adding noise to the on-time so that the SNR apparent to the alg would be exactly 6
        target_snr = 8
        current_variance = np.sum(channel_stds**2)/len(channel_stds)
        needed_std = ((snr_best**2 - target_snr**2)*current_variance/target_snr**2)**0.5
        on_spectra += np.random.normal(0,needed_std,len(on_spectra))
        channel_stds = (channel_stds**2 + needed_std**2)**0.5
        snr_best = np.sum(on_spectra) / (np.sum(channel_stds ** 2)) ** 0.5
        if verbose:
            print(f"SNR after adding noise: {snr_best}")

    on_spectra = on_spectra - np.mean(on_spectra)

    kalman_transition_sigma_list, coeffs = kalman_prepare_coeffs(channel_stds, kalman_transition_sigma_list, n_random)
    significance_secondary_spectrum_score = secondary_spectrum_cumulative_chi2_score((on_spectra / channel_stds))
    significance_kalman = kalman_significance(on_spectra, channel_stds, sig_ts=kalman_transition_sigma_list,
                                              coeffs=coeffs)

    significance_orig = scipy.stats.norm.logsf(snr_best)
    if verbose:
        print(f"Significance orig: {-significance_orig}")
        print(f"Significance kalman: {-significance_kalman}")
        print(f"Significance_fourier_domain_score: {significance_secondary_spectrum_score}")
    total_logsf_kalman = significance_orig + significance_kalman
    total_logsf_freq_domain = significance_orig + (-significance_secondary_spectrum_score)
    if np.abs(total_logsf_kalman) > 600:
        # isf function returns bad results if we try to feed it with np.exp(-600) and beyond.
        # this is because the double epsilon is reached. Needless to say, at this point the exact significance
        # does not mean anything. In this case, we return a good approximation for S/N
        return (snr_best, np.abs(2 * total_logsf_freq_domain - np.log(np.abs(2 * total_logsf_freq_domain))) ** 0.5,
                              np.abs(2 * total_logsf_freq_domain - np.log(np.abs(2 * total_logsf_freq_domain))) ** 0.5)
    snr_total_kalman = scipy.stats.norm.isf(np.exp(total_logsf_kalman))
    snr_kalman_fourier = scipy.stats.norm.isf(np.exp(total_logsf_freq_domain))
    return snr_best, snr_total_kalman, snr_kalman_fourier



#TODO: Add the boxcar determination to this function too.
#TODO: Perhaps use the above 2d function on the pol contracted data.
def examine_candidate_time_freq_pol(data, on_ind, off_inds, sig_ts=[], n_random=10000):
    """
    Go from 3d data array (time, freq, pol)  to kalman significance.
    This function would do all the required process and would serve as an example for using the module.
    Calculates coefficients from data and then adds significance to current snr.

    :param data: a 3d array, (time, freq, pol)
    :param on_ind: index to the "on-pulse" time.
    :param off_inds: index to many "off-pulse" indices that reflect the std of all channels at the burst location.
    :param sig_ts: transition probabilities to be used. if nothing is passed the default is used
    :param n_random: number of random instances to be used in measuring the tail of the kalman detector's distribution
    :return:
    """

    spec_std = data.mean(axis=2).take(off_inds, axis=0).std(axis=0)
    spec_mean = data.mean(axis=2).take(off_inds, axis=0).mean(axis=0)

    # making sure the expected value of the spec is zero.
    spec = data.mean(axis=2)[on_ind] - spec_mean

    sig_ts, coeffs = kalman_prepare_coeffs(spec_std, sig_ts, n_random)
    significance_kalman = kalman_significance(spec, spec_std, sig_ts=sig_ts,
                                              coeffs=coeffs)

    existing_inds = np.nonzero(spec_std)

    snr_orig = np.sum(spec[existing_inds]/spec_std[existing_inds]**2)/np.sum(1/spec_std[existing_inds]**2)**0.5

    significance_orig = scipy.stats.norm.logsf(snr_orig)
    total_logsf = significance_orig + significance_kalman
    if np.abs(total_logsf) > 600:
        # isf function returns bad results if we try to feed it with np.exp(-600) and beyond.
        # this is because the double epsilon is reached. Needless to say, at this point the exact significance
        # does not mean anything. In this case, we return a good approximation for S/N
        return np.abs(2*total_logsf - np.log(np.abs(2*total_logsf)))**0.5
    snr_total = scipy.stats.norm.isf(np.exp(total_logsf))
    return snr_total


