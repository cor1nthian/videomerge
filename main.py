import subprocess, os, sys

# Build ffmpeg and ffprobe from source
# or download at https://www.gyan.dev/ffmpeg/builds/
# or download at https://ffmpeg.org//download.html
# or download at https://mega.nz/file/TAlnSJhC#u58yn-9baEduAXW2dDXLz8YAc_72DC8E0u9J1Wmr6WI
# Only 'bin' folder content needed
# Windows build only

# All tools are suggested to be placed to script folder


contentFolderPath = 'C:\\users\\admin\\Downloads\\Perimeter OST\\mp3\\mp4'
outputFullFilename = contentFolderPath + os.path.sep + 'out.mp4'
outputFullFilenamemd = contentFolderPath + os.path.sep + 'outmd.mp4'
ffmpegfname = 'ffmpeg.exe'
ffprobefname = 'ffprobe.exe'
vidlistfname = 'vidlist.txt'
metadatafile = 'metadata.txt'
txtchapdesc = 'chapdesc.txt'
createTextChapDesc = False
createTextChapters = True
exactChapters = True
totalduration = 0
systemExitCode = 0

metainfokeyspl = '/'
metainfo = { 'metaauthors_perimeter': 'K-D Lab [Victor Krasnokutsky]',
             'metaadd_perimeter': { 'empire primary': 'Bell Strike',
                                    'empire psychosphere': 'Phobia',
                                    'exodus military': 'Construction',
                                    'exodus primary': 'Promised Land',
                                    'exodus psychosphere': 'Delusion',
                                    'harkbackhood primary': 'DNA',
                                    'harkbackhood covered':'Scourge',
                                    'alpha expedition': 'Destination' } }


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


def getMetaKey(keyname: str):
    global  metainfokeyspl
    try:
        if metainfokeyspl in keyname:
            keynamespl = keyname.split(metainfokeyspl)
            return metainfo[keynamespl[0]][keynamespl[1]]
        else:
            return metainfo[keyname]
    except BaseException:
        return ''


def formTitle(argstr:str):
    global metainfo
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if len(argstr) == 0 or argstr is None:
        return ''
    argstrlow = argstr.strip().lower()
    keylist = []
    for key in metainfo:
        if not '_' in key:
            continue
        keylowspl = key.lower().split('_')[1]
        if keylowspl in key.lower():
            keylist.append(key)
    title = ''
    soundname = ''
    for key in keylist:
        if 'metaauthors' in key:
            title += metainfo[key]
        if 'metaadd' in key:
            if len(metainfo[key]) != 0 and type(metainfo[key]) is dict:
                for skey in metainfo[key]:
                    skeylow = skey.lower()
                    if skeylow in argstrlow:
                        soundname = (metainfo[key][skey]) + ' [' + argstr + ']'
                        title += ' - ' + soundname
                        return title
                    else:
                        soundname = argstr
            else:
                soundname = argstr
    title += ' - ' + soundname
    return  title


def list2textfile(filename: str, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            fline = 'file ' + line.replace('\\', '\\\\').replace(' ', '\\ ') + '\n'
            f.write(fline)
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
    if duration < 10:
        return '00:00:00'
    if duration > 1000:
        dura = duration / 1000
    else:
        dura = duration
    secs = int(dura % 60)
    mins = int((dura / 60) % 60)
    hrs = int((mins / 60) % 60)
    if hrs > 0:
        days = int((hrs / 24) % 24)
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
        colorprint.out('PATH TO MP3 FILE DOES NOT EXIST')
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


if __name__ == "__main__":
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    if len(contentFolderPath) == 0 or contentFolderPath is None or not type(contentFolderPath) is str:
        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                contentFolderPath = sys.argv[1]
            else:
                colorprint.out('CONTENT FOLDER DOES NOT EXIST')
                systemExitCode = 1
                sys.exit(systemExitCode)
        else:
            colorprint.out('CONTENT FOLDER NOT FOUND')
            systemExitCode = 2
            sys.exit(systemExitCode)
    else:
        if not os.path.exists(contentFolderPath):
            colorprint.out('CONTENT FOLDER DOES NOT EXIST')
            systemExitCode = 1
            sys.exit(systemExitCode)
    if exactChapters is None or not type(exactChapters) is bool:
        if len(sys.argv) >= 3:
            createtextchapdesc = bool(sys.argv[3])
        else:
            colorprint.out('EXACT CHAPTER TIMESTAMPS MARK VARIABLE NOT SET')
            systemExitCode = 4
            sys.exit(systemExitCode)
    if createTextChapDesc is None or not type(createTextChapDesc) is bool:
        if len(sys.argv) >= 4:
            createTextChapDesc = bool(sys.argv[4])
        else:
            colorprint.out('TEXT CHAPTER CREATION MARK VARIABLE NOT SET')
            systemExitCode = 5
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
        systemExitCode = 3
        sys.exit(systemExitCode)
    if not list2textfile(vidlistfname, filelist):
        colorprint.out('COULD NOT CREATE VIDEO FILE LIST')
        systemExitCode = 4
        sys.exit(systemExitCode)
    mdcontent = []
    if createTextChapDesc:
        chapdesclines = [ 'Chapters:' ]
    minduration = 1
    for file in filelist:
        mdcontent.append('[CHAPTER]')
        mdcontent.append('TIMEBASE=1/1000')
        duration = getmediaduration(file)
        if duration is None or float(duration) == 0.0:
            colorprint.out('COULD NOT GET MEDIA DURATION')
            systemExitCode = 6
            sys.exit(systemExitCode)
        else:
            mdcontent.append('START=' + str(minduration))
            # duration = (minduration + int(float(duration)) * 1000) - 1
            title = formTitle(((file[:-4][::-1]).split('\\'))[0][::-1])
            if createTextChapDesc:
                chapdesclines.append(getrealduration(minduration) + ' ' + title)
            duration = minduration + int(float(duration)) * 1000
            if exactChapters:
                minduration = (duration + 1) + 500
            else:
                minduration = duration + 1
            mdcontent.append('END=' + str(duration))
            mdcontent.append('title=' + title + '\n')
            totalduration += int(float(duration)) + 1
    with open(metadatafile, 'w', encoding='utf-8') as f:
        f.write(';FFMETADATA1' + '\n')
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
    arglist = [ ffmpegfname,
                '-safe',
                '0',
                '-f',
                'concat',
                '-i',
                vidlistfname,
                '-codec',
                'copy',
                outputFullFilename ]
    subprocess.run(arglist)
    arglist = [ ffmpegfname,
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
    os.remove(vidlistfname)
    os.remove(metadatafile)
    if createTextChapDesc:
        print('Done. Video file available at ' + outputFullFilename +
              '\nChapter description file is available at ' + txtchapdesc)
    else:
        print('Done. Video file available at ' + outputFullFilename)