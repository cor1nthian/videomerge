import subprocess, os, sys

# Build ffmpeg and ffprobe from source or download at
# https://www.gyan.dev/ffmpeg/builds/
# or download at https://mega.nz/file/TAlnSJhC#u58yn-9baEduAXW2dDXLz8YAc_72DC8E0u9J1Wmr6WI
# only 'bin' folder content needed
# Windows build only

# All tools are suggested to be placed to script folder


contentFolderPath = 'C:\\users\\admin\\Downloads\\Perimeter OST\\mp3\\mp4'
outputFullFilename = contentFolderPath + os.path.sep + 'out.mp4'
ffmpegfname = 'ffmpeg.exe'
ffprobefname = 'ffprobe.exe'
vidlistfname = 'vidlist.txt'
totalduration = 0
systemExitCode = 0


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


def list2textfile(filename: str, datalist: list):
    if os.path.exists(filename):
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            fline = 'file ' + line.replace('\\', '\\\\').replace(' ', '\\ ') + '\n'
            f.write(fline)
        f.close()
    return True


def getmediaduration(mediafilename: str):
    global ffprobefname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if mediafilename == '':
        colorprint.out('PATH TO MP3 FILE IS EMPTY')
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
    if len(contentFolderPath) == 0 or contentFolderPath is None:
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
    scriptdir = get_script_path()
    ffmpegfname = scriptdir + os.path.sep + ffmpegfname
    ffprobefname = scriptdir + os.path.sep + ffprobefname
    vidlistfname = scriptdir + os.path.sep + vidlistfname
    filelist = listFilesInFolderByExt(contentFolderPath)
    if filelist is None or len(filelist) == 0:
        colorprint.out('NO FILES FOUND IN SPECIFIED FOLDER')
        systemExitCode = 3
        sys.exit(systemExitCode)
    if os.path.exists(vidlistfname):
        os.remove(vidlistfname)
    if os.path.exists(outputFullFilename):
        os.remove(outputFullFilename)
    if not list2textfile(vidlistfname, filelist):
        colorprint.out('COULD NOT CREATE VIDEO FILE LIST')
        systemExitCode = 4
        sys.exit(systemExitCode)
    for file in filelist:
        duration = getmediaduration(file)
        if duration is None or float(duration) == 0.0:
            colorprint.out('COULD NOT GET MEDIA DURATION')
            systemExitCode = 4
            sys.exit(systemExitCode)
        totalduration += float(duration)
    arglist = [ ffmpegfname, '-safe', '0', '-f', 'concat', '-i' ]
    arglist.append(vidlistfname)
    arglist.append('-codec')
    arglist.append('copy')
    arglist.append(outputFullFilename)
    subprocess.run(arglist)
    os.remove(vidlistfname)
    print('Done. Video file available at ' + outputFullFilename)