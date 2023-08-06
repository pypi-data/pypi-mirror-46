from .esindex import ESIndex

class YTCaptionIndex(ESIndex):
    # YTCaptionIndex defines an ESIndex specific
    # to indexing and searching Youtube video captions
    class Meta:
        index_name = 'yt-captions'
        doc_type = 'yt-video'
        doc_id_tmpl = 'yt-video-%(id)s'
        mapping = {
          'properties': {
            'id': { 'type': 'text', 'index': 'false' },
            'upload_date': { 'type': 'date', 'index': 'false'  },
            'title': { 'type': 'text' },
            'description': { 'type': 'text', 'analyzer':'english' },
            'thumbnail': { 'type': 'text', 'index': 'false'  },
            'url': { 'type': 'text', 'index': 'false' },
            'captions': {
              'type': 'nested',
              'properties': {
                'start': {'type':'long', 'index': 'false' },
                'end': {'type':'long', 'index': 'false' },
                'content': {'type':'text', 'analyzer':'english'}
              }
            }
          }
        }

    def _search(self, query, query_type='match_phrase', size=20, from_=0):
        # This seems like a reasonable query for right now.
        # TODO: make better (Google has been working on theirs since 1994)
        q = { 'query': { 'bool': {
                'should': [{ 'nested': {
                            'path': 'captions',
                            'query': { query_type: {
                                'captions.content': query
                            }},
                            'inner_hits': {'size':10}
                        }},
                        {'match':{'description': query}}
                        ]}}}
        r = self._es.search(index=self.Meta.index_name, body=q, size=size, from_=from_)
        return r

    def get(self, id):
        return self._es.get(id=self.Meta.doc_id_tmpl%{'id':id}, index=self.Meta.index_name)

    def match(self, query, size=20, from_=0):
        return self._search(query, query_type='match', size=size, from_=from_)

    def match_phrase(self, query, size=20, from_=0):
        return self._search(query, query_type='match_phrase', size=size, from_=from_)
