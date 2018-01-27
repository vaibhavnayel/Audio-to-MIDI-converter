
from scipy.fftpack import fft,ifft
from scipy.io import wavfile
import numpy as np 
from matplotlib.pyplot import *
from scipy.signal import spectrogram
from peakdetect import detect_peaks
from scipy.signal import get_window


notes = dict({
	55:"(LOW)",
	65.41:"C2",
	69.3:"C#2",
	73.42:"D2",
	77.78:"D#2",
	82.41:"E2",
	87.31:"F2",
	92.5:"F#2",
	98:"G2",
	103.83:"G#2",
	110:"A2",
	116.54:"A#2",
	123.47:"B2",
	130.81:"C3",
	138.59:"C#3",
	146.83:"D3",
	155.56:"D#3",
	164.81:"E3",
	174.61:"F3",
	185:"F#3",
	196:"G3",
	207.65:"G#3",
	220:"A3",
	233.08:"A#3",
	246.94:"B3",
	261.63:"C4",
	277.18:"C#4",
	293.66:"D4",
	311.13:"D#4",
	329.63:"E4",
	349.23:"F4",
	369.99:"F#4",
	392:"G4",
	415.3:"G#4",
	440:"A4",
	466.16:"A#4",
	493.88:"B4",
	523.25:"C5",
	554.37:"C#5",
	587.33:"D5",
	622.25:"D#5",
	659.26:"E5",
	698.46:"F5",
	739.99:"F#5",
	783.99:"G5",
	830.61:"G#5",
	880:"A5",
	932.33:"A#5",
	987.77:"B5",
	1046.5:"C6",
	1108.7:"C#6",
	1174.7:"D6",
	1244.5:"D#6",
	1318.5:"E6",
	1400:"(HIGH)"
	})

def find_closest_note(freq):
    dist = 99999
    result = ""
    for i in notes.keys():
        newDist = abs(freq-i)
        if newDist<dist:
            dist = newDist
            result = notes[i]
            key=i
    return result,key


samplerate, data  = wavfile.read('synth.wav')
data=np.average(data,axis=1)

'''
f=fft(data[2048:4096])
plot(20*np.log10(abs(f)))
show()
'''

def normalize_volume(stream,window_size):
	l=len(stream)
	peak=max(stream)
	new_stream=np.zeros(l)
	window=get_window('blackman',window_size)
	avg=np.average(abs(data))/4
	for i in range((window_size-1)/2,l-((window_size-1)/2)):
		local_avg=np.average(abs(stream[i-((window_size-1)/2):i+((window_size-1)/2)+1]),weights=window)
		#if local_avg==0 : break
		new_stream[i]=stream[i]*avg/local_avg
		if i%10000==0: print i
	return new_stream

n=normalize_volume(data,129)
wavfile.write('scaled.wav',samplerate,n)

f, t, Sxx = spectrogram(data, samplerate,nperseg=2048,noverlap=2048/4,nfft=2048,window='blackman')
subplot(321)
pcolormesh(t, f[:], np.log10(Sxx[:,:]))


cep=20*np.log10(abs(ifft(20*np.log10(Sxx),axis=0)))[:Sxx.shape[0]/2,:]
subplot(322)
pcolormesh(cep)

subplot(323)
plot(abs(cep[:,200]))
#plot(20*np.log10(Sxx[:,200]))
#plot(abs(cep[:,90]))
#plot(abs(cep[:,60]))

subplot(324)
plot(abs(cep[:,300]))
#plot(20*np.log10(Sxx[:,300]))

subplot(325)
plot(abs(cep[:,400]))
#plot(20*np.log10(Sxx[:,400]))
show()
frequencies=[]
notes_played=[]
'''
for i in range(Sxx.shape[1]):
	peaks=detect_peaks(Sxx[:,i], mph=0.002, mpd=20, show=False)
	if peaks.size>0:
		fundamental=f[peaks[0]]
		note,fundamental=find_closest_note(fundamental)
		frequencies.append(fundamental)
		notes_played.append(note)
	else:
		frequencies.append(0)
		notes_played.append('(LOW)')

plot(frequencies)
show()
'''


	   
