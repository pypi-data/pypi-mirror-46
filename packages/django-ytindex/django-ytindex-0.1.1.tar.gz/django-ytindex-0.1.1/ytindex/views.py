from django.http import JsonResponse, Http404
from django.conf import settings

from .indexing import Index

def clean_hit( hit ):
    captions = [ dict( (*caption['_source'].items(), ('score', caption['_score'])) ) for caption in hit['inner_hits']['captions']['hits']['hits']]
    return dict( (*hit['_source'].items(), ('score', hit['_score']), ('captions',captions)) )

def search(request, index, query):
    if index not in settings.YTCI_SETTINGS.keys():
        raise Http404('Index %s does note exist'%index)
        
    idx = Index(**settings.YTCI_SETTINGS[index]['elastic'])
    r = idx.match_phrase(query)
    results = [ clean_hit(hit) for hit in r['hits']['hits'] ]
    ctx = {'results':results, 'query': query, 'index':index}
    return JsonResponse(ctx)
