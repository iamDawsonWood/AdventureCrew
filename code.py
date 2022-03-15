# Write your code here :-)
import board
import alarm
import audiomixer
import time
import busio
import adafruit_aw9523
import digitalio
from digitalio import DigitalInOut
from audiocore import WaveFile
from digitalio import DigitalInOut, Direction, Pull
from random import randint
from audiomp3 import MP3Decoder

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

##Creating the MP3 Decoder
mp3 = open("Redboy_ready.mp3", "rb")
decoder = MP3Decoder(mp3)
audio = AudioOut(board.A1)

mixer = audiomixer.Mixer(voice_count=1, sample_rate=44100, channel_count=1, bits_per_sample=16, samples_signed=True)
audio.play(mixer) # attach mixer to audio playback

meleeSoundProfile = 0
magicSoundProfile = 0
dodgeSoundProfile = 0

from adafruit_pn532.i2c import PN532_I2C

reset_pin = DigitalInOut(board.D6)
req_pin = DigitalInOut(board.D12)

i2c = busio.I2C(board.SCL, board.SDA)

aw = adafruit_aw9523.AW9523(i2c)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

pn532.SAM_configuration()
intro_voice = True
writeMode = False
readMode = True

button1_pin = aw.get_pin(1)  # Button on AW io 1
button1_pin.direction = digitalio.Direction.INPUT

button2_pin = aw.get_pin(2)  # Button on AW io 2
button2_pin.direction = digitalio.Direction.INPUT

button3_pin = aw.get_pin(3)  # Button on AW io 2
button3_pin.direction = digitalio.Direction.INPUT

#powerbutton_pin = aw.get_pin(15)  # Button on AW io 2
#powerbutton_pin.switch_to_output(value=False)
#def Sleep():
    #alarm.exit_and_deep_sleep_until_alarms(powerbutton_pin)

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!


#loading sound files
decoder.file = open("Redboy_ready.mp3", "rb")

enviromentSounds = {

    #1: WaveFile(open("SCD_PCM_02.mp3", "rb")),
    #2: WaveFile(open("SCD_FM_13.mp3","rb")),
    #3: WaveFile(open("SCD_FM_18.mp3","rb")),
    #4: WaveFile(open("SCD_FM_25.mp3", "rb")),
    #5: WaveFile(open("SCD_FM_29.mp3", "rb")),
    #6: WaveFile(open("SCD_PCM_05.mp3", "rb")),
}

def load(fileName):
    return open(fileName, "rb")

############
###For the dictionaries: the key is the zone ID, (0 being default) and the value for a key is sound[] if there are values, or None if it does not change that action sound
meleeSoundLibrary = {

    #DEFAULT MELEE
    0: [
        load("MeleeDefault_Redboy_1.mp3"),
        load("MeleeDefault_Redboy_2.mp3"),
        load("MeleeDefault_Redboy_3.mp3"),
        load("MeleeDefault_Redboy_4.mp3"),
        load("MeleeDefault_Redboy_5.mp3"),
    ],

}

magicSoundLibrary = {
    #DEFAULT MAGIC
    0: [
        load("MagicDefault_Redboy_1.mp3"),
        load("MagicDefault_Redboy_2.mp3"),
        load("MagicDefault_Redboy_3.mp3"),
    ],

    1: [
        load("BoulderBash_Redboy_1.mp3"),
        load("BoulderBash_Redboy_2.mp3"),
        load("BoulderBash_Redboy_3.mp3"),
        load("BoulderBash_Redboy_4.mp3"),
        load("BoulderBash_Redboy_5.mp3"),
        load("BoulderBash_Redboy_6.mp3"),
        ]
}

dodgeSoundLibrary = {
    0: [load("DodgeDefault_Redboy_1.mp3")]
}

activeNoises = {0: meleeSoundLibrary[0], 1: magicSoundLibrary[0], 2:dodgeSoundLibrary[0]}



##Call this on zone entry or exit
## pass the new zone ID to it
## if we leave a zone pass 0
def changeActiveNoises(zone):

    activeNoises = {
        ##melee
        0: meleeSoundLibrary[zone] if meleeSoundLibrary[zone] != None else activeNoises[0],
        ##magic
        1: magicSoundLibrary[zone] if magicSoundLibrary[zone] != None else activeNoises[1],
        ##dodge
        2: dodgeSoundLibrary[zone] if dodgeSoundLibrary[zone] != None else activeNoises[2]
    }


def playActionNoise(action):

    sound = activeNoises[action]

    ##now we have an array of sounds, let's get a random one

    index = randint(0, len(sound)-1)

    ##play the sound at that index
    decoder.file = sound[index]
    mixer.voice[0].play(decoder)

    while audio.playing:
        pass


def playMeleeNoise():
    playActionNoise(0)

def playMagicNoise():
    playActionNoise(1)

def playDodgeNoise():
    playActionNoise(2)

def ReadCards():

        uid = pn532.read_passive_target(timeout=0.05)
        print(".", end="")

        try:
            cardReadValues = (pn532.ntag2xx_read_block(6))
            cardRead = int.from_bytes((cardReadValues), "big")
            print("Reading! This is Card", (cardRead), "!")
            audio.play(sounds[cardRead])

            while audio.playing:
                pass
            print("stopped")
        except TypeError:
            return


if intro_voice == True:
    mixer.voice[0].play(decoder)
    while audio.playing:
        pass

print("Waiting for RFID/NFC card to write to!")

while True:

    #if not powerbutton_pin.value:
    #    Sleep()

    if not button1_pin.value:
        playActionNoise(0)

    if not button2_pin.value:
        playActionNoise(1)

    if not button3_pin.value:
        playActionNoise(2)

    ReadCards()

  #write to card. UN-COMMENT THIS TO WRITE TO CARDS


    #cardNumber = 6
    #cardID_byteValues = (cardNumber).to_bytes(4, 'big')
    #write.do_write (6, cardID_byteValues)
    #cardWrite = int.from_bytes(cardID_byteValues, "big")
    #print("Wrote to card!", "This is Card", (cardWrite))# Write your code here :-)
# Write your code here :-)
