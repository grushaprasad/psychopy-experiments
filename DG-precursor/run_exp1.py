from psychopy import info, event, visual, core, data, logging, gui, sound

from psychopy.sound import Sound
print(sound.Sound)


import glob, random, re, numpy, subprocess, sys

part_id = 'grusha_test01'

dataFilename = './data/DGcontext_Exp1%s.csv'%part_id
stimFile_block1 = 'exp1_block1_stimlist.csv'
stimFile_block2 = 'exp1_block2_stimlist.csv'



dataFile = open(dataFilename,'w')
dataFile.write(','.join(['part_id','target_fname','cond', 'trial_id','response','\n']))
dataFile.close()


## EXPERIMENT CODE

def playSound(soundFile):  
    #soundx = sound.backend_pygame.SoundPygame(soundFile)
    #soundx = sound.SoundPygame(soundFile)
    print(soundFile)
    soundx = sound.Sound(soundFile)
    dur = soundx.getDuration()
    soundx.setVolume(1.0)
    soundx.play()
    core.wait(dur)

def waitResp():
    event.clearEvents('keyboard')
    while True:
        keys = event.getKeys()
        if 'z' in keys: return('D')
        if 'm' in keys: return('G')
        if 'q' in keys: core.quit()

def waitPress():
    event.clearEvents('keyboard')
    while True:
        keys = event.getKeys()
        if 'space' in keys: break
        if 'q' in keys: core.quit()

def runTrial(trial, trial_id, block=1):
    stim = trial['stim_fname']
    if block == 2:
        fname = trial['target_fname']
        cond = trial['condition']

    myWin.flip()
    core.wait(0.500)

    message.setText(trial_instructions)
    message.draw()
    myWin.flip()
    core.wait(1.00)

    # present auditory stimulus
    playSound(stim)
    
    response = waitResp()

    # save response to file
    dataFile = open(dataFilename,'a')
    if block == 1:
        trial_info = [part_id, stim, 'block1', trial_id, response]
    else:
        trial_info = [part_id, fname, cond, trial_id, response]

    dataFile.write(','.join([str(x) for x in trial_info]) +'\n')
    dataFile.close()

def runPracticeTrial():
    message.setText(trial_instructions)
    message.draw()
    myWin.flip()
    core.wait(1.00)
    
    playSound('./target_stims/a_dg18_CV.wav')
    response = waitResp()   # Not recording the practice data. Do I need to?
    
    message.setText(trial_instructions)
    message.draw()
    myWin.flip()
    core.wait(1.00)
    
    playSound('./target_stims/a_dg05_CV.wav')
    response = waitResp()
    
    

# # # # # # # #
#initialize display
computer = ('Mac', 'PC', 'soundbooth')[2]
if computer=='Mac':
    #myWin = visual.Window(size=(1024,768), pos=(0,0), fullscr=False, allowGUI=True, monitor='testMonitor', units='cm', color='whitesmoke', useRetina=True)
    myWin = visual.Window(size=(1400,768), fullscr=False, allowGUI=True, monitor='testMonitor', units='cm', color='whitesmoke')
    message = visual.TextStim(myWin, text="", pos=(0,6), height=1.0, color='black', wrapWidth=30, alignVert='top')
elif computer=='PC':
    myWin = visual.Window(size=(1024,768), pos=(0,0), fullscr=False, allowGUI=True, monitor='testMonitor', units='cm', color='whitesmoke')
    message = visual.TextStim(myWin, text="", pos=(0,6), height=0.8, color='black', wrapWidth=30, alignVert='top')
else:
    myWin = visual.Window(size=(1400,768), fullscr=True, allowGUI=True, monitor='testMonitor', units='cm', color='whitesmoke')
    message = visual.TextStim(myWin, text="", pos=(0,5), height=0.7, color='black', wrapWidth=25, alignVert='top')


trial_instructions = "If you hear a \"d\" at the beginning of the syllable, press the yellow key. If you hear a \"d\" at the beginning of the syllable, press the blue key. "

message.setText("Welcome! There are two parts to this experiment. In the first part, you will hear a\
syllable and decide what consonant it begins with. If you hear a \"d\" at the beginning of the syllable, \
press the yellow key (on the left). If you hear a \"g\", press the blue key (on the right).\n\n\
The second part of the experiment works exactly the same way, except that you will hear a short sequence \
of tones prior to each syllable. (You will still decide whether the beginning consonant is \"d\" or \"g\").")

message.draw()
myWin.flip()
waitPress()

message.setText("Here are some practice trials. Press the space bar when you are ready to start.")
message.draw()
myWin.flip()
waitPress()

runPracticeTrial()

message.setText("Do you have any questions?\n Press the space bar when you are ready to start the first part of the experiment.")
message.draw()
myWin.flip()
waitPress()


trials_block1 = data.TrialHandler(nReps=1,method='random',dataTypes=None,extraInfo=None,seed=None,trialList=data.importConditions(stimFile_block1))

for i,trial in enumerate(trials_block1):
    runTrial(trial, i)

message.setText("You are done with the first part of the experiment!\n\n\
As a reminder, in the second part you will hear a sequence of tones before \
the syllable, but your task is still the same. Press the yellow key if you hear \
\"d\" and the green key if you hear \"g\".")
message.draw()
myWin.flip()
waitPress()


trials_block2 = data.TrialHandler(nReps=1,method='random',dataTypes=None,extraInfo=None,seed=None,trialList=data.importConditions(stimFile_block2))

for i,trial in enumerate(trials_block2):
    runTrial(trial, i, block=2)

message.setText("You are done with the experiment! Thank you for participating.")
message.draw()
myWin.flip()
waitPress()