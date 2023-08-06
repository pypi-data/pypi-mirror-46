# -*- coding: utf-8 -*-
import unittest
import tempfile
import sys
from os import path

import shutil

from cpbox.tool import template
from cpbox.tool import file
from cpbox.tool import strings

from cpbox.tool.testutils import RandomDir

class TestTempalte(unittest.TestCase, RandomDir):

    def setUp(self):
        root_dir = path.dirname(path.realpath(sys.argv[0]))
        self.template_dir = path.join(root_dir, 'test-data')

        name = strings.random_str(10)
        self.temp_dir = path.join(root_dir, 'tmp-%s' % (name))
        file.ensure_dir(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        pass

    def test_render_to_file(self):
        data = {'date': '20190520'}
        str_after_render = '寒雨连江夜入吴 平明送客楚山孤 20190520'.encode('utf-8')
        template_file = path.join(self.template_dir, 'test-template-unicode.jinja2')
        ret = template.render_to_str(template_file, data)
        print(ret)
        print(str_after_render)
        self.assertEqual(ret, str_after_render)

        target_file = path.join(self.temp_dir, 'tmp')
        template.render_to_file(template_file, data, target_file)
        ret = file.file_get_contents(target_file)
        self.assertEqual(ret, str_after_render)

if __name__ == '__main__':
    unittest.main()
