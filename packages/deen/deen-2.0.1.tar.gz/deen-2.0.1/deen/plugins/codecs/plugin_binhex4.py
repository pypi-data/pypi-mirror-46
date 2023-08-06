"""
TODO: implement plugin
https://en.wikipedia.org/wiki/BinHex
https://docs.python.org/3/library/binhex.html"""
import codecs
import binhex

from .. import DeenPlugin


class DeenPPPPPPluginHexBin4(DeenPlugin):
    name = 'hexbin4'
    display_name = 'HexBin4'
    cmd_name = 'hexbin4'
    cmd_help='HexBin 4 encode/decode data'

    def __init__(self):
        super(DeenPluginHexBin4, self).__init__()

    def process(self, data):
        super(DeenPluginHexBin4, self).process(data)
        try:
            data = codecs.encode(data, 'hex')
        except binhex.Error as e:
            self.error = e
        return data

    def unprocess(self, data):
        super(DeenPluginHexBin4, self).unprocess(data)
        try:
            data = codecs.decode(data, 'hex')
        except (binhex.Error, TypeError) as e:
            self.error = e
        return data
