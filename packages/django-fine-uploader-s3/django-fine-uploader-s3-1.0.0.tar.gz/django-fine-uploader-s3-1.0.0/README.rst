=============================
Django Fine Uploader S3
=============================

.. image:: https://badge.fury.io/py/django-fine-uploader-s3.png
    :target: https://badge.fury.io/py/django-fine-uploader-s3


Your project description goes here

Quickstart
----------

Install Django Fine Uploader S3::

    pip install django-fine-uploader-s3

Then use it in a project::

    # settings.py
    installed_apps = [
        ...
        'django_fine_uploader_s3',
        ...
    ]

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_CLOUDFRONT_DOMAIN = os.environ.get("AWS_CLOUDFRONT_DOMAIN")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")

    # urls.py
    urlpatterns = [
        ...
         url(r'^fine-uploader/', include('django_fine_uploader_s3.urls')),
        ...
    ]

Refer `fine-uploader.html`_

S3 Bucket Configuration:
-----------------------

::

    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>GET</AllowedMethod>
            <MaxAgeSeconds>3000</MaxAgeSeconds>
            <AllowedHeader>Authorization</AllowedHeader>
        </CORSRule>
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>HEAD</AllowedMethod>
            <AllowedMethod>GET</AllowedMethod>
            <AllowedMethod>PUT</AllowedMethod>
            <AllowedMethod>POST</AllowedMethod>
            <AllowedMethod>DELETE</AllowedMethod>
            <ExposeHeader>ETag</ExposeHeader>
            <ExposeHeader>x-amz-meta-custom-header</ExposeHeader>
            <AllowedHeader>*</AllowedHeader>
        </CORSRule>
    </CORSConfiguration>


Other Projects:
--------------

* `zappa_file_widget`_

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_
*  `django-fine-uploader-s3`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _django-fine-uploader-s3: https://github.com/FineUploader/server-examples/blob/master/python/django-fine-uploader-s3
.. _fine-uploader.html: https://github.com/anush0247/django-fine-uploader-s3/blob/master/django_fine_uploader_s3/fine-uploader.html
.. _zappa_file_widget: https://github.com/anush0247/zappa-file-widget
