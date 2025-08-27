import winsound
import time

winsound.PlaySound('aiiiiiiiiiii.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
time.sleep(2)
winsound.PlaySound(None, winsound.SND_PURGE)
