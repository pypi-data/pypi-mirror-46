## Django middleware for cassette.dev

Install with `pip install cassette-django`

Add `cassette_django` to your installed apps.

```
INSTALLED_APPS = [
    ...
    'cassette_django',
    ...
]
```

Add the middleware as at the end of the middleware list

```
MIDDLEWARE = [
    ...
    'cassette_django.middleware.CassetteMiddleware,
]
```

Now you're good to go! To import your API just install cassette's cli (`npm install -g @cassette.dev/cassette-cli` or read more at [npmjs.com](https://www.npmjs.com/package/@cassette.dev/cassette-cli))
and follow the instructions.