import datetime
import os


def write_line(s, logname=None):
    if not logname:
        logname = 'foo'
    logfile = '/tmp/' + logname
    print(s)
    # q&d temporary log file
    with open(logfile, 'a') as f:
        f.write(s)
        f.write('\n')

def log(msg, logname=None):
    msg = "{} {}".format(datetime.datetime.now().isoformat(), msg)
    return write_line(msg, logname)

def wav_to_chunk(b):
    """Return wav bytes with header removed."""
    # ie only one chunk, we will probably need to split.
    #binarySound = bytearray()
    #binaryHeader = bytearray()
    #with open("a2002011001-e02.wav",'rb') as f:
        #binaryHeader = f.read(44)
        #binarySound = f.read()
    # The header length can vary depending on the fact chunk. Could skip to "data" plus 4?
    #https://www.twilio.com/blog/build-a-soundboard-using-gcp-speech-to-text-twilio-voice-media-streams-and-aspdotnet-core
    # usually 44, we have 58?
    #_header = f.read(58)
    #return f.read()
    return b[58:]

# Google wants creds in a file and the filename in an env var.
# This is stupid and dangerous. A build script would be better but
# still stupid and dangerous. The build tooling is probably made
# for Docker, wiithout that all we have is env for secrets.
def cred_kluge():
    """
    Stuff creds from env into a file, put that filename into an
    env var.
    """
    log("cred_kluge")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_creds.json'
    with open('google_creds.json', 'w') as f:
        f.write(os.environ['GOOGLE_CREDS_JSON'])
