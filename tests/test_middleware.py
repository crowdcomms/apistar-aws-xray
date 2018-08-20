import pytest
from apistar import App, Route, test
from apistar_aws_xray.event_hooks import AWSXrayEventHook
from aws_xray_sdk.core.context import Context
from tests.utils import get_new_stubbed_recorder




def all_good():
    return {'all':'good'}


def oh_noes():
    assert 'oh' == 'noes!'


routes = [
    Route('/all-good', method='GET', handler=all_good),
    Route('/oh-noes', method='GET', handler=oh_noes)
]


recorder = get_new_stubbed_recorder()
recorder.configure(service='test', sampling=False, context=Context())


event_hooks = [AWSXrayEventHook(recorder)]

app = App(routes=routes, event_hooks=event_hooks)

client = test.TestClient(app)




@pytest.fixture(autouse=True)
def cleanup():
    recorder.clear_trace_entities()
    yield
    recorder.clear_trace_entities()



def test_on_response():
    response = client.get('/all-good')
    assert response.status_code == 200

    segment = recorder.emitter.pop()
    assert not segment.in_progress

    request = segment.http['request']
    response = segment.http['response']

    assert request['method'] == 'GET'
    assert request['url'] == "http://testserver/all-good"
    assert response['status'] == 200
    assert response['content_length'] == 14


def test_fault():

    with pytest.raises(AssertionError):
        client.get('/oh-noes')

    segment = recorder.emitter.pop()
    assert not segment.in_progress

    request = segment.http['request']
    response = segment.http['response']
    assert request['method'] == 'GET'
    assert request['url'] == 'http://testserver/oh-noes'
    assert response['status'] == 500
    assert segment.fault

    exception = segment.cause['exceptions'][0]
    assert exception.type == 'AssertionError'