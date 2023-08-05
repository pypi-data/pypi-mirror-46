import plac

from hermes_audio_server.__about__ import __recorder__
from hermes_audio_server import cli
from hermes_audio_server.config import DEFAULT_CONFIG


def main(verbose: ('use verbose output', 'flag', 'v'),
         version: ('print version information and exit', 'flag', 'V'),
         config: ('configuration file [default: {}]'.format(DEFAULT_CONFIG),
                  'option', 'c')):
    """hermes-audio-recorder is an audio server implementing the recording part
    of the Hermes protocol."""
    cli.main(__recorder__, verbose, version, config)


if __name__ == '__main__':
    plac.call(main)
