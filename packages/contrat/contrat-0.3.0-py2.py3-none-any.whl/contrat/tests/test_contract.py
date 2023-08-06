import unittest


import contrat


def sample(arg1, arg2=False, arg3=1):
    pass


class TestContrat(unittest.TestCase):
    def test_getargspec(self):
        expected = (
            "ArgSpec(args=['arg1', 'arg2', 'arg3'], varargs=None, "
            "keywords=None, defaults=(False, 1))"
        )
        self.assertEqual(expected, str(contrat.getargspec(sample)))

    def test_getfullargspec(self):
        expected = (
            "FullArgSpec(args=['arg1', 'arg2', 'arg3'], "
            "varargs=None, varkw=None, defaults=(False, 1), "
            "kwonlyargs=[], kwonlydefaults=None, annotations={})"
        )
        if contrat.py2k:
            with self.assertRaises(AttributeError):
                contrat.getfullargspec(sample)
        else:
            self.assertEqual(expected, str(contrat.getfullargspec(sample)))
