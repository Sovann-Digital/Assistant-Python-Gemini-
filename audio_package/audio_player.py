import asyncio
import edge_tts
import os
from pydub import AudioSegment
from pydub.playback import play

class AudioPlayer:
    async def tts(self, text, voice='en-US-GuyNeural', output_file='output.mp3'):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    async def main(self, text, voice='en-US-GuyNeural', output_file='output.mp3'):
        await self.tts(text, voice, output_file)
        # print(f"Text '{text}' has been converted to speech.")
        self.play_and_remove(output_file)

    def play_and_remove(self, output_file):
        # Play the audio file
        audio = AudioSegment.from_mp3(output_file)
        play(audio)
        
        # Remove the audio file after playback
        os.remove(output_file)
        # print(f"Audio file '{output_file}' has been played and removed.")
