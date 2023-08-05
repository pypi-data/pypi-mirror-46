# Discognition

**Discognition** is a command line tool to reorganize your media library. It uses data available from the Discogs API to add/modify ID3 tags, change file names and alter library directory structure. 

## Requirements

- python3
- Discogs account (free)

## Installation & Setup

- Install via pip `pip install discognition` (required python packages: [mutagen](https://github.com/quodlibet/mutagen) and [discogs_client](https://github.com/discogs/discogs_client))


- You need to have a Discogs account in order to get a Discogs API token. Once you have registered for an account, you can generate or access your user token at https://www.discogs.com/settings/developers

- Add your Discogs API user-token and your music library directory using the `--generateconfig` option:
  
```
discognition -g TOKEN /PATH/TO/LIBRARY
```

- Or if you prefer to create your config file manually, add the following to `~/.discognition-conf.yaml`:

```
token: TOKEN
directory: /PATH/TO/LIBRARY
```
 

## Usage

```
discognition [-h] [-t [TAG [TAG ...]]] [-p] [-rn] [-rd] [-i] [-R] [-s ]
                    [-g [[...]]] [-v]
                    [directory]

update mp3 metadata and file/directory names using the discogs api

positional arguments:
  directory             specify album directory for querying discogs.

optional arguments:
  -h, --help            show this help message and exit
  -t [TAG [TAG ...]], --tag [TAG [TAG ...]]
                        update existing files' tags with specific metadata
                        fields: options = 'artist', 'album', 'year', 'label',
                        'art', 'track', 'tracknumber'; or 'all' to rewrite
                        tags using all available data from Discogs
  -p, --print           print album metadata (default action if -t, -rn, and
                        -rd are unused)
  -rn, --renametracks   rename files from Discogs metadata.
  -rd, --renamedirectories
                        rename directories from Discogs metadata.
  -i, --interactive     iterate through search items interactively
  -R, --recursive       use all subdirectories with mp3s. e.g.: use on an
                        artist's directory or music library directory.
  -s [], --search []    query discogs database instead of existing metadata.
                        takes search string or release id/url
  -g [ [ ...]], --generateconfig [ [ ...]]
                        create yaml configuration file. first argument =
                        Discogs API token, second argument = music library
                        directory
  -v, --version         show program's version number and exit

```

## Examples

Search for an album and print its metadata, without updating any files or tags:

```
> discognition -s madvillainy

searching Discogs for "madvillainy"...
found 37 album(s)...
using album: Doom* & Madlib - Madvillain - Madvillainy
https://www.discogs.com/Doom-Madlib-Madvillain-Madvillainy/release/242785
TALB : Madvillainy
TPE1 : MF Doom, Madlib, Madvillain
TPUB : Stones Throw Records
TDRC : 2004
image_url : https://img.discogs.com/WxPQzrIegpuWDicMoxIx1y0UKNo=/fit-in/600x597/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-239980-1290094126.jpeg.jpg
tracks : {'title': ['The Illest Villains', 'Accordion', 'Meat Grinder', 'Bistro', 'Raid', "America's Most Blunted", 'Sickfit (Inst.)', 'Rainbows', 'Curls', 'Do Not Fire! (Inst.)', 'Money Folder', 'Scene Two (Voice Skit)', 'Shadows Of Tomorrow', 'Operation Lifesaver AKA Mint Test', 'Figaro', 'Hardcore Hustle', 'Strange Ways', '(Intro)', 'Fancy Clown', 'Eye', 'Supervillain Theme (Inst.)', 'All Caps', 'Great Day', 'Rhinestone Cowboy']}
```

Add record labels to the "Publisher" field for all of an artist's albums

```
> discognition Music/music-library/Annette\ Peacock/ -R -t label

No mp3s found in Music/music-library/Annette Peacock/

found the following directories with mp3s:
Music/music-library/Annette Peacock/I'm  the One(1972)
Music/music-library/Annette Peacock/X-Dreams(1978)

searching Discogs for "I'm the One Annette Peacock"...
found 59 album(s)...
using album: Annette Peacock - I'm The One
https://www.discogs.com/Annette-Peacock-Im-The-One/release/2704734

changed TPUB to RCA Victor

searching Discogs for "X-Dreams Annette Peacock"...
found 27 album(s)...
using album: Annette Peacock - X-Dreams
https://www.discogs.com/Annette-Peacock-X-Dreams/release/540789

changed TPUB to Aura
```

Update all tags for an album and print Discogs data to terminal 

```
> discognition Music/music-library/Steve\ Lehman/Sélébéyone\(2016\)/ -p -t all

searching Discogs for "Steve Lehman & Sélébéyone Steve Lehman, Sélébéyone"...
found 2 album(s)...
using album: Steve Lehman & Sélébéyone - Steve Lehman & Sélébéyone
https://www.discogs.com/Steve-Lehman-S%C3%A9l%C3%A9b%C3%A9yone-Steve-Lehman-S%C3%A9l%C3%A9b%C3%A9yone/release/9712042

TALB : Steve Lehman & Sélébéyone
TPE1 : Steve Lehman, Sélébéyone
TPUB : Pi Recordings
TDRC : 2016
image_url : https://img.discogs.com/NuXf8_9vW5DUSCbCIqeFlXGVqt0=/fit-in/500x446/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-9712042-1485171083-4918.jpeg.jpg
tracks : {'title': ['Laamb', 'Are You In Peace? ', 'Akap', 'Origine ', 'Cognition ', 'Hybrid', 'Dualism ', 'Geminou', 'Bamba']}

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 01 Laamb.mp3's TIT2 to Laamb

changed APIC to Music/music-library/Steve Lehman/Sélébéyone(2016)/cover.jpg

changed TDRC to 2016

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 01 Laamb.mp3's TRCK to 1

changed TPUB to Pi Recordings

changed TPE1 to Steve Lehman, Sélébéyone

changed TALB to Steve Lehman & Sélébéyone

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 02 Are You In Peace-.mp3's TIT2 to Are You In Peace? 

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 02 Are You In Peace-.mp3's TRCK to 2

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 03 Akap.mp3's TIT2 to Akap

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 03 Akap.mp3's TRCK to 3

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 04 Origine.mp3's TIT2 to Origine 

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 04 Origine.mp3's TRCK to 4

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 05 Cognition.mp3's TIT2 to Cognition 

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 05 Cognition.mp3's TRCK to 5

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 06 Hybrid.mp3's TIT2 to Hybrid

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 06 Hybrid.mp3's TRCK to 6

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 07 Dualism.mp3's TIT2 to Dualism 

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 07 Dualism.mp3's TRCK to 7

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 08 Geminou.mp3's TIT2 to Geminou

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 08 Geminou.mp3's TRCK to 8

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 09 Bamba.mp3's TIT2 to Bamba

changed Music/music-library/Steve Lehman/Sélébéyone(2016)/Steve Lehman - Sélébéyone - 09 Bamba.mp3's TRCK to 9
```

Interactively search Discogs and download cover art for an album

```
> discognition Music/music-library/Swans/To\ Be\ Kind\(2014\)/ -t cover -i -p

searching Discogs for "To Be Kind Swans"...
searched for To Be Kind Swans

Do you want: 
Swans - To Be Kind (2014)
11 tracks on Vinyl
https://www.discogs.com/Swans-To-Be-Kind/release/5690090
(y/n)? 
n

Do you want: 
Swans - To Be Kind (2014)
11 tracks on Vinyl
https://www.discogs.com/Swans-To-Be-Kind/release/5679893
(y/n)? 
n

Do you want: 
Swans - To Be Kind (2014)
10 tracks on CD
https://www.discogs.com/Swans-To-Be-Kind/release/5649159
(y/n)? 
y

using album: To Be Kind
https://www.discogs.com/Swans-To-Be-Kind/release/5649159

TALB : To Be Kind
TPE1 : Swans
TPUB : Young God Records
TDRC : 2014
image_url : https://img.discogs.com/cOcqx5xxohqD5INywki8T4Ygc-M=/fit-in/600x538/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-5649159-1399990559-7559.jpeg.jpg
tracks : {'title': ['Screen Shot', 'Just A Little Boy (For Chester Burnett)', 'A Little God In My Hands', "Bring The Sun / Toussaint L'Ouverture", 'Some Things We Do', 'She Loves Us', 'Kirsten Supine', 'Oxygen', 'Nathalie Neal', 'To Be Kind']}

changed APIC to Music/music-library/Swans/To Be Kind(2014)/cover.jpg

```

Standardize all file and directory names in music library

```
> discognition Music/music-library -R -rn -rd
```

## License

MIT
