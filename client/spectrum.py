import sys
import wave #open and read wave files
from struct import unpack #convert the audio data for numpy

import alsaaudio as aa #use to play the audio
import numpy as np #to do calculations as the fft
import scrollphathd as s

def power_index(val):
    #Return the power array index corresponding to a particular frequency.
    return int(2 * chunk * val / sample_rate)

def compute_fft(matrix, data, chunk, sample_rate):
    #global matrix

    # Convert raw sound data to Numpy array
    #print(len(data))
    data = unpack("%dh" % (len(data) / 2), data)
    data = np.array(data, dtype='h')

    # Apply FFT-real data
    fourier = np.fft.rfft(data)
    #Remove last element in array to make it the same size as chunk
    fourier = np.delete(fourier, len(fourier) - 1)
    #Find average 'amplitude' for specific frequency ranges in Hz
    power = np.abs(fourier)
    matrix[0] = int(np.mean(power[power_index(0):power_index(156):1]))
    matrix[1] = int(np.mean(power[power_index(156):power_index(213):1]))
    matrix[2] = int(np.mean(power[power_index(213):power_index(313):1]))
    matrix[3] = int(np.mean(power[power_index(313):power_index(450):1]))
    matrix[4] = int(np.mean(power[power_index(450):power_index(625):1]))
    matrix[5] = int(np.mean(power[power_index(625):power_index(812):1]))
    matrix[6] = int(np.mean(power[power_index(812):power_index(1000):1]))
    matrix[7] = int(np.mean(power[power_index(1000):power_index(1500):1]))
    matrix[8] = int(np.mean(power[power_index(1500):power_index(2000):1]))
    matrix[9] = int(np.mean(power[power_index(2000):power_index(2500):1]))
    matrix[10] = int(np.mean(power[power_index(812):power_index(1000):1]))
    matrix[11] = int(np.mean(power[power_index(625):power_index(812):1]))
    matrix[12] = int(np.mean(power[power_index(450):power_index(625):1]))
    matrix[13] = int(np.mean(power[power_index(313):power_index(450):1]))
    matrix[14] = int(np.mean(power[power_index(213):power_index(313):1]))
    matrix[15] = int(np.mean(power[power_index(156):power_index(213):1]))
    matrix[16] = int(np.mean(power[power_index(0):power_index(156):1]))

    #tidy up column values for the LED matrix
    matrix = np.divide(np.multiply(matrix, weighting), 1000000)
    matrix = matrix.clip(0, s.DISPLAY_HEIGHT)
    matrix = [float(m) for m in matrix]

    return matrix

def spectrum():
    wavfile = wave.open("1.wav", 'r')

    global sample_rate
    sample_rate = wavfile.getframerate()
    global no_channels
    no_channels = wavfile.getnchannels()
    global chunk
    chunk = 4096
    output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL,
                channels = no_channels,
                rate = sample_rate,
                format = aa.PCM_FORMAT_S16_LE,
                periodsize = chunk)
    '''
    output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
    output.setchannels(no_channels)
    output.setrate(sample_rate)
    output.setformat(aa.PCM_FORMAT_S16_LE)
    output.setperiodsize(chunk)
    '''
    global matrix
    matrix  = [0] * s.DISPLAY_WIDTH
    global power
    power = []
    # weighting using an altered Fibonacci sequence
    global weighting
    weighting = [1, 2, 8, 13, 21, 89, 144, 233, 377, 233, 144,89, 21,13, 8, 2, 1 ]
    s.set_brightness(0.75)
    s.rotate(degrees=180)

    data = wavfile.readframes(chunk)

    while len(data) != 0:
        output.write(data)
        matrix = compute_fft(matrix, data, chunk, sample_rate)
        s.set_graph(matrix, 0, s.DISPLAY_HEIGHT)
        s.show()
        data = wavfile.readframes(chunk)

#spectrum()
