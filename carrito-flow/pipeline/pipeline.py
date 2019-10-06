import argparse
import json
import logging
import sys

import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText, ReadFromPubSub
from apache_beam.options.pipeline_options import PipelineOptions


TOPIC = 'projects/PROJECT/topics/carrito'


class CarritoOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--output',
                                           dest='output',
                                           default='names',
                                           help='Output file to write results to.')


def run(argv=None):
    print(argv)
    pipeline_options = PipelineOptions()

    carrito_options = pipeline_options.view_as(CarritoOptions)

    with beam.Pipeline(options=pipeline_options) as p:
        (p
         | 'read' >> ReadFromPubSub(topic=TOPIC)
         | 'json' >> # ??
         | 'data' >> # ??
         | 'write' >> # ?? write to file
         )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run(sys.argv)
