Usage
-----

.. code-block:: python

    from aws_xray_sdk.core import xray_recorder
    from apistar_aws_xray.event_hooks import AWSXrayEventHook

    xray_recorder.configure(service='my-service')

    event_hooks = [AWSXrayEventHook(xray_recorder)]

    app = App(
        ...
        event_hooks = event_hooks
    )