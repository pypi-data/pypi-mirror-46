import glob
import numpy as np
import scipy.stats
from matplotlib import pyplot as plt
import kalman_detector
import scipy
import sigproc_keith


def analyze_vishal_bursts():
    try:
        files_off = sorted(glob.glob('/Users/bzackay/Dropbox/python/Radio/public/On_Off_spectra/*_off.txt*'))
        files_on = sorted(glob.glob('/Users/bzackay/Dropbox/python/Radio/public/On_Off_spectra/*a.txt*'))

        on_spectra = [list(zip(*[list(map(float, x.split())) for x in open(files_on[i], 'r').readlines()])) for i in
                      range(len(files_on))]
        off_spectra = [list(zip(*[list(map(float, x.split())) for x in open(files_off[i], 'r').readlines()])) for i
                       in
                       range(len(files_off))]

        failed_spectra = []
        improvements = []
        for i in range(len(files_on)):
            frb_signal = on_spectra[i][1] / np.std(off_spectra[i][1])
            n = len(frb_signal)
            snr_naive = np.sum(frb_signal) / np.sqrt(n)
            if snr_naive < 4:
                print("Failed file!!!", files_on[i])
                failed_spectra.append(frb_signal)
                continue
            print('FRB:', files_on[i], ": ")
            significance = scipy.stats.norm.logsf(snr_naive)

            print('SNR:', snr_naive, " significance: ", significance)
            my_improvement = kalman_detector.kalman_detector.kalman_significance(frb_signal - np.mean(frb_signal),
                                                                                 np.ones(len(frb_signal)))
            print('kalman_extra_significance:', my_improvement)
            improvements.append((my_improvement + significance) / significance)

        plt.hist(improvements, 20)
    except FileNotFoundError:
        print("Vishal files not found - If you are not Barak Zackay, this is OK")


def analyze_askap_bursts():
    #%%
    files = glob.glob('/Users/bzackay/Dropbox/from_keith_frb/*/*/*.npy')

    res = []
    for f in files:

            print(f)
            data = np.load(open(f, 'rb'))
            tmp_res = kalman_detector.compare_statistics_freq_time(data, verbose=True)

            res.append(tmp_res)

    #%%


# Loading FRB data provided by Keith Bannister:
def Test_askap_frbs():
    #%%
    frb_names = ['170906','171003','171004','171019','171020','171116']
    directories = ["/Users/bzackay/Downloads/frbcutouts/cutout%s/"%name for name in frb_names]
    beam_nums = [20,12,26,21,0,28]
    dm_estimates = [390.3,463, 304,460.8,114.1,618.5]
    n = 336
    #%%
    #KS = KalmanScorer(n,[0.03,0.1,0.3],1)

    for frb_ind in range(1,len(frb_names)):
        fname = glob.glob(directories[frb_ind]+'*.%02d.fil'%beam_nums[frb_ind])[0]
        dd = load_keith_FRBs(fname,{'dm':dm_estimates[frb_ind]})

        dd /= np.std(dd)
        dd -= np.mean(dd)
        frb_pos = np.argmax(np.mean(dd, 1))
        frb_signal = dd[frb_pos]

        snr_naive = np.sum(frb_signal) / np.sqrt(n)
        print('FRB:',frb_names[frb_ind],": ")
        print('SNR:', snr_naive," significance: ", scipy.stats.norm.logsf(snr_naive))
        my_improvement = kalman_detector.kalman_significance(frb_signal-np.mean(frb_signal),
                                                             np.ones_like(frb_signal), [0.03, 0.1, 0.3])
        print('kalman_extra_significance:', my_improvement)


def load_keith_FRBs(f, values):
    s = sigproc_keith.SigprocFile(f)
    fch1 = s.header['fch1']
    foff = s.header['foff']
    nchan = s.header['nchans']
    tsamp = s.header['tsamp']
    nsamp = 4096
    samp_start = 7000
    # s.seek_sample(samp_start)
    # d = np.fromfile(s.fin, count=nsamp*nchan, dtype=np.uint8)
    # d.shape = nsamp,nchan
    d = s[samp_start:samp_start + nsamp]
    # rescale to roughly 0 mean and 1 variance
    d = d.astype(float)
    d -= 128
    d /= 18.

    assert s.header['nbits'] == 8
    assert s.header['nifs'] == 1
    assert d.shape == (nsamp, nchan)

    dd = roll_dedisperse(d, nchan, fch1, foff, tsamp, values['dm'])
    return dd


def roll_dedisperse(d, nchan, fch1, foff, tsamp, dm):
    dd = d.copy()
    for c in range(nchan):
        f = fch1 + foff * c
        delayms = 4.15 * dm * ((fch1 / 1e3) ** -2 - (f / 1e3) ** -2)
        delaysamp = -int(abs(np.round(delayms / 1e3 / tsamp)))
        dd[:, c] = np.roll(d[:, c], delaysamp)

    return dd


