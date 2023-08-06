import os, json
from urllib import request
from xml.etree import ElementTree

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ytindex.indexing import Index
from ytindex.indexing.downloader import YTCaptionDownloader, YTCaptionNotFoundException

class Command(BaseCommand):
    help = 'A quick and dirty helper to ingest video ids from playlist json files.'

    def add_arguments(self, parser):
        parser.add_argument('index', type=str)
        parser.add_argument('path',  type=str)

    def handle(self, *args, **options):

        def index_video(ytid, idx):
            downloader = YTCaptionDownloader(ytid)
            idx.index_object(downloader.as_dict())

        index = options['index']
        path  = options['path']
        idx = Index(**settings.YTCI_SETTINGS[index]['elastic'])

        for fname in os.listdir(path):
            if fname.endswith('.json'):
                with open(os.path.join(path, fname),'r') as json_file:
                    print('Found file:', fname)
                    playlist = json.loads(json_file.read())
                    for entry in playlist['entries']:
                        print('Indexing:', entry['id'], end=' ')
                        try:
                            index_video(entry['id'], idx)
                            print('...done')
                        except YTCaptionNotFoundException as e:
                            print(e)
                        except Exception as e:
                            print('Most unexpected!!!', e)
