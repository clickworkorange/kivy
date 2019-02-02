import unittest
import io
import os
import tempfile


class ImageTestCase(unittest.TestCase):

    def setUp(self):
        from kivy.core.window import Window
        from kivy.core.image import Image
        import os
        self.cls = Image
        self.image = os.path.join(os.path.dirname(__file__), 'test_button.png')
        print(self.image)
        self.root = Image(self.image)

    def test_keep_data(self):
        root = self.root
        texture = root.texture
        self.assertEqual(root._image._data[0].data, None)
        i1 = self.cls(self.image, keep_data=True)
        if not i1._image._data[0].data:
            self.fail('Image has no data even with keep_data = True')

    def test_save_into_bytesio(self):
        Image = self.cls

        # load kivy logo
        img = Image.load("data/logo/kivy-icon-512.png")
        self.assertIsNotNone(img)

        # try to save without any format
        with self.assertRaises(Exception) as context:
            bio = io.BytesIO()
            img.save(bio)

        # save it in png
        bio = io.BytesIO()
        self.assertTrue(img.save(bio, fmt="png"))  # if False, then there is no provider
        pngdata = bio.read()
        self.assertTrue(len(pngdata) > 0)

        # try to save in a filename
        try:
            _, filename = tempfile.mkstemp(suffix=".png")
            self.assertTrue(img.save(filename, fmt="png"))
        finally:
            os.unlink(filename)

        # XXX Test wrote but temporary commented
        # XXX because of the issue #6123 on OSX
        # XXX https://github.com/kivy/kivy/issues/6123
        # with open(filename, "rb") as fd2:
        #     pngdatafile = fd2.read()
        # # check the png file data is the same as bytesio
        # self.assertTrue(pngdata == pngdatafile)

        # save it in jpeg
        bio = io.BytesIO()
        self.assertTrue(img.save(bio, fmt="jpg"))  # if False, then there is no provider
        self.assertTrue(len(bio.read()) > 0)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as fd:
            self.assertTrue(img.save(fd.name))
