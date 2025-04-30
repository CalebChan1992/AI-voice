# Backend Requirements Update for Testing

To add testing capabilities to your backend, you'll need to install pytest and related packages. Here's what you should add to your requirements:

```
pytest==7.4.4
pytest-flask==1.3.0
pytest-cov==4.1.0
```

To install these packages, run the following command in your backend directory:

```bash
pip install pytest pytest-flask pytest-cov
```

You can then run your tests with:

```bash
pytest ../test/backend
```

For coverage reports, use:

```bash
pytest ../test/backend --cov=app
```
