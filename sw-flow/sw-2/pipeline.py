# -*- coding: utf-8 -*-

import json
import logging

import apache_beam as beam
from apache_beam.io.gcp.datastore.v1.datastoreio import WriteToDatastore
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms import DoFn, ParDo


class ReadFromRest(DoFn):
    def __init__(self):
        super(ReadFromRest, self).__init__()

    def process(self, element, *args, **kwargs):
        def query(query_url):
            import requests
            headers = {'User-Agent': 'swapi-python'}
            response = requests.get(query_url, headers=headers)
            if response.status_code != 200:
                pass

            return response.content

        data = query(element)

        return [data]


class ReadFromApi(beam.PTransform):

    def __init__(self, entities):
        self._entities = entities

    def expand(self, pcoll):
        SWAPI_URL = 'https://swapi.co/api'

        entities = (pcoll.pipeline
                    | 'Creare entities list' >> beam.Create(self._entities)
                    | 'Composite urls' >> beam.Map(lambda entity: '{api}/{entity}'.format(api=SWAPI_URL, entity=entity))
                    | 'Request API' >> ParDo(ReadFromRest())
                    | 'Parse API response' >> beam.Map(lambda x: json.loads(x))
                    | 'Split response' >> beam.FlatMap(lambda x: x['results'])
                    )
        return entities


class EntityWrapper(object):
    """Create a Cloud Datastore entity from the given content."""
    def __init__(self, kind, namespace=None):
        self._namespace = namespace
        self._kind = kind

    def make_entity(self, content):
        import uuid
        from google.cloud.proto.datastore.v1 import entity_pb2
        from googledatastore import helper as datastore_helper

        entity = entity_pb2.Entity()
        if self._namespace.get() is not None:
            entity.key.partition_id.namespace_id = self._namespace.get()

        datastore_helper.add_key_path(entity.key, self._kind.get(), str(uuid.uuid4()))

        datastore_helper.add_properties(entity, content)
        return entity


class SwOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--dataset',
                            dest='dataset',
                            default='project-id',
                            required=False,
                            help='Project ID to read from Cloud Datastore.')
        parser.add_value_provider_argument('--kind',
                                           dest='kind',
                                           default='starships',
                                           required=False,
                                           help='Datastore Kind')
        parser.add_value_provider_argument('--namespace',
                                           dest='namespace',
                                           default='sw',
                                           help='Datastore Namespace')


def run(argv=None):

    pipeline_options = PipelineOptions()

    sw_options = pipeline_options.view_as(SwOptions)

    with beam.Pipeline(options=pipeline_options) as p:
        (p
         | 'read' >> # ???
         | 'name' >> beam.Map(lambda x: {'name': x['name']})
         | 'create entity' >> beam.Map(EntityWrapper(sw_options.kind, namespace=sw_options.namespace).make_entity)
         | 'write' >> WriteToDatastore(sw_options.dataset))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
