# wagtail-automatic-move-redirects

Creates a automatic redirect every time a published page is moved. Please note that this is an experiment, for production, use [wagtail-automatic-redirects](https://github.com/themotleyfool/wagtail-automatic-redirects), it covers a wider range of usages.

## Installation

    install the package through the pip git feature

Add the package to your project's settings

```python
INSTALLED_APPS = [
    # ... Other apps
    "wagtail_automatic_redirects",
    "wagtail.contrib.redirects",
    # ... Other apps
]
```

Make sure the `INSTALLED_APPS` setting include `"wagtail.contrib.redirects",` app from Wagtail.

Also, check the `MIDDLEWARE` setting include

```python
MIDDLEWARE = [
    # ... Other middlewares
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # ... Other middlewares
]
```

## Credits

This is library started of as a fork to the great [wagtail-automatic-redirects](https://github.com/themotleyfool/wagtail-automatic-redirects) 


## License

[BSD](https://github.com/themotleyfool/wagtail-automatic-redirects/blob/master/LICENSE)
