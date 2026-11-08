from gnani.tts import GnaniTTSClient

voices = GnaniTTSClient.supported_voices(model="timbre-v2.5")

print("\nAVAILABLE TIMBRE 2.5 VOICES:\n")

for voice in voices:
    print(voice)