from __future__ import annotations


def yolo(value):
    return True


class TestModule(object):
    """ Distronode core jinja2 tests """

    def tests(self):
        return {
            # failure testing
            'yolo': yolo,
        }
