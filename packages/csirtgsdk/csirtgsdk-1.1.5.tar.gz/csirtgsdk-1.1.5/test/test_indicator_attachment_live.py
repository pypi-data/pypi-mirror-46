import pytest
import os
from csirtgsdk.indicator import Indicator
from csirtgsdk.feed import Feed
from csirtgsdk.client.http import HTTP as Client
from time import sleep

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')
FEED = os.environ.get('CSIRTG_FEED', 'ci_attachment_test')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")

@pytest.fixture
def client():
    return Client(
        token=TOKEN,
        remote=REMOTE
    )

@liveonly
def test_indicator_attachment_txt(client):
    sleep(3)
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/message.eml',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    # assert r['indicator'] == '2f9496a6331b2e75e5208b93d144e8fe484b316a'
    # assert r['attachments'][0]['attachment']
    # assert r['attachments'][0]['filesize']
    # assert r['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200

@liveonly
def test_indicator_attachment_zip(client):
    sleep(3)
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/malware.jar.zip',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator'] == 'f31e226048d9bd45513e691a50a4b83893397235'
    # assert r['attachments'][0]['attachment']
    # assert r['attachments'][0]['filesize']
    # assert r['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_attachment_jar(client):
    sleep(3)
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/malware.jar',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator'] == '8ab0079d8e80c2e166b3b12364c89255d79c9f75'
    # assert r['attachments'][0]['attachment']
    # assert r['attachments'][0]['filesize']
    # assert r['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200

@liveonly
def test_indicator_attachment_docx(client):
    sleep(3)
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/c..docx',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator'] == 'c2642e519c7f325300ed250710b4f815ac542c1d'
    # assert r['attachments'][0]['attachment']
    # assert r['attachments'][0]['filesize']
    # assert r['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200

@liveonly
def test_indicator_attachment_doc(client):
    sleep(3)
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/business_relationship.doc',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator'] == 'f0ee0d5a1279fbdd93a9c5b9a1377894113f0ec0'
    # assert r['attachments'][0]['attachment']
    # assert r['attachments'][0]['filesize']
    # assert r['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200

@liveonly
def test_indicator_attachment_pdf(client):
    sleep(3)
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/hello_world.pdf',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator'] == 'cc9881dc27a8d3e410cdf7e667ff5efa5cbfdaed'
    # assert r['attachments'][0]['attachment']
    # assert r['attachments'][0]['filesize']
    # assert r['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200
