import shutil, subprocess, os, sys


# Build ffmpeg and ffprobe from source
# or download at https://www.gyan.dev/ffmpeg/builds/
# or download at https://ffmpeg.org//download.html
# or download at https://mega.nz/file/TAlnSJhC#u58yn-9baEduAXW2dDXLz8YAc_72DC8E0u9J1Wmr6WI
# Only 'bin' folder content needed
# Windows build only

# All tools are suggested to be placed to script folder


contentFolderPath = 'C:\\Users\\admin\\Downloads\\tronlegacy\\mp4'
outputFullFilename = contentFolderPath + os.path.sep + 'out.mp4'
outputFullFilenamemd = contentFolderPath + os.path.sep + 'outmd.mp4'
ffmpegfname = 'ffmpeg.exe'
ffprobefname = 'ffprobe.exe'
vidlistfname = 'vidlist.txt'
metadatafile = 'metadata.txt'
txtchapdesc = 'chapdesc.txt'
escChar = '\\'
createTextChapDesc = True
createTextChapters = False
exactChapters = True
addNums2ChapDesc = False
createFadeIn = True
createFadeOut = True
totalduration = 0
systemExitCode = 0

maxdfo = 10 # max fade out duration
maxdfi = 10 # max fade in duration

metainfokeyspl = '/'

escapeChrs = [ '\\', ' ', '\'' ]

allowedSizes = [ '7680x4320',
                 '3840x2160',
                 '2560x1440',
                 '1920x1080',
                 '1280x720',
                 '854x480',
                 '640x360',
                 '426x240' ]

metainfo = { 'metaauthors_perimeter': 'K-D Lab [Victor Krasnokutsky]',
             'metaadd_perimeter': { 'empire primary': 'Bell Strike',
                                    'empire psychosphere': 'Phobia',
                                    'exodus military': 'Construction',
                                    'exodus primary': 'Promised Land',
                                    'exodus psychosphere': 'Delusion',
                                    'harkbackhood primary': 'DNA',
                                    'harkbackhood covered':'Scourge',
                                    'alpha expedition': 'Destination' },
             'metaauthors_tekken 5': '',
             'metaadd_tekken 5': '',
             'metaauthors_fight club': 'The Dust Brothers',
             'metaadd_fight club': '',
             'metaauthors_doom 2016': 'Mick Gordon',
             'metaadd_doom 2016': '',
             'metaauthors_doom eternal': 'Mick Gordon',
             'metaadd_doom eternal': '',
             'metaauthors_warcraft 3': '',
             'metaadd_warcraft 3': '',
             'metaauthors_wh': 'Jeremy Soule',
             'metaadd_wh': '' }


# A python class definition for printing formatted text on terminal.
# Initialize TextFormatter object like this:
# >>> cprint = TextFormatter()
#
# Configure formatting style using .cfg method:
# >>> cprint.cfg('r', 'y', 'i')
# Argument 1: foreground(text) color
# Argument 2: background color
# Argument 3: text style
#
# Print formatted text using .out method:
# >>> cprint.out("Hello, world!")
#
# Reset to default settings using .reset method:
# >>> cprint.reset()

class TextFormatter:
    COLORCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7   # white
    }
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }


    # constructor
    def __init__(self):
        self.reset()


    # function to reset properties
    def reset(self):
        # properties as dictionary
        self.prop = {'st': None, 'fg': None, 'bg': None}
        return self


    # function to configure properties
    def cfg(self, fg, bg=None, st=None):
        # reset and set all properties
        return self.reset().st(st).fg(fg).bg(bg)


    # set text style
    def st(self, st):
        if st in self.FORMATCODE.keys():
            self.prop['st'] = self.FORMATCODE[st]
        return self


    # set foreground color
    def fg(self, fg):
        if fg in self.COLORCODE.keys():
            self.prop['fg'] = 30 + self.COLORCODE[fg]
        return self


    # set background color
    def bg(self, bg):
        if bg in self.COLORCODE.keys():
            self.prop['bg'] = 40 + self.COLORCODE[bg]
        return self


    # formatting function
    def format(self, string):
        w = [self.prop['st'], self.prop['fg'], self.prop['bg']]
        w = [str(x) for x in w if x is not None]
        # return formatted string
        return '\x1b[%sm%s\x1b[0m' % (';'.join(w), string) if w else string


    # output formatted string
    def out(self, string):
        print(self.format(string))


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def escapeChars(sequence: str):
    out = ''
    for ch in sequence:
        out += escChar + ch
    return out


def getMetaKey(keyname: str):
    global metainfokeyspl
    try:
        if metainfokeyspl in keyname:
            keynamespl = keyname.split(metainfokeyspl)
            return metainfo[keynamespl[0]][keynamespl[1]]
        else:
            return metainfo[keyname]
    except BaseException:
        return ''



def addFadeIn(fname:str, start: int = 0, duration: int = 5):
    global  ffmpegfname
    global outputFullFilename
    global  maxdfo
    global  maxdfi
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(fname):
        return None
    dura = getmediaduration(fname)
    if dura is None:
        return None
    duraint = int(float(dura))
    if maxdfo < duration or 0 >= duration:
        return None
    if 0 > start or duraint <= start:
        return None
    fadestr = 'fade=t=in:st=' + str(start) + ':d=' + str(duration)
    outputFullFilenamespl = outputFullFilename.split('\\')
    outputFullFilenamejoined = os.path.sep.join(outputFullFilenamespl[:-1])
    outputFullFilenameed = outputFullFilenamespl[-1].split('.')
    if len(outputFullFilenameed) > 2:
        outputFullFilenamemi = '.'.join(outputFullFilenameed[:-1]) + 'mi.' + outputFullFilenameed[-1]
    elif len(outputFullFilenameed) == 2:
        outputFullFilenamemi = outputFullFilenameed[0] + 'mi.' + outputFullFilenameed[1]
    else:
        return None
    outputFullFilenamemi = outputFullFilenamejoined + os.path.sep + outputFullFilenamemi
    arglist = [ ffmpegfname,
                '-y',
                '-i',
                fname,
                '-vf',
                fadestr,
                '-c:a',
                'copy',
                outputFullFilenamemi ]
    subprocess.run(arglist)
    return outputFullFilenamemi


def addFadeOut(fname:str, start: int = -999999, duration: int = 5):
    global ffmpegfname
    global outputFullFilename
    global maxdfo
    global maxdfi
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(fname):
        return None
    dura = getmediaduration(fname)
    if dura is None:
        return None
    duraint = int(float(dura))
    if maxdfi < duration or 0 >= duration:
        return None
    if -duraint <= start:
        return None
    if start < 0:
        if -999999 == start:
            start = duraint - duration
        else:
            start = duraint + start
    fadestr = 'fade=t=out:st=' + str(start) + ':d=' + str(duration)
    outputFullFilenamespl = outputFullFilename.split('\\')
    outputFullFilenamejoined = os.path.sep.join(outputFullFilenamespl[:-1])
    outputFullFilenameed = outputFullFilenamespl[-1].split('.')
    if len(outputFullFilenameed) > 2:
        outputFullFilenamemo = '.'.join(outputFullFilenameed[:-1]) + 'mo.' + outputFullFilenameed[-1]
    elif len(outputFullFilenameed) == 2:
        outputFullFilenamemo = outputFullFilenameed[0] + 'mo.' + outputFullFilenameed[1]
    else:
        return None
    outputFullFilenamemo = outputFullFilenamejoined + os.path.sep + outputFullFilenamemo
    arglist = [ffmpegfname,
               '-y',
               '-i',
               fname,
               '-vf',
               fadestr,
               '-c:a',
               'copy',
               outputFullFilenamemo ]
    subprocess.run(arglist)
    return outputFullFilenamemo


def formTitle(argstr:str, removeNums: bool = True):
    global metainfo
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if 'EpicHyrbrid' in argstr:
        print('!!!')
    if len(argstr) == 0 or argstr is None:
        return ''
    argstrlow = argstr.strip().lower()
    keylist = []
    for key in metainfo:
        if not '_' in key:
            continue
        keylowspl = key.lower().split('_')[-1]
        if keylowspl in argstrlow:
            keylist.append(key)
    title = ''
    # title = argstr
    soundname = argstr.split('\\')[-1]
    if removeNums and '. ' in soundname:
        soundname = ''.join(soundname.split('. ')[1:]).strip()
    for key in keylist:
        if 'metaauthors' in key:
            if len(metainfo[key]) > 0 and not ' - ' in argstr:
                title += metainfo[key]
        if 'metaadd' in key:
            if len(metainfo[key]) > 0 and type(metainfo[key]) is dict:
                for skey in metainfo[key]:
                    skeylow = skey.lower()
                    if skeylow in argstrlow:
                        argstrpr = argstr.split('c')[0][::-1].split('\\')[0][::-1]
                        soundname = (metainfo[key][skey]) + ' [' + argstr + ']'
                        if len(title) > 0:
                            title += ' - ' + soundname
                        else:
                            title = soundname
                        return title
                    # else:
                        # soundname = argstr
            # else:
                # soundname = argstr
    if len(title) > 0:
        if '.' in soundname:
            title += ' - ' + soundname.replace(soundname.split('.')[-1], '')[:-1]
        else:
            title += ' - ' + soundname
    else:
        if len(soundname) > 0:
            # snext = soundname.split('.')[-1]
            if '.' in soundname:
                title = soundname.replace(soundname.split('.')[-1], '')[:-1]
    return title


def list2textfile(filename: str, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            # fline = 'file "' + line.replace('\\', '\\\\').replace(' ', '\\ ') + '"\n'
            # flieln = 'file ' + escapeChars(line)
            flieln = 'file ' + line.replace('\\', '\\\\').replace('\'', '\\\'').replace(' ', '\\ ') + '\n'
            f.write(flieln)
        f.close()
    return True


def getrealduration(duration: int):
    if duration == 0 or duration is None:
        return None
    realdura = ''
    days = 0
    hrs = 0
    mins = 0
    secs = 0
    dura = 0
    if duration <= 10:
        return '00:00:00'
    if duration > 1000:
        dura = duration / 1000
    else:
        dura = duration
    secs = int(dura % 60)
    mins = int((dura / 60) % 60)
    hrs = int(dura / 3600)
    if hrs > 0:
        days = int(dura / 86400)
    if days > 0:
        realdura = ('{:02}'.format(days) + '{:02}'.format(hrs) + ':' + '{:02}'.format(mins) + ':' +
                    '{:02}'.format(secs))
    else:
        realdura = '{:02}'.format(hrs) + ':' + '{:02}'.format(mins) + ':' + '{:02}'.format(secs)
    return realdura


def getmediaduration(mediafilename: str):
    global ffprobefname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if mediafilename == '':
        colorprint.out('PATH TO MEDIA FILE IS EMPTY')
        return None
    if not os.path.exists(mediafilename):
        colorprint.out('PATH TO MEDIA FILE DOES NOT EXIST')
        return None
    subarglist = [ ffprobefname, '-show_entries', 'format=duration', '-i', mediafilename ]
    popen  = subprocess.Popen(subarglist, stdout = subprocess.PIPE)
    popen.wait()
    output = str(popen.stdout.read())
    if len(output) > 0 and '\\r\\n' in output:
        return output.split('\\r\\n')[1][9:]
    else:
        return None


def listFilesInFolderByExt(folderpath: str, fileext: str = '.mp4',
                           fullfilenames: bool = True):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if folderpath == '':
        colorprint.out('PATH TO FOLDER IS EMPTY')
        return None
    if not os.path.exists(folderpath):
        colorprint.out('PATH TO FOLDER DOES NOT EXIST')
        return None
    filenames = []
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            if os.path.splitext(filename)[1] == fileext:
                if fullfilenames:
                    filenames.append(os.path.join(root, filename))
                else:
                    filenames.append(filename)
    return filenames


######### SCRIPT #########
if __name__ == "__main__":
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    # print(formTitle('C:\\Users\\admin\\Downloads\\ppsc\\mp4\\05. Spanish Fly (Flamenco Dub Pt. 1).mp4'))
    if len(contentFolderPath) == 0 or contentFolderPath is None or not type(contentFolderPath) is str:
        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                contentFolderPath = sys.argv[1]
            else:
                colorprint.out('CONTENT FOLDER DOES NOT EXIST')
                systemExitCode = 1
                sys.exit(systemExitCode)
        else:
            colorprint.out('CONTENT FOLDER PATH NOT FOUND')
            systemExitCode = 2
            sys.exit(systemExitCode)
    else:
        if not os.path.exists(contentFolderPath):
            colorprint.out('CONTENT FOLDER DOES NOT EXIST')
            systemExitCode = 1
            sys.exit(systemExitCode)
    if exactChapters is None or not type(exactChapters) is bool:
        if len(sys.argv) > 2:
            createTextChapters = bool(sys.argv[2])
        else:
            colorprint.out('EXACT CHAPTER TIMESTAMPS MARK VARIABLE NOT SET')
            systemExitCode = 3
            sys.exit(systemExitCode)
    if createTextChapDesc is None or not type(createTextChapDesc) is bool:
        if len(sys.argv) > 3:
            createTextChapDesc = bool(sys.argv[2])
        else:
            colorprint.out('TEXT CHAPTER CREATION MARK VARIABLE NOT SET')
            systemExitCode = 4
            sys.exit(systemExitCode)
    scriptdir = get_script_path()
    ffmpegfname = scriptdir + os.path.sep + ffmpegfname
    ffprobefname = scriptdir + os.path.sep + ffprobefname
    vidlistfname = scriptdir + os.path.sep + vidlistfname
    metadatafile = scriptdir + os.path.sep + metadatafile
    txtchapdesc = contentFolderPath + os.path.sep + txtchapdesc
    if os.path.exists(outputFullFilename):
        os.remove(outputFullFilename)
    if os.path.exists(outputFullFilenamemd):
        os.remove(outputFullFilenamemd)
    if os.path.exists(vidlistfname):
        os.remove(vidlistfname)
    if createTextChapDesc:
        if os.path.exists(txtchapdesc):
            os.remove(txtchapdesc)
    filelist = listFilesInFolderByExt(contentFolderPath)
    if filelist is None or len(filelist) == 0 or not type(filelist) is list:
        colorprint.out('NO FILES FOUND IN SPECIFIED FOLDER')
        systemExitCode = 5
        sys.exit(systemExitCode)
    if not list2textfile(vidlistfname, filelist):
        colorprint.out('COULD NOT CREATE VIDEO FILE LIST')
        systemExitCode = 6
        sys.exit(systemExitCode)
    mdcontent = [ ';FFMETADATA1' ]
    if createTextChapDesc:
        chapdesclines = [ 'Chapters:' ]
    arglist = [ ffmpegfname,
                '-y',
               '-safe',
               '0',
               '-f',
               'concat',
               '-i',
               vidlistfname,
               '-codec',
               'copy',
                # '-t',
                # '00:15:45',
               outputFullFilename ]
    subprocess.run(arglist)
    vidx = 0
    minduration = 0  # 1
    fllen = len(filelist) - 1
    pdur = 0
    mdur = int(float(getmediaduration(outputFullFilename))) * 1000
    for file in filelist:
        mdcontent.append('[CHAPTER]')
        mdcontent.append('TIMEBASE=1/1000')
        duration = getmediaduration(file)
        if duration is None or float(duration) == 0.0:
            colorprint.out('COULD NOT GET MEDIA DURATION')
            systemExitCode = 7
            sys.exit(systemExitCode)
        else:
            duration = pdur + minduration + (int(float(duration)) * 1000)
            mdcontent.append('START=' + str(minduration + 1))
            # duration = (minduration + int(float(duration)) * 1000) - 1
            # title = formTitle(((file[:-4][::-1]).split('\\'))[0][::-1])
            if vidx < fllen:
                mdcontent.append('END=' + str(duration))
            else:
                mdcontent.append('END=' + str(mdur))
            # title = formTitle((file[:-4].split('\\'))[-1])
            title = formTitle(file)
            mdcontent.append('title=' + title + '\n')
            if createTextChapDesc:
                if addNums2ChapDesc:
                    num = file.split('\\')[-1].split('. ')[0]
                    chapdesclines.append(getrealduration(minduration + 1) + ' [' + num + '] ' + title)
                else:
                    chapdesclines.append(getrealduration(minduration + 1) + ' ' + title)
            if exactChapters:
                minduration = duration + 300
            else:
                minduration = duration
            # pdur = int(float(getmediaduration(outputFullFilename))) * 1000
            # if vidx > 0:
                # fmetaname = '.'.join(file.split('\\')[-1].split('.')[:-1]) + '_meta.txt'
                # if os.path.exists(fmetaname):
        vidx += 1
    with open(metadatafile, 'w', encoding='utf-8') as f:
        for line in mdcontent:
            f.write(line + '\n')
        f.close()
    if createTextChapDesc:
        if os.path.exists(txtchapdesc):
            os.remove(txtchapdesc)
        with open(txtchapdesc, 'w', encoding='utf-8') as f:
            for line in chapdesclines:
                f.write(line + '\n')
            f.close()
    if createFadeIn:
        afires = addFadeIn(outputFullFilename)
        if afires is None:
            colorprint.out('COULD NOT ADD FADE IN EFFECT')
            systemExitCode = 7
            sys.exit(systemExitCode)
        shutil.copy2(afires, outputFullFilename)
        os.remove(afires)
    if createFadeOut:
        afores = addFadeOut(outputFullFilename)
        if afores is None:
            colorprint.out('COULD NOT ADD FADE OUT EFFECT')
            systemExitCode = 8
            sys.exit(systemExitCode)
        shutil.copy2(afores, outputFullFilename)
        os.remove(afores)
    arglist = [ ffmpegfname,
                '-y',
                '-i',
                outputFullFilename,
                '-i',
                metadatafile,
                '-map_metadata',
                '1',
                '-codec',
                'copy',
                outputFullFilenamemd ]
    subprocess.run(arglist)
    subprocess.run(arglist)
    os.remove(vidlistfname)
    os.remove(metadatafile)
    if createTextChapDesc:
        print('Done. Video file available at ' + outputFullFilename +
              '\nChapter description file is available at ' + txtchapdesc)
    else:
        print('Done. Video file available at ' + outputFullFilename)