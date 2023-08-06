"""Play music from stormbot"""
import os
import shlex
import subprocess
from stormbot.bot import Plugin


class Music(Plugin):
    def __init__(self, bot, args):
        self._bot = bot
        self.player = args.music_player
        self.path = os.path.abspath(args.music_path)
        self.default = args.music_default

    @classmethod
    def argparser(cls, parser):
        parser.add_argument("--music-player", type=str, default="paplay", help="Music player (default: %(default)s)")
        parser.add_argument("--music-path", type=str, default=os.getcwd(), help="Music player (default: %(default)s)")
        parser.add_argument("--music-default", type=str, default=None, help="Music player (default: %(default)s)")

    def safe_path(self, path):
        path = os.path.abspath(path)
        common_prefix = os.path.commonpath([path, self.path])
        return common_prefix == self.path

    def cmdparser(self, parser):
        subparser = parser.add_parser('music', bot=self._bot)
        subparser.set_defaults(command=self.run)
        subparser.add_argument("--volume", type=int, default=65536, help="Music player volume (default: %(default)i)")
        subparser.add_argument("music", type=str, nargs='?', default=self.default,
                               help="Music to play (default: %(default)s)")

    def run(self, msg, parser, args, peer):
        music = os.path.join(self.path, args.music)
        if not self.safe_path(music):
            self._bot.write("Don't try to mess with me !")
            return

        if not os.path.exists(music):
            self._bot.write("You have such shit taste I don't even have this song !")

        self._bot.write("playing your favorite song out loud !")
        cmd = shlex.split(self.player) + [music]
        subprocess.Popen(cmd, stdin=None, stdout=None, stderr=None, close_fds=True)
