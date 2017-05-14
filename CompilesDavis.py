'''
▒█▀▀█ █▀▀█ █▀▄▀█ █▀▀█ ░▀░ █░░ █▀▀ █▀▀ 　 ▒█▀▀▄ █▀▀█ ▀█░█▀ ░▀░ █▀▀ 
▒█░░░ █░░█ █░▀░█ █░░█ ▀█▀ █░░ █▀▀ ▀▀█ 　 ▒█░▒█ █▄▄█ ░█▄█░ ▀█▀ ▀▀█ 
▒█▄▄█ ▀▀▀▀ ▀░░░▀ █▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ 　 ▒█▄▄▀ ▀░░▀ ░░▀░░ ▀▀▀ ▀▀▀ 

Jordan Reichgut
Mentor: Arman Hezarkhani
15-112 Term Project
Spring 2017
'''

from music21 import *
import random, string

def makeMelody(changes, numChoruses, numMeasures):
    changes *= numChoruses

    measureLength = 8
    data = [] # 2D list of measures

    # make list of measures
    for chord in changes:
        root = findRoot(chord)
        chordType = findChordType(chord)
        scale = makeScale(chord)
        chordTones = findChordTones(root, chordType)
        measure = createMeasure(scale, [], chordTones) # constructed recursively
        data.append(measure)

    # algorithms to make the music sound more human
    for i in range(len(data)+1):
        if i > 0:
            root = findRoot(changes[i-1])
            chordType = findChordType(changes[i-1])
            scale = makeScale(changes[i-1])
            chordTones = findChordTones(root, chordType)

        # every 4th measure ends on a chord tone
        if (i+1) % 4 == 0:
            data[i][-1] = (random.choice(chordTones), data[i][-1][1])

        # replace measure's first note with chord tone
        if data[i-1][0][0] not in chordTones:
            data[i-1][0] = (random.choice(chordTones), data[i-1][0][1])

        # diminished & half diminished measures - only chord tones
        if i > 0 and findChordType(changes[i-1]) in ['dim','halfDim']:
            for j in range(len(data[i-1])): # len(measure)
                data[i-1][j] = (random.choice(chordTones), data[i-1][j][1])

        # for min7 measures, leading tone is always followed by the root
        if i > 0 and findChordType(changes[i-1]) == 'min7': 
            for j in range(len(data[i-1])): # len(measure)
                if data[i-1][j][0] == scale[7] and j != len(data[i-1]) - 1:
                    data[i-1][j] = (scale[8], data[i-1][j][1])
                elif data[i-1][j][0] == scale[7] and j == len(data[i-1]) - 1:
                    data[i-1][j] = (scale[8], data[i-1][j][1])

    part = stream.Part()

    for measure in data: 
        # replace 'b' with '-' for Music21 notation
        for i in range(len(measure)):
            if 'b' in measure[i][0]: # measure[i] = note tuple
                measure[i] = (measure[i][0].replace('b', '-'), measure[i][1])
        m = stream.Measure()
        for (pitch, dur) in measure:
            if pitch == 'rest':
                n = note.Rest(pitch)
            else:
                n = note.Note(pitch)
            n.duration.type = dur # music21 duration notation
            m.append(n)
        part.append(m)

    part.show() 

def createMeasure(scale, measure, chordTones):
    x = random.random()
    
    if x <= 0.85:
        noteType, noteValue = random.choice([('quarter', 2), ('eighth', 1)])
    else:
        noteType, noteValue = ('half', 4)

    pitch = random.choice(chordTones)
    measure.append((pitch, noteType))
    measure = measureHelper(measure, scale, pitch, noteType)

    # 80% chance of an 8th note being followed by another 8th note
    for i in range(len(measure)-1):
        if measure[i][1] == 'eighth':
            x = random.random()
            if x < 0.8:
                measure[i+1] = (measure[i+1][0], 'eighth')

    # get measureValue to check length
    measureValue = 0
    measureVals = {'eighth':1, 'quarter':2, 'half':4}
    for c in measure:
        measureValue += measureVals[c[1]]

    # adjust measure length if != 8
    if measureValue > 8:
        while measureValue > 8:
            for i in range(len(measure)-1, 0, -1): # iterate backwards
                if measureValue > 9:
                    if measure[i][-1] == 'half':
                        measure[i] = (measure[i][0], 'quarter')
                        measureValue -= 2
                if measure[i][-1] == 'eighth':
                    measure.remove(measure[i])
                    measureValue -= 1
                elif measure[i][-1] == 'quarter':
                    measure[i] = (measure[i][0], 'eighth')
                    measureValue -= 1
                if measureValue <= 8: 
                    break
    if measureValue < 8:
        while measureValue < 8:
            if measure[-1][0] == scale[-1]:
                measure.append((scale[0], 'eighth'))
                measureValue += 1
            else:
                measure.append((scale[scale.index(measure[-1][0])+1], 'eighth'))
                measureValue += 1

    return measure

def measureHelper(measure, scale, pitch, noteType, diff=1):
    # assume len(measure) > 0
    measureValue = 0
    measureVals = {'eighth':1, 'quarter':2, 'half':4}

    for c in measure:
        measureValue += measureVals[c[1]]

    if measureValue > 8:
        measure[-1][-1] == 'eighth'
        measureValue -= 1
        return measure

    elif measureValue == 8:
        return measure

    else:
        x = random.random()
        if x <= 0.66: # next note is one above or below
            if pitch in scale:
                i = scale.index(pitch)
            else:
                scale.append(pitch)
                i = scale.index(pitch)

            # note below first note --> last note
            if i - diff < 0:
                i += (len(scale)+1)

            # note above last note --> first note
            if i + diff >= len(scale):
                i -= (len(scale)+1)

            measure.append(random.choice([(scale[(i-diff)%len(scale)], noteType), 
                          (scale[(i+diff)%len(scale)], noteType)]))
            noteType, noteValue = random.choice([('quarter', 2), ('eighth', 1)])
            return measureHelper(measure, scale, pitch, noteType, 1)
        else:
            noteType, noteValue = random.choice([('quarter', 2), ('eighth', 1)])
            return measureHelper(measure, scale, pitch, noteType, diff+1)

def findChordTones(root, chordType):
    # returns chordTones
    maj =     [0, 4, 7]
    minor =   [0, 3, 7]
    dom7 =    [0, 4, 7, 10]
    min7 =    [0, 3, 7, 10]
    maj7 =    [0, 4, 7, 11]
    dim =     [0, 3, 6, 9]
    halfDim = [0, 3, 6, 10]
    dom7b9 =  [0, 3, 7, 1]

    chordTones = []
    chromScales = chromScalesDict()

    chords = {'maj':maj,'minor':minor,'dom7':dom7,'min7':min7,'maj7':maj7,
                  'dim':dim,'halfDim':halfDim,'dom7b9':dom7b9}

    # map inputs to correct dict indices
    scale = chromScales[root]
    chord = chords[chordType]
    for c in chord:
        chordTones.append(scale[c])

    return chordTones

def findRoot(chord):
    # returns root symbol ('A', 'B', 'C', etc.)
    if len(chord) == 1: return chord
    for i in range(len(chord)):
        if chord[i] not in 'ABCDEFG':
            if chord[i] in '#b': 
                return chord[:i+1]
            else:
                return chord[:i]

def findChordType(chord):
    # 'maj', 'minor', 'dom7', 'min7', 'maj7', 'dim', 'halfDim', or '7b9'
    if len(chord) == 1: return 'maj'
    for i in range(len(chord)):
        if chord[i] not in 'ABCDEFG':
            if chord[i] in '#b':
                if chord[i]== chord[-1]: # no suffix
                    return 'maj'
                else: # #/b + something
                    continue
            elif chord[i] == '-': # alternate min/min7 notation
                if '7' in chord: return 'min7'
                else: return 'minor'
            elif chord[i:] == 'min': return 'minor'
            elif chord[i] == '7': return 'dom7'
            elif chord[i:] == 'dom7b9': return '7b9'
            else: 
                if chord[i:] in ['maj','minor','min7','dom7','maj7','dim',
                                 'halfDim','7b9']:
                    return chord[i:]
                else:
                    return None

def makeScale(chord):
    # returns the scale matching the chord
    chromScales = chromScalesDict()
    root, chordType = findRoot(chord), findChordType(chord)

    if chordType in ['maj','maj7']:
        scaleTones = [0, 2, 4, 5, 7, 9, 11, 12, 13]
    elif chordType == 'minor':
        scaleTones = [0, 2, 3, 5, 7, 8, 10, 12, 13]
    elif chordType == 'dom7':
        scaleTones = [0, 2, 4, 5, 7, 9, 10, 12, 13]
    elif chordType == 'min7':
        scaleTones = [0, 2, 3, 5, 7, 9, 10, 11, 12, 13]
    elif chordType in ['dim','halfDim']:
        scaleTones = [0, 2, 3, 5, 6, 8, 9, 11, 12, 13]
    elif chordType == '7b9':
        scaleTones = [0, 2, 4, 5, 7, 9, 10, 1, 12, 13]

    chromScale = chromScales[root]
    scale = []

    for c in scaleTones:
        scale.append(chromScale[c])

    return scale

def chromScalesDict():
    #       0    1     2    3     4    5    6     7    8     9    10   11    12   13    
    C =  ['C4','C#4','D4','Eb4','E4','F4','F#4','G4','G#4','A4','Bb4','B4','C5','rest']
    Cs = ['C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4','C5','C#5','rest']
    Db = ['Db4','D4','Eb4','E4','F4','Gb4','G4','Ab4','A4','Bb4','B4','C5','Db5','rest']
    D =  ['D4','Eb4','E4','F4','F#4','G4','Ab4','A4','Bb4','B4','C5','C#5','D5','rest'] 
    Ds = ['D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4','C5','C#5','D5','D#5','rest']
    Eb = ['Eb4','E4','F4','Gb4','G4','Ab4','A4','Bb4','B4','C5','Db5','D5','Eb5','rest']
    E =  ['E4','F4','F#4','G4','G#4','A4','A#4','B4','C5','C#5','D5','D#5','E5','rest']
    F =  ['F4','Gb4','G4','Ab4','A4','Bb4','B4','C5','Db5','D5','Eb5','E5','F5','rest']
    Fs = ['F#4','G4','G#4','A4','A#4','B4','C5','C#5','D5','Eb5','E5','F5','F#5','rest']
    Gb = ['Gb4','G4','Ab4','A4','Bb4','B4','C5','Db5','D5','Eb5','E5','F5','Gb5','rest']
    G =  ['G4','G#4','A4','Bb4','B4','C5','Db5','D5','Eb5','E5','F5','F#5','G5','rest']
    Gs = ['G#4','A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','rest']
    Ab = ['Ab4','A4','Bb4','B4','C5','Db5','D5','Eb5','E5','F5','Gb5','G5','Ab5','rest']
    A =  ['A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','rest']
    As = ['A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','rest']
    Bb = ['Bb4','B4','C5','Db5','D5','Eb5','E5','F5','Gb5','G5','Ab5','A5','Bb5','rest']
    B =  ['B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5','rest']

    return {'C':C,'C#':Cs,'Db':Db,'D':D,'D#':Ds,'Eb':Eb,'E':E,'F':F,'F#':Fs,
                  'Gb':Gb,'G':G,'G#':Gs,'Ab':Ab,'A':A,'A#':As,'Bb':Bb,'B':B}

def songListDict():
    AllOfMe = ['Dmaj7','Dmaj7','F#7','F#7',
               'B7','B7','E-7','E-7',
               'F#7','F#7','B-7','B-7',
               'E7','E7','E-7','A7',
               'Dmaj7','Dmaj7','F#7','F#7',
               'B7','B7','E-7','E-7',
               'Gmaj7','G-7','F#-7','B7',
               'E-7','A7','D7','A7']

    AllTheThingsYouAre = ['G-7','C-7','F7','Bbmaj7',
                          'Ebmaj7','A7','Dmaj7','Dmaj7',
                          'D-7','G-7','C7','Fmaj7',
                          'Bbmaj7','E7','Amaj7','Amaj7',
                          'B-7','E7','Amaj7','Amaj7',
                          'AbhalfDim','Db7','Gbmaj7','D7',
                          'G-7','C-7','F7','Bbmaj7',
                          'Ebmaj7','Ab7','D-7','DbhalfDim',
                          'C-7','F7','Bbmaj7','Bbmaj7']

    AutumnLeaves = ['D-7','G7','Cmaj7','Fmaj7',
                    'BhalfDim','E7b9','A-7','A-7',
                    'D-7','G7','Cmaj7','Fmaj7',
                    'BhalfDim','E7b9','A-7','A-7',
                    'BhalfDim','E7b9','A-7','A-7',
                    'D-7','G7','Cmaj7','Fmaj7',
                    'BhalfDim','E7b9','A-7','F#7',
                    'BhalfDim','E7b9','A-7','A-7']

    BlackOrpheus = ['B-','C#halfDim','B-','F#7b9',
                    'B-','E-7','Dmaj7','D#dim',
                    'E-7','A7','Dmaj7','Gmaj7',
                    'C#halfDim','F#7b9','B-','C#halfDim',
                    'B-','C#halfDim','B-','F#7b9',
                    'F#halfDim','B7b9','E-','E-',
                    'E-','F#7b9','B-7','Gmaj7',
                    'C#halfDim','F#7b9','B-','B-']

    BlueBossa = ['D-','D-','G-7','G-7',
                 'EhalfDim','A7b9','D-','D-',
                 'F-7','Bb7','Ebmaj7','Ebmaj7',
                 'EhalfDim','A7b9','D-','D-']

    BluesChanges = ['C7','F7','C7','C7',
                    'F7','F#dim','C7','C7',
                    'D-7','G7','C7','C7']

    Cherokee = ['Cmaj7','Cmaj7','G-7','C7',
                'Fmaj7','Fmaj7','Bb7','Bb7',
                'Cmaj7','Cmaj7','D7','D7',
                'D-7','A7b9','D-7','G7', # 1st ending
                'Cmaj7','Cmaj7','G-7','C7',
                'Fmaj7','Fmaj7','Bb7','Bb7',
                'Cmaj7','Cmaj7','D7','D7',
                'D-7','G7','Cmaj7','Cmaj7', # 2nd ending
                'Eb-7','Ab7','Dbmaj7','Dbmaj7', # B section
                'Db-7','F#7','Bmaj7','Bmaj7',
                'B-7','E7','Amaj7','Amaj7',
                'A-7','D7','D-7','G7', 
                'Cmaj7','Cmaj7','G-7','C7',
                'Fmaj7','Fmaj7','Bb7','Bb7',
                'Cmaj7','Cmaj7','D7','D7',
                'D-7','G7','Cmaj7','Cmaj7']

    Confirmation = ['Gmaj7','F#halfDim','E-','G7',
                    'C7','E7','A7','D7',
                    'Gmaj7','F#halfDim','E-','G7',
                    'C7','E7','D7','G',
                    'D-7','G7','Cmaj7','Cmaj7',
                    'F-7','Bb7','Ebmaj7','D7',
                    'Gmaj7','F#halfDim','E-','G7',
                    'C7','E7','A7','G']

    DonnaLee = ['Bbmaj7','G7','C7','C7',
                'C-7','F7','Bbmaj7','Bb7',
                'Ebmaj7','Ab7','Bbmaj7','G7',
                'C7','C7','C-7','F7',
                'Bbmaj7','G7','C7','C7',
                'AhalfDim','D7b9','G-','D7b9',
                'G-','D7b9','G-','Dbdim',
                'G7','F7','Bbmaj7','Bbmaj7']

    FlyMeToTheMoon = ['A-','D-','G7','C',
                      'D-','BhalfDim','E7','A-',
                      'D-','G7','C','C',
                      'D-','G7','C','E7',
                      'A-','D-','G7','C',
                      'D-','BhalfDim','E7','A-',
                      'D-','G7','E7','E7',
                      'D-','G7','C','C']

    Four = ['Fmaj7','Fmaj7','F-7','Bb7',
            'G-7','G-7','Bb-7','Eb7',
            'Fmaj7','Db7','G-7','C7',
            'Fmaj7','Db7','G-7','C7',
            'Fmaj7','Fmaj7','F-7','Bb7',
            'G-7','G-7','Bb-7','Eb7',
            'Fmaj7','Db7','G-7','C7',
            'Ab-7','C7','Fmaj7','Fmaj7']

    GroovinHigh = ['Fmaj7','Fmaj7','B-7','E7',
                   'Fmaj7','Fmaj7','A-7','D7',
                   'G7','G7','G-7','C7',
                   'A-7','Ab-7','G-7','C7',
                   'Fmaj7','Fmaj7','B-7','E7',
                   'Fmaj7','Fmaj7','A-7','D7',
                   'G7','G7','G-7','C7',
                   'G-7','Eb7','Fmaj7','C7']

    Jordu = ['E7','D-7','G7','Fmaj7',
             'E7','D-7','Bb7','Bb7',
             'A7','G7','F7','Ebmaj7',
             'G7','F7','Eb7','C#maj7',
             'E7','D-7','G7','Fmaj7',
             'E7','D-7','Bb7','Bb7']

    JoySpring = ['Gmaj7','D7','Gmaj7','C-7',
                 'B-7','D7','Gmaj7','Bb-7',
                 'Abmaj7','Eb7','Abmaj7','B-7',
                 'Amaj7','D7','Gmaj7','G-7',
                 'Fmaj7','Eb7','Abmaj7','A-7',
                 'Gmaj7','D7','Gmaj7','C-7',
                 'B-7','D7','Gmaj7','Gmaj7']

    LazyBird = ['B-7','D-7','G-7','C7',
                'Fmaj7','B-7','Amaj7,','C#-7',
                'B-7','D-7','G-7','C7',
                'Fmaj7','B-7','Amaj7,','B-7',
                'C#-7','F#7','Bmaj7','F7',
                'B-7','E7','Amaj7','D#7',
                'B-7','D-7','G-7','C7',
                'Fmaj7','B-7','Amaj7,','C#-7']

    Misty = ['Fmaj7','C-7','Bbmaj7','Eb7',
             'Fmaj7','G-7','A-7','C7',
             'Fmaj7','C-7','Bbmaj7','Eb7',
             'Fmaj7','G-7','Fmaj7','Fmaj7',
             'C-7','F7b9','Bbmaj7','Bbmaj7',
             'B-7','E7','AhalfDim','C7',
             'Fmaj7','C-7','Bbmaj7','Eb7',
             'Fmaj7','G-7','A-7','C7']

    ANightInTunisia = ['F7','E-','F7','E-',
                       'F7','E-','F#halfDim','E-',
                       'F7','E-','F7','E-',
                       'F7','E-','F#halfDim','E-',
                       'AhalfDim','D7b9','Gmaj7','B7b9',
                       'F7','E-','F7','E-',
                       'F7','E-','F#halfDim','E-',
                       'F#halfDim','F#halfDim','Fdim','Fdim',
                       'E-7','E-7','Adim','Adim',
                       'A-7','A-7','G#7','G#7',
                       'Gmaj7','Gmaj7','F#halfDim','B7b9']

    Solar = ['D-7','D-7','A-7','D7',
             'Gmaj7','Gmaj7','G-7','C7',
             'Fmaj7','Bb7','Ebmaj7','EhalfDim']

    TakeTheATrain = ['D','D','E7','E7',
                     'E-7','A7','D','D',
                     'D','D','E7','E7',
                     'E-7','A7','D','D',
                     'Gmaj7','Gmaj7','Gmaj7','Gmaj7',
                     'E7','E7','E-7','A7',
                     'D','D','E7','E7',
                     'E-7','A7','D','D']

    YardbirdSuite = ['D','G-','D7','B7',
                     'E7','A7','F#-','A7',
                     'D','G-','D7','B7',
                     'E7','A7','D','D',
                     'F#-','G#halfDim','F#-','B7',
                     'E-','B7','E7','A7',
                     'D','G-','D7','B7',
                     'E7','A7','D','D']

    return {'All Of Me':AllOfMe,
            'All the Things You Are':AllTheThingsYouAre,
            'Autumn Leaves':AutumnLeaves,
            'Black Orpheus':BlackOrpheus,
            'Blue Bossa':BlueBossa,
            'Blues Changes':BluesChanges,
            'Cherokee':Cherokee,
            'Confirmation':Confirmation,
            'Donna Lee':DonnaLee,
            'Fly Me To The Mood':FlyMeToTheMoon,
            'Four':Four,
            "Groovin' High":GroovinHigh,
            'Jordu':Jordu,
            'Joy Spring':JoySpring,
            'Lazy Bird':LazyBird,
            "Misty":Misty,
            'A Night In Tunisia':ANightInTunisia,
            'Solar':Solar,
            'Take the "A" Train':TakeTheATrain,
            'Yardbird Suite':YardbirdSuite}

################################################################################
# Code modified from grid-demo.py (class notes)
################################################################################

from tkinter import *

def init(data):
    data.cols = 4
    data.rows = 0
    data.margin = 200
    data.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
    data.changes = []
    data.chord = ''
    data.closeWindow = False
    data.chordTypes = ['maj','minor','min7','-7','maj7','dom7','dim','halfDim',
                       '7b9']

    ############################################################################
    # MENU screen variables
    ############################################################################

    data.menuScreen = True
    data.startBounds = (data.width/2-150, 300, data.width/2+150, 400)
    data.instructionsBounds = (data.width/2-150, 500, data.width/2+150, 600)
    data.startFill = 'gray'
    data.instructionsFill = 'gray' # button on menu screen

    ############################################################################
    # INSTRUCTIONS screen variables
    ############################################################################

    data.instructionsScreen = False
    data.menuInstructions = '''
    Welcome to Compiles Davis! This tool generates original music over any set of chord changes\n
    to help jazz musicians improve their playing and expand their vocabulary.\n

                                                                            HOW IT WORKS\n

    There are two options: select a tune from a list of standards or input custom chord changes.\n
    To select a tune, simply click its name. To enter custom changes, enter the number of\n 
    measures in one chorus as well as the number of times the changes repeat. Then click GO.\n

    If you select a tune from the list, the music will be generated immediately. If you choose to\n 
    input custom changes, you will be prompted to enter the chords in a table. Each cell\n 
    represents one measure. Your music will be generated once the table is complete. Happy soloing!\n

    NOTE: All pre-programmed chord changes are in the key of Bb.\n    
    '''
    
    ############################################################################
    # HOME screen variables
    ############################################################################

    data.homeScreen = False
    data.mpc = '' # (measures per chorus)
    data.key = ''
    data.choruses = ''
    data.mpcBounds = (3*data.width/4-100, 300, 3*data.width/4+100, 350)
    data.keyBounds = (3*data.width/4-100, 600, 3*data.width/4+100, 650)
    data.chorusesBounds = (3*data.width/4-100, 450, 3*data.width/4+100, 500)
    data.goBounds = (3*data.width/4-100, 600, 3*data.width/4+100, 700)
    data.mpcFill = 'white'
    data.chorusesFill = 'white'
    data.songListDict = songListDict()
    data.songList = []
    data.homeScreenError = False
    data.goButton = True
    data.songBounds = []
    data.songFills = ['gray'] * 20

    ############################################################################
    # HELP screen variables
    ############################################################################

    data.helpScreen = False
    data.instructions = '''


        Major........................................ no additional text\n
        Minor........................................ "-" or “min”\n
        Dominant 7th............................ “7”\n
        Minor 7th.................................. "-7" or “min7”\n
        Major 7th (Δ7).......................... “maj7”\n
        Half Diminished (Ø)................. “halfDim”\n
        Diminished (O)......................... “dim”\n
        Dominant 7th + b9............ “7b9”\n


        Example: for Bb minor 7th, type “Bb-7” or "Bbmin7"
    '''
    ############################################################################
    # ENTRY screen variables
    ############################################################################

    data.entryScreen = False
    data.entryFill = 'white'
    data.backButtonBounds = (25, 25, 175, 75)
    data.helpButtonBounds = (data.width-175, 25, data.width-25, 75)

    data.minBounds = (data.width/2-500, data.height-125, data.width/2-400, data.height-45)
    data.dom7Bounds = (data.width/2-350, data.height-125, data.width/2-250, data.height-45)
    data.min7Bounds = (data.width/2-200, data.height-125, data.width/2-100, data.height-45)
    data.maj7Bounds = (data.width/2-50, data.height-125, data.width/2+50, data.height-45)
    data.dimBounds = (data.width/2+100, data.height-125, data.width/2+200, data.height-45)
    data.halfDimBounds = (data.width/2+250, data.height-125, data.width/2+350, data.height-45)
    data.dom7b9Bounds = (data.width/2+400, data.height-125, data.width/2+500, data.height-45)

    data.entryScreenError = False

def pointInGrid(x, y, data): # from class notes
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data): # from class notes
    # aka 'viewToModel'
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    row = (y - data.margin) // cellHeight
    col = (x - data.margin) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)

def getCellBounds(row, col, data): # from class notes
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * rowHeight
    y1 = data.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)

################################################################################
# Main Tkinter functions
################################################################################

def mousePressed(event, data):
    if data.menuScreen:
        # start
        if (data.startBounds[0] <= event.x <= data.startBounds[2] and
            data.startBounds[1] <= event.y <= data.startBounds[3]):
            data.homeScreen = True
            data.menuScreen = False
        # instructions
        if (data.instructionsBounds[0] <= event.x <= data.instructionsBounds[2] and
            data.instructionsBounds[1] <= event.y <= data.instructionsBounds[3]):
            data.instructionsScreen = True
            data.menuScreen = False

    if data.homeScreen:
        # mpc (measures per chorus)
        if (data.mpcBounds[0] <= event.x <= data.mpcBounds[2] and
            data.mpcBounds[1] <= event.y <= data.mpcBounds[3]):
            if data.mpcFill == 'white': data.mpcFill = 'lightBlue'
            elif data.mpcFill == 'lightBlue': data.mpcFill = 'white'
            if data.chorusesFill == 'lightBlue': data.chorusesFill = 'white'

        # choruses
        if (data.chorusesBounds[0] <= event.x <= data.chorusesBounds[2] and
            data.chorusesBounds[1] <= event.y <= data.chorusesBounds[3]):
            if data.chorusesFill == 'white': data.chorusesFill = 'lightBlue'
            elif data.chorusesFill == 'lightBlue': data.chorusesFill = 'white'
            if data.mpcFill == 'lightBlue': data.mpcFill = 'white'

        # GO button --> chord entry screen
        if (data.goBounds[0] <= event.x <= data.goBounds[2] and
            data.goBounds[1] <= event.y <= data.goBounds[3]): # button clicked
            if (data.mpc != '' and data.choruses != '' and 
                int(data.mpc) % 4 == 0): # valid inputs
                data.entryScreen = True
                data.homeScreen = False
            else:
                data.homeScreenError = True

        # table of preprogrammed songs
        for i in range(len(data.songList)):
            if (data.songBounds[i][0] <= event.x <= data.songBounds[i][2] and
                data.songBounds[i][1] <= event.y <= data.songBounds[i][3]):
                data.changes = data.songListDict[data.songList[i]]
                data.mpc, data.choruses = len(data.changes), 1
                data.homeScreen = False
                #data.closeWindow = True
                if data.choruses != '' and data.mpc != '':
                    makeMelody(data.changes, int(data.choruses), int(data.mpc))
                    quit()
                else:
                    makeMelody(data.changes, 1, len(data.changes))
                    quit()

    elif data.entryScreen:
        (row, col) = getCell(event.x, event.y, data)
        
        # back button
        if (data.backButtonBounds[0] <= event.x <= data.backButtonBounds[2] and
            data.backButtonBounds[1] <= event.y <= data.backButtonBounds[3] and
            data.buttonPressed == False):
            data.homeScreen = True
            data.entryScreen = False
        # help button
        elif (data.helpButtonBounds[0] <= event.x <= data.helpButtonBounds[2] and
            data.helpButtonBounds[1] <= event.y <= data.helpButtonBounds[3] and
            data.buttonPressed == False):
            data.helpScreen = True
            data.entryScreen = False
        # chord buttons
        elif (data.minBounds[0] <= event.x <= data.minBounds[2] and
            data.minBounds[1] <= event.y <= data.minBounds[3] and
            data.buttonPressed == False):
            data.chord += '-'
            data.buttonPressed = True
        elif (data.dom7Bounds[0] <= event.x <= data.dom7Bounds[2] and
            data.dom7Bounds[1] <= event.y <= data.dom7Bounds[3] and
            data.buttonPressed == False):
            data.chord += '7'
            data.buttonPressed = True
        elif (data.min7Bounds[0] <= event.x <= data.min7Bounds[2] and
            data.min7Bounds[1] <= event.y <= data.min7Bounds[3] and
            data.buttonPressed == False):
            data.chord += '-7'
            data.buttonPressed = True
        elif (data.maj7Bounds[0] <= event.x <= data.maj7Bounds[2] and
            data.maj7Bounds[1] <= event.y <= data.maj7Bounds[3] and
            data.buttonPressed == False):
            data.chord += 'maj7'
            data.buttonPressed = True
        elif (data.dimBounds[0] <= event.x <= data.dimBounds[2] and
            data.dimBounds[1] <= event.y <= data.dimBounds[3] and
            data.buttonPressed == False):
            data.chord += 'dim'
            data.buttonPressed = True
        elif (data.halfDimBounds[0] <= event.x <= data.halfDimBounds[2] and
            data.halfDimBounds[1] <= event.y <= data.halfDimBounds[3] and
            data.buttonPressed == False):
            data.chord += 'halfDim'
            data.buttonPressed = True
        elif (data.dom7b9Bounds[0] <= event.x <= data.dom7b9Bounds[2] and
            data.dom7b9Bounds[1] <= event.y <= data.dom7b9Bounds[3] and
            data.buttonPressed == False):
            data.chord += '7b9'
            data.buttonPressed = True
        else:
            # data.selection = (row, col)
            if (data.selection == (row, col)):
                data.selection = (-1, -1)
            else:
                data.selection = (row, col)
                data.buttonPressed = False
            if data.selection != (-1, -1):
                data.entryScreen = True
                data.buttonPressed = False

def keyPressed(event, data):
    if data.homeScreen:
        # mpc
        if data.mpcFill == 'lightBlue':
            if event.keysym in string.digits:
                data.mpc += event.keysym
            elif event.keysym == "BackSpace" and data.mpc != '':
                data.mpc = data.mpc[:-1]
            elif event.keysym == "Return":
                data.mpcFill = 'white'
                data.chorusesFill = 'lightBlue'

        # choruses
        if data.chorusesFill == 'lightBlue':
            if event.keysym in string.digits:
                data.choruses += event.keysym
            elif event.keysym == "BackSpace" and data.choruses != '':
                data.choruses = data.choruses[:-1]

    if data.instructionsScreen:
        if event.keysym == 'Return':
            data.homeScreen = True
            data.instructionsScreen = False

    if data.entryScreen:
        if (event.keysym in 'ABCDEFGb' or 
            event.keysym in string.ascii_letters or
            event.keysym in string.digits):
            data.chord += event.keysym
        elif event.keysym == 'numbersign':
            data.chord += '#'
        elif event.keysym == 'minus':
            data.chord += '-'
        elif event.keysym == "BackSpace" and data.chord != '':
            data.chord = data.chord[:-1]
        if event.keysym == 'Return' and data.chord != '':
            if findChordType(data.chord) != None:
                data.changes.append(data.chord)
                data.buttonPressed = False
                if data.entryScreenError: data.entryScreenError = False
                if (data.selection[1]+1) % 4 == 0:
                    data.selection = (data.selection[0]+1, 0)
                else:
                    data.selection = (data.selection[0], data.selection[1]+1)
            else:
                data.entryScreenError = True
            data.chord = ''

    if data.helpScreen:
        if event.keysym == 'b':
            data.entryScreen = True
            data.helpScreen = False

def timerFired(data):
    pass

def drawMenuScreen(canvas, data):
    # side images
    data.image1 = PhotoImage(file='trumpetplayer.gif')
    # http://www.vinylsilhouettes.com/content/images/thumbs/0003382_trumpet-player-12-wall-silhouettes.gif
    data.image2 = PhotoImage(file='saxplayer.gif')
    # https://s-media-cache-ak0.pinimg.com/736x/79/bc/6b/79bc6b58e2c3553ed2b75406c22ffcef.jpg
    canvas.create_image(3*data.width/4+50, data.height/2+50, image=data.image1)
    canvas.create_image(data.width/4-75, data.height/2+50, image=data.image2)
    # title
    canvas.create_text(data.width/2, 100, text='COMPILES DAVIS', 
                       font='Zapfino 60 bold', fill='white')
    canvas.create_text(data.width/2, 175, text='A tool for jazz musicians',
                       font='Zapfino 25 italic', fill='white')
    # start button
    canvas.create_rectangle(data.startBounds, fill=data.startFill, width=5)
    canvas.create_text(data.width/2, 
                      (data.startBounds[1]+data.startBounds[3])/2,
                       text='START',
                       font='Athelas 30 bold')
    # instructions button
    canvas.create_rectangle(data.instructionsBounds, fill=data.instructionsFill,
                            width=5)
    canvas.create_text(data.width/2, 
                      (data.instructionsBounds[1]+data.instructionsBounds[3])/2,
                       text='INSTRUCTIONS',
                       font='Athelas 30 bold')

def drawInstructionsScreen(canvas, data):
    canvas.create_text(data.width/2, 100, text='COMPILES DAVIS', 
                       font='Zapfino 60 bold', fill='white')
    canvas.create_rectangle(data.width/4-100, 145, 3*data.width/4+100, 755, 
                            fill='gray', width=5)
    canvas.create_text(data.width/2, data.height/2+50, text=data.menuInstructions,
                       font='Athelas 19')
    canvas.create_text(data.width/2, 725, text='(Press enter to start)',
                       font='Athelas 18 italic')

def drawHomeScreen(canvas, data):
    # Title
    canvas.create_text(data.width/2, 100, text='COMPILES DAVIS', 
                       font='Zapfino 60 bold', fill='white')
    # CHOOSE A TUNE
    canvas.create_text(data.width/4-25, 200, text='CHOOSE A TUNE',
                       font='Athelas 40', fill='white')
    # "OR" TEXT
    canvas.create_text(data.width/2, data.height/2, text='OR...', 
                       font='Athelas 40 italic', fill='white')
    # Enter custom changes
    canvas.create_text(3*data.width/4, 200, text='ENTER CUSTOM CHANGES',
                       font='Athelas 40', fill='white')
    # mpc TEXT above
    canvas.create_text(3*data.width/4, 265, text='Measures per chorus:', 
                       font='Athelas 30', fill='white')
    canvas.create_text(3*data.width/4, 365, text='(must be a multiple of 4)',
                       font='Athelas 17', fill='white')
    # mpc BOX
    canvas.create_rectangle(data.mpcBounds, fill=data.mpcFill)
    # mpc TEXT in box
    canvas.create_text(3*data.width/4, (data.mpcBounds[3]+data.mpcBounds[1])/2, 
                       text=data.mpc, font='Helvetica 30 italic')
    # choruses TEXT above
    canvas.create_text(3*data.width/4, 415, text='Number of choruses:', 
                       font='Athelas 30', fill='white')
    # choruses BOX
    canvas.create_rectangle(data.chorusesBounds, fill=data.chorusesFill)
    # choruses TEXT in box
    canvas.create_text(3*data.width/4, 
                       (data.chorusesBounds[3] + data.chorusesBounds[1])/2, 
                       text=data.choruses, font='Helvetica 30 italic')
    # Go BOX
    canvas.create_rectangle(data.goBounds, fill='green', width=5)
    # Go TEXT
    canvas.create_text(3*data.width/4, 650, text='GO!', 
                       font='Athelas 50')
    # Error message
    if data.homeScreenError:
        canvas.create_text(3*data.width/4, 750, text='ERROR: INVALID INPUTS',
                           font='Times 30 bold italic', fill='red')
    # Song list
    for songName in data.songListDict:
        data.songList.append(songName)

    # songs 1-10 (left column)
    l = 0
    for i in range(0, 500, 50):
        canvas.create_rectangle(data.width/4-225, 250+i, data.width/4-25, 300+i,
                                fill=data.songFills[l])
        data.songBounds.append((data.width/4-225, 250+i, data.width/4-25, 300+i))
        l += 1

    # songs 11-20 (right column)
    r = 0
    for i in range(0, 500, 50):
        canvas.create_rectangle(data.width/4-25, 250+i, data.width/4+175, 300+i,
                                fill=data.songFills[r])
        data.songBounds.append((data.width/4-25, 250+i, data.width/4+175, 300+i))
        r += 1

    for i in range(10):
        canvas.create_text(data.width/4-125, 275+50*i, text=data.songList[i],
                           font='Times 17 italic')

    for i in range(10):
        canvas.create_text(data.width/4+75, 275+50*i, text=data.songList[10+i],
                           font='Times 17 italic')

def drawHelpScreen(canvas, data):
    canvas.create_rectangle(data.width/4-100, 150, 3*data.width/4+100, 750, 
                            fill='gray', width=5)
    canvas.create_text(data.width/2, 80, text='CHORD ENTRY INSTRUCTIONS',
                       font='Athelas 50', fill='white')
    canvas.create_text(data.width/2-195, 185, 
                       text='Key                                Suffix',
                       font='Athelas 30 bold', anchor=NW)
    canvas.create_text(data.width/2, data.height/2+25, text=data.instructions, 
                       font='Times 20')
    canvas.create_text(data.width/2, data.height-75, 
                       text='Press "b" to go back', font='Athelas 20 italic')

def drawEntryScreen(canvas, data):
    # draw grid; fill cell when clicked; draw current chord

    if len(data.changes) == int(data.mpc):
        data.entryScreen = False

    data.rows = int(data.mpc) // data.cols

    # title
    canvas.create_text(data.width/2, 100, text='CLICK TO ENTER CHORDS',
                       font='Athelas 50', fill='white')
    # draw current chord
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            if (data.selection == (row, col)):
                data.entryFill = 'lightBlue'  
            else: 
                data.entryFill = 'white'
            canvas.create_rectangle(x0, y0, x1, y1, fill=data.entryFill)
            if data.selection == (row, col):
                canvas.create_text(x0 + (x1-x0)/2, y0 + (y1-y0)/2, 
                                   text=data.chord, font='Times 40')
    # draw previous chords            
    for i in range(len(data.changes)):
        row, col = i//4, i%4
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text=data.changes[i],
                           font='Times 40')   

    # back button
    canvas.create_rectangle(data.backButtonBounds, width=5, fill='yellow')
    canvas.create_text((data.backButtonBounds[0]+data.backButtonBounds[2])/2,
                        (data.backButtonBounds[1]+data.backButtonBounds[3])/2,
                        text='BACK', font='Athelas 40')

    # help button
    canvas.create_rectangle(data.helpButtonBounds, width=5, fill='yellow')
    canvas.create_text((data.helpButtonBounds[0]+data.helpButtonBounds[2])/2,
                        (data.helpButtonBounds[1]+data.helpButtonBounds[3])/2,
                        text='HELP', font='Athelas 40')

    if data.entryScreenError:
        canvas.create_text(data.width/2, 640, text='ERROR: INVALID CHORD',
                           font='Times 40 bold italic', fill='red')

    ############################################################################
    # CHORD BUTTONS
    ############################################################################

    # minor button
    canvas.create_rectangle(data.minBounds, fill='lightBlue')
    canvas.create_text((data.minBounds[0]+data.minBounds[2])/2,
                        (data.minBounds[1]+data.minBounds[3])/2,
                        text='-', font='Times 40')
    canvas.create_text((data.minBounds[0]+data.minBounds[2])/2,
                        (data.minBounds[1]+data.minBounds[3])/2+55,
                        text='Minor', font='Athelas 20', fill='white')

    # dom7 button
    canvas.create_rectangle(data.dom7Bounds, fill='lightBlue')
    canvas.create_text((data.dom7Bounds[0]+data.dom7Bounds[2])/2,
                        (data.dom7Bounds[1]+data.dom7Bounds[3])/2,
                        text='7', font='Times 40')
    canvas.create_text((data.dom7Bounds[0]+data.dom7Bounds[2])/2,
                        (data.dom7Bounds[1]+data.dom7Bounds[3])/2+55,
                        text='Dominant 7th', font='Athelas 20', fill='white')

    # min7 button
    canvas.create_rectangle(data.min7Bounds, fill='lightBlue')
    canvas.create_text((data.min7Bounds[0]+data.min7Bounds[2])/2,
                        (data.min7Bounds[1]+data.min7Bounds[3])/2,
                        text='-7', font='Times 40')
    canvas.create_text((data.min7Bounds[0]+data.min7Bounds[2])/2,
                        (data.min7Bounds[1]+data.min7Bounds[3])/2+55,
                        text='Minor 7th', font='Athelas 20', fill='white')

    # maj7 button
    canvas.create_rectangle(data.maj7Bounds, fill='lightBlue')
    canvas.create_text((data.maj7Bounds[0]+data.maj7Bounds[2])/2,
                        (data.maj7Bounds[1]+data.maj7Bounds[3])/2,
                        text='Δ7', font='Times 40')
    canvas.create_text((data.maj7Bounds[0]+data.maj7Bounds[2])/2,
                        (data.maj7Bounds[1]+data.maj7Bounds[3])/2+55,
                        text='Major 7th', font='Athelas 20', fill='white')

    # dim button
    canvas.create_rectangle(data.dimBounds, fill='lightBlue')
    canvas.create_text((data.dimBounds[0]+data.dimBounds[2])/2,
                        (data.dimBounds[1]+data.dimBounds[3])/2,
                        text='O', font='Times 40')
    canvas.create_text((data.dimBounds[0]+data.dimBounds[2])/2,
                        (data.dimBounds[1]+data.dimBounds[3])/2+55,
                        text='Diminished', font='Athelas 20', fill='white')

    # halfDim button
    canvas.create_rectangle(data.halfDimBounds, fill='lightBlue')
    canvas.create_text((data.halfDimBounds[0]+data.halfDimBounds[2])/2,
                        (data.halfDimBounds[1]+data.halfDimBounds[3])/2,
                        text='Ø', font='Times 40')
    canvas.create_text((data.halfDimBounds[0]+data.halfDimBounds[2])/2,
                        (data.halfDimBounds[1]+data.halfDimBounds[3])/2+55,
                        text='Half Diminished', font='Athelas 20', fill='white')

    # 7b9 button
    canvas.create_rectangle(data.dom7b9Bounds, fill='lightBlue')
    canvas.create_text((data.dom7b9Bounds[0]+data.dom7b9Bounds[2])/2,
                        (data.dom7b9Bounds[1]+data.dom7b9Bounds[3])/2,
                        text='7b9', font='Times 40')
    canvas.create_text((data.dom7b9Bounds[0]+data.dom7b9Bounds[2])/2,
                        (data.dom7b9Bounds[1]+data.dom7b9Bounds[3])/2+55,
                        text='Dominant 7+b9', font='Athelas 20', fill='white')
    
def redrawAll(canvas, data):
    data.image = PhotoImage(file='tp_background.gif')
    canvas.create_image(data.width/2, data.height/2, image=data.image)

    if data.menuScreen: drawMenuScreen(canvas, data)
    elif data.instructionsScreen: drawInstructionsScreen(canvas, data)
    elif data.homeScreen: drawHomeScreen(canvas, data)
    elif data.helpScreen: drawHelpScreen(canvas, data)
    elif data.entryScreen: drawEntryScreen(canvas, data)
    else:
        data.closeWindow = True
        if data.choruses != '' and data.mpc != '':
            makeMelody(data.changes, int(data.choruses), int(data.mpc))
            quit()
        else:
            makeMelody(data.changes, 1, len(data.changes))
            quit()

def quit():
    root.destroy()

################################################################################
# RUN FUNCTION (from 15-112 class notes)
################################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.title('Compiles Davis')
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind('<Button-1>', lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind('<Key>', lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app

run(1200, 800)

################################################################################
# TEST FUNCTIONS
################################################################################

def testFindRoot():
    print('Testing findRoot...', end='')
    assert(findRoot('C') == 'C')
    assert(findRoot('C-') == 'C')
    assert(findRoot('Cmin') == 'C')
    assert(findRoot('C#') == 'C#')
    assert(findRoot('C#min') == 'C#')
    assert(findRoot('Bb') == 'Bb')
    print('Passed!')

def testFindChordType():
    print('Testing findChordType...', end='')
    assert(findChordType('C') == 'maj')
    assert(findChordType('Cmaj') == 'maj')
    assert(findChordType('Cmin') == 'minor')
    assert(findChordType('C-') == 'minor')
    assert(findChordType('Cmin7') == 'min7')
    assert(findChordType('C-7') == 'min7')
    assert(findChordType('C#') == 'maj')
    assert(findChordType('C#-') == 'minor')
    assert(findChordType('C#-7') == 'min7')
    print('Passed!')

def testfindChordTones():
    print('Testing findChordTones...', end='')
    assert(findChordTones('C', 'maj') == ['C4', 'E4', 'G4'])
    assert(findChordTones('F', 'maj') == ['F4', 'A4', 'C5'])
    assert(findChordTones('C', 'minor') == ['C4', 'Eb4', 'G4'])
    assert(findChordTones('C', 'min7') == ['C4', 'Eb4', 'G4', 'Bb4'])
    assert(findChordTones('C', 'dom7') == ['C4', 'E4', 'G4', 'Bb4'])
    assert(findChordTones('C', 'dim') == ['C4', 'Eb4', 'F#4', 'A4'])
    assert(findChordTones('C', 'halfDim') == ['C4', 'Eb4', 'F#4', 'Bb4'])
    print('Passed!')

def testAll():
    testfindChordTones()
    testFindRoot()
    testFindChordType()

#testAll()