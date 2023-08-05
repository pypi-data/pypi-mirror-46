from ftw.simplelayout import _
from ftw.simplelayout.utils import IS_PLONE_5
from zExceptions import BadRequest
from zope.i18n import translate
from ftw.simplelayout.contenttypes.browser.dropzone import DropzoneUploadBase

if IS_PLONE_5:
    from plone.namedfile.utils import getImageInfo
else:
    # Plone 4
    from plone.namedfile.file import getImageInfo


class SliderBlockUpload(DropzoneUploadBase):

    def create(self, file_):
        content_type, width, height = getImageInfo(file_.read())
        file_.seek(0)
        if not content_type:
            error = translate(_('Only images can be added to the sliderblock.'),
                              context=self.request)
            raise BadRequest(error)

        return self.create_obj('ftw.slider.Pane', 'image', file_)
