import vlc
import subprocess

# p = vlc.MediaPlayer('sample.mp4')
# i = vlc.Instance()
# p = i.media_player_new()
# m = i.media_new('sample.mp4')
# p.set_media(m)
# p.play()
subprocess.call('vlc sample.mp4', shell=True)
while True:
    q = input('Input \'q\' to quit.\n>>')
    if q == 'q':
        break
