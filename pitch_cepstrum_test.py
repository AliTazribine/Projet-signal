import Utils
import audiofile

speakerw=Utils.get_random_speakers('slt',5)
speakerm=Utils.get_random_speakers('bdl',5)
sig,fs=audiofile.read(speakerw[0])

pitch=Utils.pitch_cepstrum(speakerw)
ok=True
for i in pitch:
    if(i<60 or i>500):
        ok=False
if(ok):
    print("le pitch est bien entre 60Hz et 500Hz")
else:
    print("il y'a une erreur")