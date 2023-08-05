import argparse
import os
from discognition.version import __version__


parser = argparse.ArgumentParser(
    prog='discognition',
    description='update mp3 metadata and file/directory names using the discogs api',
    )

parser.add_argument('directory', nargs='?', default=None, help='specify album directory for querying discogs.') #default=os.getcwd()

parser.add_argument('-t', '--tag', nargs='*', help="update existing files' tags with specific metadata fields:\
    options = 'artist', 'album', 'year', 'label', 'art', 'track', 'tracknumber'; \
    or 'all' to rewrite tags using all available data from Discogs")

parser.add_argument('-p', '--print', action='store_true', help='print album metadata \
    (default action if -t, -rn, and -rd are unused)')

parser.add_argument('-rn', '--renametracks', action='store_true', help='rename files from Discogs metadata.')

parser.add_argument('-rd', '--renamedirectories', action='store_true', help='rename directories from Discogs metadata.')

parser.add_argument('-i', '--interactive', action='store_true', help='iterate through search items interactively')

parser.add_argument('-R', '--recursive', action='store_true', help='use all subdirectories with mp3s. e.g.: use on an artist\'s directory \
or music library directory. ')

parser.add_argument('-s', '--search', nargs='?', help='query discogs database instead of existing metadata. \
    takes search string or release id/url', metavar="")

parser.add_argument('-g', '--generateconfig', nargs='*', help=' create yaml configuration file. \
    first argument = Discogs API token, second argument = music library directory', metavar="")

parser.add_argument('-v', '--version', action='version', version="%(prog)s ("+__version__+")", help='show program\'s version number and exit')

args = parser.parse_args()