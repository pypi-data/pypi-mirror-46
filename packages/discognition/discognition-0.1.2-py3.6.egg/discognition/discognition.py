#!/usr/bin/python3

import discogs_client
import re
import sys
import os
import mutagen.id3
import urllib.request
import time
import subprocess
import yaml
from pathlib import Path

from discognition.parser import args
from discognition.version import __version__

def configure():
    config_file = str(Path.home())+"/.discognition-conf.yaml"

    if args.generateconfig is not None: # generate configuration

        data = {
            'token': args.generateconfig[0],
            'directory': args.generateconfig[1]
        }
        
        with open(config_file, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

        print('created file: ' + config_file)

    try:
        config = yaml.safe_load(open(config_file))
        client = discogs_client.Client('discognition/'+__version__, user_token=config['token'])

    except:
        print('You need to set your configuration file at "~/.discogs_conf.yaml"')
        print('You can do this by running "discognition -g TOKEN /PATH/TO/MUSIC/LIBRARY"')
        exit()

    

    return {
        'config': config,
        'client': client,
    }


###########

def getData(discogs_search_str, interactive, client, num_files, search_limit=10):

    regex = re.search('(^|release/)([0-9]+)$', discogs_search_str)

    if bool(regex):

        album = client.release(regex.group(2))

    else:
    
        results = client.search(discogs_search_str, type='release')

        found = False
        hits = len(results)
        if hits is 0:
            print('album not found. exiting...')
            sys.exit()
        elif hits is 1 or (num_files is None and not interactive):
            print('found '+ str(hits) +' album(s)...')
            album = results[0]
            print('\nusing album: ' + album.title)
            print(album.url)

        elif not interactive:
            print('found '+ str(hits) +' album(s)...')
            index = 0

            while index < search_limit:
                album = results[index]

                if len(album.tracklist) is num_files:
                    print('\nusing album: ' + album.title)
                    print(album.url)
                    break

                else:
                    print('\nalbum (' + album.url + ') has wrong number of tracks. trying another...')
                    index += 1
                    time.sleep(.5)

            if index is search_limit: 
                print('\nyour query did not return a match in the first ' + str(search_limit) + ' results.')
                print( 'your search may be incorrect or you may be missing track files.')
                print('\nexiting...')
                exit()
        else:
            print('searched for '+ discogs_search_str)

            result_num = 0
            while not found:
                album = results[result_num]
                found = getInput([
                    album.title + ' (' + album.year + ')',
                    str(len(album.tracklist)) + ' tracks on ' + album.formats[0]['name'],
                    album.url,
                    ])[0]
                if not found: result_num = result_num + 1

            print('\nusing album: ' + album.title)
            print(album.url)

    artists_list = []
    for a in album.artists:
        artists_list.append(re.sub(' \([0-9]+\)$','',a.name)) # remove numbers used to distinguish artists on discogs
    artist=", ".join(artists_list)

    discogs_track_list = album.tracklist


    track_titles = []
    tracklist = album.tracklist
    
    track_data = iterateDiscogsTracks(album.tracklist, ['title'])

    master = False
   
    try:
        image = album.master.images[0]['uri'] # master release tends to have more consistent image quality, when it exists
        master = True
    except:
        try:
            image = album.images[0]['uri']
        except:
            image = None

    if master:
        if len(album.master.versions) < 10: # try not to make API unhappy
            first_release = 9999
            for r in album.master.versions:
                time.sleep(.5) # if there are many versions, can throw 'discogs_client.exceptions.HTTPError: 429: You are making requests too quickly.'
                if r.year < first_release and r.year is not 0:
                    first_release = r.year
                    label_list = r.labels
        else:
            first_release = album.master.main_release.year
            label_list = album.master.main_release.labels

    else:
        label_list = album.labels
        first_release = album.year

    # concatenate labels into string if multiple are given
    if len(label_list) is 1:
        label = re.sub(' \([0-9]+\)$','', label_list[0].name)
    else:
        label_name_list = []
        for l in label_list:
            label_name_list.append(re.sub(' \([0-9]+\)$','', l.name))
        label = ", ".join(label_name_list)


    '''
    additional available Discogs API data:

    id
    status
    genres
    country
    notes
    styles
    url
    tracklist
    credits
    companies

    '''

    return {         #  structured data for directory path and metadata tagging
        
        'TALB' : album.title,
        'TPE1' : artist,
        'TPUB': label,
        'TDRC': first_release,
        'image_url' : image,
        'tracks' : track_data,

        #'genres' : album.genres
        #'country' : album.country 
        #'styles' : album.styles 

    }




def iterateDiscogsTracks(tracklist, fields):

    ret = {field: [] for field in fields}

    for i, track in enumerate(tracklist):

        # remove multi-track movements that register as tracks,
        if len(track.position) is not 0: 
            
            # keep titles from single tracks that are composed of two pieces from different composers
            try: 
                # i.e., flag 4b, but not 4a, A4, B4, B, 4, etc.
                # (some vinyl has 1A, 2A  instead of A1, A2...)
                actually_one_track = bool(re.search('^[0-9]+?[B-Zb-z]$', track.position)) and not \
                track.position[1:].startswith(tracklist[i-1].position[1]) and \
                track.position[0] == tracklist[i-1].position[0]
            except: 
                actually_one_track = False

            if actually_one_track:
                for f in fields:
                    ret[f][-1] = ret[f][-1] + '/' + getattr(track,f)
            else:
                [ret[f].append(getattr(track,f)) for f in fields]
                    
    return ret
                


def renameTracks(files, album_dir, data, pattern=None):

    same = True
    new_paths = []

    for n, track in enumerate(files):

        tracknum = "{0:0=2d}".format(n+1) # format as 01, 02... 09, 10, 11, ... etc.
        pattern = '%s-%s.mp3' % (tracknum, data['tracks']['title'][n])
        new_fn = album_dir + pattern
        os.rename(track, new_fn)
        new_paths.append(new_fn)

        if not files[n] == new_fn: same = False

    if same: print("\nexisting filenames already match output format.")
    else: print('\nfiles successfully renamed.')
    
    return new_paths


def renameDirs(album_dir, data, mus_lib, pattern=None):

    pattern = '%s/%s (%s)/' % (data['TPE1'], data['TALB'], data['TDRC'])

    new_dir_name = mus_lib + pattern

    if new_dir_name == album_dir: 
        print('\ndirectory name is already ' + album_dir)
        print('directory will not be renamed')
        return album_dir

    elif os.path.isdir(new_dir_name):
        print('\nalready a directory with name ' + new_dir_name)
        print('unable to change name')
        return album_dir

    else:
        print('\nchanging directory name from \n' + album_dir + ' \nto: \n' + new_dir_name)
        os.rename(album_dir, new_dir_name)
        return new_dir_name


def getTracks(path):

    tracks = []

    if not os.path.isdir(path): # if artist/album path is not valid, do nothing
        print("No directory for '" + path + "'")
        return []
    else:
        tracks = [path + file for file in os.listdir(path) if file.endswith('.mp3')]
        if len(tracks) is 0:
            print('No mp3s found in ' + path)
            return []
        return sorted(tracks)


def read_ID3(file):

    return mutagen.id3.ID3(file)


def setMetadata (data, filelist, album_dir, update_fields):

    synonyms = {

        'label': 'TPUB',
        'publisher': 'TPUB',

        'year': 'TDRC',
        'date': 'TDRC',

        'artist': 'TPE1',

        'title': 'TIT2',
        'track': 'TIT2',
        'name': 'TIT2',

        'album': 'TALB',

        'tracknumber': 'TRCK',

        'image': 'APIC',
        'art': 'APIC',
        'cover': 'APIC',
        'picture': 'APIC',
        'pic': 'APIC',
        'albumcover': 'APIC',

        }

    tags = []

    for field in update_fields:
        if field in data:
            tags.append(field)
        elif field in synonyms:
            tags.append(synonyms[field])
        elif field == 'all':
            tags = list(set(synonyms[k]for k in synonyms))
        else:
            print('tag ' + field + ' not supported.')

    
    for i, f in enumerate(filelist):
        for tag in tags:
            #print(tag)
            m = mutagen.id3.ID3(f)

            # TODO:
            #
            # - there is a better way of doing this... requires using variable with getattr/setattr,
            # (i.e., mutagen.id3.*tag*) but seems to fail with mutagen.id3 
            #
            # - if data has already been set to value, do not print change message

            if 'TPUB' in tag:
                m.add(mutagen.id3.TPUB(encoding=3, text=data[tag])) # record label
                if i is 0: print('\nchanged ' + tag + ' to ' + str(data[tag]))
            if 'TALB' in tag:    
                m.add(mutagen.id3.TALB(encoding=3, text=data[tag])) # album title
                if i is 0: print('\nchanged ' + tag + ' to ' + str(data[tag]))
            if 'TPE1' in tag:    
                m.add(mutagen.id3.TPE1(encoding=3, text=data[tag])) # artist
                if i is 0: print('\nchanged ' + tag + ' to ' + str(data[tag]))
            if 'TDRC' in tag:    
                m.add(mutagen.id3.TDRC(encoding=3, text=str(data[tag]))) # year
                if i is 0: print('\nchanged ' + tag + ' to ' + str(data[tag]))

            #track_change = '\n'
            if 'TIT2' in tag:
                title = data['tracks']['title'][i]
                m.add(mutagen.id3.TIT2(encoding=3, text=title)) # track title
                print('\nchanged ' + f +'\'s ' + tag + ' to ' + title)
            if 'TRCK' in tag:
                tracknum = str(i+1)    
                m.add(mutagen.id3.TRCK(encoding=3, text=tracknum)) # track number
                print('\nchanged ' + f +'\'s ' + tag + ' to ' + tracknum)
            if 'APIC' in tag and data['image_url'] is not None:
                image = dl_cover(data['image_url'], album_dir)
                m.add(mutagen.id3.APIC(encoding=3, mime = 'image/jpeg', type=3, desc=u'Cover', data=open(image, 'rb').read())) # embed album art
                if i is 0: print('\nchanged APIC to ' + image)

            m.save()

def dl_cover(url, path): 

    out = path + 'cover.jpg'
    urllib.request.urlretrieve(url, out)
    return out 


def queryTracks(data, filelist):

    return len(filelist) is len(data['tracks']['title'])


def get_mp3_dirs(big_dir):
    
    return [x[0] for x in os.walk(big_dir) if len(getTracks(x[0])) is not 0] 

yes = {'yes','y', 'ye', ''}
no = {'no','n'}

def getInput(info):
    print('\nDo you want: ')
    [print(i) for i in info]
    print('(y/n)? ')

    choice = input().lower()
    if choice in yes:
       return [True, info]
    elif choice in no:
       return [False, info]
    else:
       sys.stdout.write("Please respond with '(y)es' or '(n)o'")






def main():

    c = configure()

    client = c['client']
    music_lib = c['config']['directory']

    if args.directory is not None:

        if args.recursive:
            albumdirectories = get_mp3_dirs(args.directory)
            print('\nfound the following directories with mp3s:')
            [print(a) for a in albumdirectories]

        else: albumdirectories = [args.directory]

        for i, albumdirectory in enumerate(albumdirectories):

            if not albumdirectory.endswith('/'): albumdirectory = albumdirectory + '/'

            files = getTracks(albumdirectory)
            
            if len(files) is 0: exit()
          
            if args.search is not None:

                discogs_query = args.search

            else:

                id3_data = read_ID3(files[0])
                discogs_query = str(id3_data["TALB"]) + ' ' + str(id3_data["TPE1"])

            print('\nsearching Discogs for "' + discogs_query + '"...')

            discogs_data = getData(discogs_query, args.interactive, client, len(files))


            if args.tag is None and not args.renametracks and not args.renamedirectories:
                print()
                for datum in discogs_data:
                    print (datum, ':', discogs_data[datum])

            else:

                if args.print:
                    print()
                    for datum in discogs_data:
                        print (datum, ':', discogs_data[datum])


                if queryTracks(discogs_data, files):

                    if args.tag is not None:

                        setMetadata(discogs_data, files, albumdirectory, args.tag)
                      
                    if args.renametracks: 

                        files = renameTracks(files, albumdirectory, discogs_data)
                        print('new file names: ')
                        for f in files:
                            print(os.path.basename(f))

                    if args.renamedirectories:

                        albumdirectory = renameDirs(albumdirectory, discogs_data, music_lib )

                else:

                    print('number of files and number of Discogs tracks do not match.')
                    print('exiting...')

            if i is not len(albumdirectories)-1: time.sleep(4) # try not to send too many requests to Discogs


    elif args.search is not None:

        discogs_query = args.search

        print('searching Discogs for "' + discogs_query + '"...')

        discogs_data = getData(discogs_query, args.interactive, client, None)

        for datum in discogs_data:

            print (datum, ':', discogs_data[datum])

    else:
        if args.generateconfig is None:
            print("please specify album or search")
            print('exiting...')
        exit()


if __name__ == '__main__':
    main()