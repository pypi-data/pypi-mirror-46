django-file-serve-view
====

This small class-based view allows you to serve static files via Django.

A common use-case would be have a "downloads" section of your website, but the downloads are only available to certain users, i.e. where `user.is_authenticated == True` and, optionally, satisfy other criteria of your choosing.

---

To install:
 - `pip install django-file-serve-view`
 - Add `fileserveview` to your `INSTALLED_APPS` within `settings.py`.

---

Example #1: To serve file a file anyone can access, you can do something like this in your `urls.py`:
```
    path('robots.txt', FileServeView.as_view(
        authenticated_user_only=False,
        file=os.path.join(settings.STATIC_ROOT, 'robots.txt'),
        is_download=False
    )),
```
*Yes, I'm aware this is not the most efficient method of serving a robots file, but it illustrates the point*

---

Example #2: To serve a file only authenticated users can download, try:
```
    path('my-special-download', FileServeView.as_view(
        file=os.path.join(
            settings.BASE_DIR,
            '/path/to/get-rich-quick.pdf'
        ),
    )),
```

---

Example #3: To serve files based on a URL, you can extend the class as with some code such as:
```
    from fileserveview.views import FileServeView
    from myfiles.models import MyFile

    class MyDownloads(FileServeView):
        def get_file(self, request, *args, **kwargs):
            id = kwargs['id']
            slug = kwargs['slug']
            f = MyFile.objects.filter(id=id).filter(slug=slug).first()
            if f is not None:
                self.file = f.path

                # maybe we want to show PDFs in the browser
                if f.filetype == 'pdf':
                    self.download = False

                # who can see this file
                if not request.user.can_download:
                    self.has_permission = False
```
*It is likely the `get_file()` method is the only one you'd ever need to override with custom code.*

Then add something like this to your `urls.py`:
```
    path('downloads/<int:id>/<slug:slug>', MyDownloads.as_view()),
```
*I trust it is obvious that the above example is just an example. In this case you still need to create the MyFile model, whatever it may look like, and adjust the user Model to have a "can_download" attribute.*

---

Available parameters:
 - authenticated_user_only<br>Default: True<br>Does the visitor need to be authenticated (logged in) to see this file.

 - content_type<br>Default: None<br>The MIME type of the file. If not provided, it is calculated based on this list: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types. Alternatively, override the `get_content_type()` method.

 - download_filename<br>Default: None<br>An optional 'friendly' filename for the file sent to the user. For example, on your disk, the file may be "9e41fe35-cbb1-49b0-9e70-4ada17df7252", but the user's copy should be called "get-rich-quick.pdf"

 - file<br>Default: None<br>The path to the file to be downloaded, e.g. "/path/to/my-file.pdf"

 - has_permission<br>Default: True<br>If set to `False`, the user will see an 403 'Forbidden' error instead of the requested file. See "Example #3" above.

 - is_download<br>Default: True<br>By default the file is sent to the browser as an "attachment", i.e. a file sent to their "Downloads" folder. By setting this to False, the file is displayed in the browser (if the browser understands it)

---

To change the error messages, override the error401(), error403() and error404() methods. See the [source code](https://github.com/joncombe/django-file-serve-view/blob/master/fileserveview/views.py) for details.
