from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.views.generic import View


class FileServeView(View):
    authenticated_user_only = True
    content_type = None
    download_filename = None
    file = None
    has_permission = True
    is_download = True

    def error401(self, request, *args, **kwargs):
        return HttpResponse('Unauthorized', status=401)

    def error403(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def error404(self, request, *args, **kwargs):
        raise Http404()

    def get(self, request, *args, **kwargs):
        # 401 for non-authenticated users who should be authenticated
        if self.authenticated_user_only and not request.user.is_authenticated:
            return self.error401(request, *args, **kwargs)

        # get file
        self.get_file(request, *args, **kwargs)

        # 404 for no file
        if self.file is None:
            return self.error404(request, *args, **kwargs)

        # 403 for authenticated users who do not have permission
        if not self.has_permission:
            return self.error403(request, *args, **kwargs)

        return self.serve(request, *args, **kwargs)

    def get_content_type(self, request, *args, **kwargs):
        if self.content_type is None:
            try:
                suffix = self.file.lower().split('.')[-1:][0]
                # thank you:
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
                self.content_type = {
                    'aac': 'audio/aac',
                    'abw': 'application/x-abiword',
                    'arc': 'application/x-freearc',
                    'avi': 'video/x-msvideo',
                    'azw': 'application/vnd.amazon.ebook',
                    'bin': 'application/octet-stream',
                    'bmp': 'image/bmp',
                    'bz': 'application/x-bzip',
                    'bz2': 'application/x-bzip2',
                    'csh': 'application/x-csh',
                    'css': 'text/css',
                    'csv': 'text/csv',
                    'doc': 'application/msword',
                    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'eot': 'application/vnd.ms-fontobject',
                    'epub': 'application/epub+zip',
                    'gif': 'image/gif',
                    'htm': 'text/html',
                    'html': 'text/html',
                    'ico': 'image/vnd.microsoft.icon',
                    'ics': 'text/calendar',
                    'jar': 'application/java-archive',
                    'jpeg': 'image/jpeg',
                    'jpg': 'image/jpeg',
                    'js': 'text/javascript',
                    'json': 'application/json',
                    'jsonld': 'application/ld+json',
                    'mid': 'audio/midi audio/x-midi',
                    'midi': 'audio/midi audio/x-midi',
                    'mjs': 'text/javascript',
                    'mp3': 'audio/mpeg',
                    'mpeg': 'video/mpeg',
                    'mpkg': 'application/vnd.apple.installer+xml',
                    'odp': 'application/vnd.oasis.opendocument.presentation',
                    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
                    'odt': 'application/vnd.oasis.opendocument.text',
                    'oga': 'audio/ogg',
                    'ogv': 'video/ogg',
                    'ogx': 'application/ogg',
                    'otf': 'font/otf',
                    'png': 'image/png',
                    'pdf': 'application/pdf',
                    'ppt': 'application/vnd.ms-powerpoint',
                    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                    'rar': 'application/x-rar-compressed',
                    'rtf': 'application/rtf',
                    'sh': 'application/x-sh',
                    'svg': 'image/svg+xml',
                    'swf': 'application/x-shockwave-flash',
                    'tar': 'application/x-tar',
                    'tif': 'image/tiff',
                    'tiff': 'image/tiff',
                    'ttf': 'font/ttf',
                    'txt': 'text/plain',
                    'vsd': 'application/vnd.visio',
                    'wav': 'audio/wav',
                    'weba': 'audio/webm',
                    'webm': 'video/webm',
                    'webp': 'image/webp',
                    'woff': 'font/woff',
                    'woff2': 'font/woff2',
                    'xhtml': 'application/xhtml+xml',
                    'xls': 'application/vnd.ms-excel',
                    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'xml': 'application/xml',
                    'xul': 'application/vnd.mozilla.xul+xml',
                    'zip': 'application/zip',
                    '3gp': 'video/3gpp, *args, **kwargs',
                    '3g2': 'video/3gpp2',
                    '7z': 'application/x-7z-compressed'
                }[suffix]
            except:
                self.content_type = 'application/octet-stream'

    def get_file(self, request, *args, **kwargs):
        #
        # Add your own logic here to set the file, e.g.
        #     self.file = '....'
        #
        # The logic may decide that this user does not have
        # permission to see this file, therefore:
        #     self.has_permission = False
        #
        pass

    def serve(self, request, *args, **kwargs):
        # set the content_type (e.g. file mime type)
        if self.content_type is None:
            self.get_content_type(request, *args, **kwargs)

        # load file
        fp = open(self.file, 'rb')
        response = HttpResponse(fp.read(), content_type=self.content_type)
        response['Content-Length'] = len(response.content)
        fp.close()

        # download?
        if self.is_download:
            if self.download_filename is None:
                self.download_filename = \
                    self.file.replace('\\', '/').split('/')[-1:][0]
            response['Content-Disposition'] = 'attachment; filename="%s"' % \
                self.download_filename

        # serve
        return response
