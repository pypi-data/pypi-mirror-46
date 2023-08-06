Ranch
=====

Standardized tooling, monitoring, and retry logic for use with Celery

## Installation

Ranch is a Django application. To use Ranch with Celery, add the following to your settings file:

```python
INSTALLED_APPS = [
    ...
    'mbq.ranch'
]

RANCH = {
    'env': ENV_NAME,  # e.g. production, development
    'service': MY_SERVICE_NAME,  # e.g. os-core
}
```

## Features

### Metrics

Any application with Ranch installed will have Celery metrics available in [the Celery/Ranch DataDog Dashboard](https://app.datadoghq.com/dash/930140/celery--ranch).

### Monitors

*TODO: Include link to Invoice's monitors once they're built*

You may set up monitors for your application using the metrics provided by Ranch. To get started, you might want to copy Invoicing's monitors.

### Dead Letter Queue

Celery jobs that fail will be stored in the application's database for inspection and reprocessing. Ranch provides an Admin interface for this.

See [OS Core's Ranch Admin](https://api.managedbyq.com/admin/ranch/loggedtask/) for an example.

### Correlation IDs

Ranch can flow correlation IDs through your Celery jobs. Ranch will *not* change any of your logging configuration, so you'll still need to do that as part of your correlation ID implementation.

To use the correlation ID functionality, add the following settings:

```python
RANCH = {
    ...,
    'correlation': {
        'getter': getter_fn,  # callable with no args that returns the current correlation ID
        'setter': setter_fn,  # callable with one arg which should be set as the current correlation ID
    },
}
```

### Supplemental Error Tagging

Ranch provides a hook to add additional tagging information to error item metrics. This is used in OS Core to tag each error as belonging to a specific team.

To use this feature, add the following settings:

```python
RANCH = {
    ...,
    # tags_fn takes a single arg (the Ranch Task object that failed)
    # and should return a list of strings in the format "tag_name:tag_value"
    # See OS Core's usage for an example
    'extra_error_queue_tags_fn': tags_fn,
}
```
