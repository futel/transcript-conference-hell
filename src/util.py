import boto3
import datetime
import os

transcript_bucket_name = 'transcript-conference-hell'


def write_line(s, logname):
    """Write a line to a log file."""
    logfile = '/tmp/' + logname
    # q&d temporary log file
    with open(logfile, 'a') as f:
        f.write(s)
        f.write('\n')

def clear_lines():
    """Clear log file."""
    logname = 'lines'
    logfile = '/tmp/' + logname
    open(logfile, 'w').close()

def log(msg, logname=None):
    log_msg = msg
    if logname:
        msg_name = logname
    else:
        msg_name = 'log'
    log_msg = "{} {} {}".format(
        datetime.datetime.now().isoformat(), msg_name, log_msg)
    print(log_msg)
    if logname:
        # Also write a line to the given transcript file.
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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_creds.json'
    with open('google_creds.json', 'w') as f:
        f.write(os.environ['GOOGLE_CREDS_JSON'])

def _s3_transcript_key():
    """ Return a unique s3 key name. """
    return "transcript_{}".format(datetime.datetime.now().isoformat())

def write_lines_s3():
    """Write the transcript file to an S3 bucket."""
    # Get S3 resource with creds in env.
    #s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    key_name = _s3_transcript_key()
    log_file_name = 'lines'
    log_file_path = '/tmp/' + log_file_name
    response = s3_client.upload_file(
        log_file_path, transcript_bucket_name, key_name)
    print('XXX {}'.format(response))
    #s3.Bucket(BUCKET).upload_file(logfile, key_name)
    #s3.Bucket(bucket_name).put_object(Key=key_name, Body=data)
    print('Wrote transcript to {}'.format(key_name))
