import subprocess
from unittest import TestCase


class TestRender(TestCase):
    def test_render_time(self):
        subprocess.run(['python', 'main.py', '--test-run'])
