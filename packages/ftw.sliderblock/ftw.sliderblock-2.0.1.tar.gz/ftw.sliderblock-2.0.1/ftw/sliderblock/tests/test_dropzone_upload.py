from ftw.builder import Builder
from ftw.builder import create
from ftw.sliderblock.tests import FunctionalTestCase
from ftw.testbrowser import browser as defaultbrowser
from ftw.testbrowser import browsing
from plone.protect import createToken


class TestDropZoneUpload(FunctionalTestCase):

    def setUp(self):
        super(TestDropZoneUpload, self).setUp()
        self.grant('Manager')

    @browsing
    def test_sliderblock_has_dropzone(self, browser):
        sliderblock = create(Builder('sliderblock').titled(u'Slider Block')
                             .within(
            create(Builder('sl content page').titled(u'Page'))))

        browser.login().visit(sliderblock, view='block_view')
        dropzone_elements = browser.css('.dropzonewrapper')

        self.assertTrue(dropzone_elements.first,
                        'We expect that we find the css selector of the '
                        'dropzonewrapper in the sliderblock.')

    @browsing
    def test_create_images_in_sliderblock(self, browser):
        sliderblock = create(Builder('sliderblock').titled(u'Slider Block')
                             .within(
            create(Builder('sl content page').titled(u'Page'))))
        self.assertEquals([], sliderblock.objectIds())

        browser.login()
        self.make_dropzone_upload(sliderblock,
                                  self.asset('image.jpg').open('rb'))
        self.assertEqual(201, browser.status_code)
        self.assertEqual({u'content': u'Created',
                          u'url': u'http://nohost/plone/page/slider-block/image.jpg',
                          u'proceed': True}, browser.json)
        self.assertEquals(['image.jpg'], sliderblock.objectIds())

        img, = sliderblock.objectValues()

        self.assertEquals('ftw.slider.Pane', img.portal_type)
        self.assertEquals('image.jpg', img.Title())

    @browsing
    def test_files_are_not_allowed_in_galleries(self, browser):
        sliderblock = create(Builder('sliderblock').titled(u'Slider Block')
                             .within(
            create(Builder('sl content page').titled(u'Page'))))
        self.assertEquals([], sliderblock.objectIds())

        with browser.login().expect_http_error(400):
            self.make_dropzone_upload(sliderblock,
                                      self.asset('textfile.txt').open('r'))

        self.assertEqual(
            {u'error': u'Only images can be added to the sliderblock.',
             u'proceed': False}, browser.json)
        self.assertEquals([], sliderblock.objectIds())

    @staticmethod
    def make_dropzone_upload(context, file_):
        """The dropzone JS makes a multipart upload with the the file as field named "file".
        The testbrowser does not support making multipart requests directly (we would have to
        create the MIME body ourself), but the form filling does that well.
        Therefore we use an HTML form for uploading.
        """
        html = (
            '<form action="{}/@@dropzone-upload" method="post" enctype="multipart/form-data">'
            '  <input type="file" name="file" />'
            '  <input type="hidden" name="_authenticator" value="{}" />'
            '  <input type="submit" />'
            '</form>').format(context.absolute_url(), createToken())
        defaultbrowser.open(context).parse(html)
        defaultbrowser.fill({'file': file_}).submit()
        return defaultbrowser
