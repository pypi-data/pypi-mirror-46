Songline Library:


from songline import Sendline

token = 'xdkakfdjksjdfayfdyaodf'
messenger = Sendline(token)

#send message
messenger.sendtext('Hello world')

#send sticker
messenger.sticker(1,1)

#send image
messenger.sendimage('https://img.pngio.com/python-logo-python-logo-png-268_300.png')
