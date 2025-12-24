import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import useragents
from streamlink.stream.hls import HLSStream


@pluginmatcher(
    re.compile(r"https?://img\.tv8bucuk\.com/.*tv8-5-canli-yayin.*")
)
class TV8Bucuk(Plugin):

    _HLS_RE = re.compile(
        r'https://tv8\.daioncdn\.net/[^"\']+\.m3u8[^"\']*'
    )

    def _get_streams(self):
        headers = {
            "User-Agent": useragents.CHROME,
            "Referer": "https://img.tv8bucuk.com/",
        }

        # Make HLS reader as tolerant as Streamlink allows
        self.session.options.set("hls-timeout", 0)
        self.session.options.set("hls-segment-timeout", 15)
        self.session.options.set("hls-playlist-reload-time", 1)

        res = self.session.http.get(
            self.url,
            headers=headers,
            acceptable_status=(200,),
        )

        match = self._HLS_RE.search(res.text)
        if not match:
            self.logger.error("TV8.5: HLS URL not found")
            return

        return HLSStream.parse_variant_playlist(
            self.session,
            match.group(0),
            headers=headers,
            namekey="pixels",
        )


__plugin__ = TV8Bucuk

