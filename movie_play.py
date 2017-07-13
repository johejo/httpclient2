import vlc

p = vlc.MediaPlayer('sample.mp4')
p.play()
while True:
    q = input('Input \'q\' to quit.\n>>')
    if q == 'q':
        break
