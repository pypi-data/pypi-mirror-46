import eopayment
import pytest

def test_dummy():
    options = {
            'direct_notification_url': 'http://example.com/direct_notification_url',
            'siret': '1234',
            'origin': 'Mairie de Perpette-les-oies'
    }
    p = eopayment.Payment('dummy', options)
    retour = 'http://example.com/retour?amount=10.0&direct_notification_url=http%3A%2F%2Fexample.com%2Fdirect_notification_url&email=toto%40example.com&transaction_id=6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T&return_url=http%3A%2F%2Fexample.com%2Fretour&nok=1'
    r = p.response(retour.split('?',1)[1])
    assert not r.signed
    assert r.transaction_id == '6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
    assert r.return_content is None
    retour = 'http://example.com/retour?amount=10.0&direct_notification_url=http%3A%2F%2Fexample.com%2Fdirect_notification_url&email=toto%40example.com&transaction_id=6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T&return_url=http%3A%2F%2Fexample.com%2Fretour&ok=1&signed=1'
    r = p.response(retour.split('?',1)[1])
    assert r.signed
    assert r.transaction_id == '6Tfw2e1bPyYnz7CedZqvdHt7T9XX6T'
    assert r.return_content == 'signature ok'

    data = {'foo': 'bar'}
    with pytest.raises(eopayment.ResponseError, match='missing transaction_id'):
        p.response('foo=bar')
