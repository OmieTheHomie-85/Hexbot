from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import nextcord
from nextcord.ext import commands, activities
from gtts import gTTS

LANGUAGES = {
    "Arabic":'ar',
    "Bulgarian":'bg',
    "Bengali":'bn',
    "Bosnian":'bs' ,
    "Catalan":'ca' ,
    "Czech":'cs' ,
    "Welsh":'cy' ,
    "Danish":'da' ,
    "German":'de',
    "English":'en' ,
    "Spanish":'es' ,
    "Finnish":'fi' ,
    "French":'fr' ,
    "Gujarati":'gu' ,
    "Hindi":'hi' ,
    "Icelandic":'is' ,
    "Italian":'it' ,
    "Thai":'th' ,
    "Filipino":'tl' ,
    "Turkish":'tr' ,
    "Ukrainian":'uk' ,
    "Urdu":'ur' ,
    "Vietnamese":'vi' ,
    "Chinese":'zH-CN' ,
    "Chinese (Mandarin)":'zh-TW',
}
def get_all_languages():
    languages = []
    for language in LANGUAGES.keys():
        languages.append(language)
    return languages

def convert_language(language):
    return LANGUAGES[language]


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @nextcord.slash_command(name="tts", description="Text to speech")
    async def tts(self, interaction:Interaction, text: str = SlashOption(description="Text to speech"), language: str = SlashOption(description="Language to speak in", choices=get_all_languages())):
        if interaction.user.voice is not None:
            try:
                vc = await interaction.user.voice.channel.connect()
            except:
                vc = interaction.guild.voice_client

            sound = gTTS(text=text, lang=convert_language(language), slow=False)
            sound.save("cogs/tts-audio.mp3")

            if vc.is_playing():
                return await interaction.send("I'm already playing something")

            source = await nextcord.FFmpegOpusAudio.from_probe(source="cogs/tts-audio.mp3", method="fallback")
            vc.play(source)
            await interaction.send("Playing text to speech")
        else:
            await interaction.send("You are not in a voice channel")




def setup(bot):
    bot.add_cog(TextToSpeech(bot))