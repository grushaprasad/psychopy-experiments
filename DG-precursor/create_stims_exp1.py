#from psychopy import visual, event, core, data, logging, gui, info  #NOTE the order of the import matters
#from psychopy import prefs
#prefs.hardware['audioLib'] = ['pygame']
#from psychopy import sound

#print(sound.Sound)

import librosa, random, subprocess, sys, glob, re, csv
import numpy as np

soundfile_path = './stim/'
stim_files = ['a_dg08_CV.wav', 'a_dg09_CV.wav', 'a_dg10_CV.wav', 'a_dg11_CV.wav', 'a_dg12_CV.wav']

offset = 0.098 
duration = 0.365

rms_target = 0.06362659 # average of Stephens & Holt 2011 synthetic stimuli


# parameters of the 
sil_dur = 45

standard_freq = 2300.0 # standard tone at 2300 Hz
tone_dur = 70.0/1000.0 # 70 ms duration for each tone
isi_dur = 30.0/1000.0 # 30 ms silence between successive tones
sil_dur = 50.0/1000.0 # 50 ms silence between standard tone and speech
ramp_dur = 5.0/1000.0
sr = 11025
#sr = 10000
#tone_length = tone_dur/



# Experiment parameters
num_conds = 4
num_trials_per_cond = 10



## STIMULI CODE
def rms_amplitude(x):
    rms = np.sqrt(np.mean(x**2.0))
    return rms

def scale_rms(x, rms_target):
    rms_x = rms_amplitude(x)
    s = (rms_target / rms_x)
    y = s*x
    return y

#speech_dga, speech_sr = librosa.core.load('./stim/a_dg11_CV.wav', sr=None)


# Reading in the stimuli
dg_stims = [0] * len(stim_files)


for i,stim in enumerate(stim_files):
    curr_file = soundfile_path+stim
    curr_dga, curr_sr = librosa.core.load(curr_file, sr = sr, offset = offset, duration = duration)  #if I don't have sr, the sr becomes 22050. Why?
    dg_stims[i] = (curr_dga, stim)


dg_stims = dg_stims*num_conds*num_trials_per_cond


# Creating precursor tones
low = np.arange(800.0, 1800.0+100.0, 100.0) # mean 1300
mid = np.arange(1800.0, 2800.0+100.0, 100.0) # mean 2300
high = np.arange(2800.0, 3800.0+100.0, 100.0) # mean 3300

def create_precursor_freqs(l1,l2):
    np.random.shuffle(l1)
    np.random.shuffle(l2)
    return(np.concatenate((l1, l2),0))

def create_precursors(l, tone_sr, tone_dur):   
    linear_ramp = np.linspace(0.0, 1.0, int(ramp_dur*tone_sr))
    mask = np.ones(int((tone_dur - 2.0*ramp_dur)*tone_sr))
    mask = np.concatenate((linear_ramp, mask, linear_ramp[::-1]))
    standard_tone = mask*librosa.core.tone(standard_freq, tone_sr, duration=tone_dur)[0:771] 


    sil = np.zeros(int(sil_dur * tone_sr))
    isi = np.zeros(int(isi_dur * tone_sr))

    precursor_list = [0]*len(l)
    for i, item in enumerate(l):

        curr_tones = [mask*librosa.core.tone(freq, tone_sr, duration=tone_dur)[0:771] for freq in item]
        curr_precursor = np.concatenate([np.concatenate((tone, isi)) for tone in curr_tones] + [standard_tone, sil])
        precursor_list[i] = scale_rms(curr_precursor, rms_target)
    return(precursor_list)

lowmid = [create_precursor_freqs(low, mid) for i in range(num_trials_per_cond*len(stim_files))]
midlow = [create_precursor_freqs(mid, low) for i in range(num_trials_per_cond*len(stim_files))]
highmid = [create_precursor_freqs(high, mid) for i in range(num_trials_per_cond*len(stim_files))]
midhigh = [create_precursor_freqs(mid, high) for i in range(num_trials_per_cond*len(stim_files))]

lowmid_precursors = create_precursors(lowmid, sr, tone_dur)
lowmid_precursors = [(item, 'lowmid') for item in lowmid_precursors] 

midlow_precursors = create_precursors(midlow, sr, tone_dur)
midlow_precursors = [(item, 'midlow') for item in midlow_precursors]

highmid_precursors = create_precursors(highmid, sr, tone_dur)
highmid_precursors = [(item, 'highmid') for item in highmid_precursors]

midhigh_precursors = create_precursors(midhigh, sr, tone_dur)
midhigh_precursors = [(item, 'midhigh') for item in midhigh_precursors]


all_precursors = lowmid_precursors + midlow_precursors + highmid_precursors + midhigh_precursors


# Create stims and stim list for block 2

all_stims = [0]*len(all_precursors)

for i, item in enumerate(all_precursors):
    curr_stim = np.concatenate((item[0], dg_stims[i][0]))
    fname = 'dg%s_%s_%s.wav'%(re.findall('\d+', dg_stims[i][1])[0], i+1, item[1])
    fpath = './stims/%s'%fname
    librosa.output.write_wav(fpath, curr_stim, sr=sr)
    all_stims[i] = (fpath, dg_stims[i][1], item[1])

all_stims.insert(0, ['stim_fname', 'target_fname', 'condition'])

with open("exp1_block2_stimlist.csv",'wb') as resultFile:
    wr = csv.writer(resultFile)
    wr.writerows(all_stims)


# Create stim list for block1 


with open("exp1_block1_stimlist.csv",'wb') as resultFile:
    resultFile.write('stim_fname\n')
    for item in stim_files*num_trials_per_cond:
        resultFile.write('./stim/%s\n'%item)








