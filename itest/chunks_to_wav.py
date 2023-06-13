"""
Try to turn ulaw chunks into a WAV file.
"""

import wave

# foo is concatenated chunks with no header
with open("foo", "rb") as f:
    with wave.open("foo.wav", 'w') as fw:
        fw.setframerate(8000.0)
        #fw.setframerate(8012.0)
        fw.setnchannels(1) # mono
        fw.setsampwidth(1)
        fw.writeframes(f.read())
        #fw.writeframesraw(f.read())
