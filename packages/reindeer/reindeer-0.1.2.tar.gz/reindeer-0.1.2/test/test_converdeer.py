from unittest import TestCase
import numpy as np
import csv
from reindeer.converdeer import csv2ttl


class TestConverdeer(TestCase):
    def test_csv2ttl(self):
        test_input_file = './test_data/test_input_file.csv'
        test_output_file_actual = './test_data/test_output_file_a.ttl'
        test_output_file_expected = './test_data/test_output_file_e.ttl'
        csv2ttl(test_input_file, test_output_file_actual)
        with open(test_output_file_actual, 'r') as a:
            actual = a.read().replace('\n', '')
        with open(test_output_file_expected, 'r') as e:
            expected = e.read().replace('\n', '')
        self.assertEqual(expected, actual)
