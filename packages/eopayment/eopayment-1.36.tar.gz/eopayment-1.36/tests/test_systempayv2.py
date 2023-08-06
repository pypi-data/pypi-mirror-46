# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytest
from six.moves.urllib import parse as urlparse

import eopayment
from eopayment.systempayv2 import Payment, VADS_CUST_FIRST_NAME, \
    VADS_CUST_LAST_NAME, PAID
from eopayment import ResponseError

PARAMS = {
    'secret_test': u'1122334455667788',
    'vads_site_id': u'12345678',
    'vads_ctx_mode': u'TEST',
    'vads_trans_date': u'20090501193530',
}


def get_field(form, field_name):
    for field in form.fields:
        if field['name'] == field_name:
            return field


def test_systempayv2():
    p = Payment(PARAMS)
    data = {'amount': 15.24, 'orderid': '654321',
            'first_name': u'Jean Michél',
            'last_name': u'Mihaï'
    }
    qs = 'vads_version=V2&vads_page_action=PAYMENT&vads_action_mode=INTERACTIV' \
         'E&vads_payment_config=SINGLE&vads_site_id=12345678&vads_ctx_mode=TES' \
         'T&vads_trans_id=654321&vads_trans_date=20090501193530&vads_amount=15' \
         '24&vads_currency=978&vads_cust_first_name=Jean+Mich%C3%A9l&vads_cust_last_name=Mihaï'
    qs = urlparse.parse_qs(qs)
    for key in qs.keys():
        qs[key] = qs[key][0]
    assert p.signature(qs) == 'cf1ccac335590a33d6c243345c4f4531a0316b7f'
    transaction_id, f, form = p.request(**data)

    # check that user first and last names are unicode
    for field in form.fields:
        if field['name'] in (VADS_CUST_FIRST_NAME, VADS_CUST_LAST_NAME):
            assert field['value'] in (u'Jean Michél', u'Mihaï')

    response_qs = 'vads_amount=1042&vads_auth_mode=FULL&vads_auth_number=3feadf' \
                  '&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB' \
                  '&vads_card_number=497010XXXXXX0000' \
                  '&vads_payment_certificate=582ba2b725057618706d7a06e9e59acdbf69ff53' \
                  '&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1042' \
                  '&vads_site_id=70168983&vads_trans_date=20161013101355' \
                  '&vads_trans_id=226787&vads_trans_uuid=4b5053b3b1fe4b02a07753e7a' \
                  '&signature=62a4fb6738ebadebf9cc720164bc70e47282d36e'
    response = p.response(response_qs)
    assert response.result == PAID

    # bad response
    with pytest.raises(ResponseError, match='missing signature, vads_ctx_mode or vads_auth_result'):
        p.response('foo=bar')


def test_systempayv2_deferred_payment():
    default_params = {
        'secret_test': u'1122334455667788',
        'vads_site_id': u'12345678',
        'vads_ctx_mode': u'TEST',
    }
    default_data = {
        'amount': 15.24, 'orderid': '654321', 'first_name': u'John',
        'last_name': u'Doe'
    }

    # default vads_capture_delay used
    params = default_params.copy()
    params['vads_capture_delay'] = 1

    backend = eopayment.Payment('systempayv2', params)
    data = default_data.copy()
    transaction_id, f, form = backend.request(**data)
    assert get_field(form, 'vads_capture_delay')['value'] == '1'

    # vads_capture_delay can used in request and
    # override default vads_capture_delay
    params = default_params.copy()
    params['vads_capture_delay'] = 1
    p = eopayment.Payment('systempayv2', params)
    data = default_data.copy()
    data['vads_capture_delay'] = '3'
    transaction_id, f, form = p.request(**data)
    assert get_field(form, 'vads_capture_delay')['value'] == '3'

    # capture_date can be used for deferred_payment
    params = default_params.copy()
    params['vads_capture_delay'] = 1
    p = eopayment.Payment('systempayv2', params)
    data = default_data.copy()
    data['capture_date'] = (datetime.now().date() + timedelta(days=4))
    transaction_id, f, form = p.request(**data)
    assert get_field(form, 'vads_capture_delay')['value'] == '4'


def test_manual_validation():
    params = {
        'secret_test': u'1122334455667788',
        'vads_site_id': u'12345678',
        'vads_ctx_mode': u'TEST',
    }
    data = {
        'amount': 15.24, 'orderid': '654321', 'first_name': u'John',
        'last_name': u'Doe'
    }

    backend = eopayment.Payment('systempayv2', params)
    transaction_id, f, form = backend.request(**data.copy())
    assert get_field(form, 'vads_validation_mode')['value'] == ''

    data['manual_validation'] = True
    transaction_id, f, form = backend.request(**data.copy())
    assert get_field(form, 'vads_validation_mode')['value'] == '1'
