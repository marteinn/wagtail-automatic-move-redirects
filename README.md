# wagtail-automatic-move-redirects

This package does one thing, it makes sure a redirect is created every time a published page is moved in the Wagtail admin.

## Installation

1. First make sure you activate Wagtail redirects, you can do this by following this [official guide](https://docs.wagtail.io/en/latest/reference/contrib/redirects.html#installation)

2. Then install this package by running

```
python -m pip install git+https://github.com/marteinn/wagtail-automatic-move-redirects
```

3. Add the package to your project's settings

```python
INSTALLED_APPS = [
    # ... Other apps
    "wagtail_automatic_move_redirects",
    "wagtail.contrib.redirects",
    # ... Other apps
]
```

4. Done!

## Credits

This is library originated as a fork of [wagtail-automatic-redirects](https://github.com/themotleyfool/wagtail-automatic-redirects).


## License

[BSD](https://github.com/themotleyfool/wagtail-automatic-move-redirects/blob/master/LICENSE)
