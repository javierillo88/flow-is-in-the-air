# -*- coding: utf-8 -*-

import argparse
import json
import logging
import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions


class SwOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--input',
                                           dest='input',
                                           default='../dataset/people2.json',
                                           help='Input file specified a local or GCS path with json data.')

        parser.add_value_provider_argument('--output',
                                           dest='output',
                                           default='names',
                                           help='Output file to write results to.')


def run(argv=None):

    pipeline_options = PipelineOptions()

    sw_options = pipeline_options.view_as(SwOptions)

    with beam.Pipeline(options=pipeline_options) as p:
        (p
         | 'read' >> ReadFromText(sw_options.input)
         # Map to get only names
         | 'write' >> WriteToText(sw_options.output))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
