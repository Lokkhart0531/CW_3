import pytest
from datetime import datetime
from dir.dto import Payment, Operation, Amount
import dir.utils

@pytest.fixture
def operation_data_with_from() -> dict:
    return {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    }

@pytest.fixture
def operation_data_without_from():
    return {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод с карты на карту",
        "to": "Visa Platinum 8990922113665229"
    }

def test_init_payment_from_str():
    payment = Payment.init_from_str('Visa Classic 6831982476737658')
    assert payment.name == 'Visa Classic'
    assert payment.number == '6831982476737658'

def test_safe_payment_for_amount():
    payment = Payment(name='Счет', number='64686473678894779589')
    assert payment.safe() == 'Счет **9589'

def test_safe_payment_for_card_number():
    payment = Payment(name='MasterCard', number='7158300734726758')
    assert payment.safe() == 'MasterCard 7158 30** **** 6758'

def test_split_card_number_by_blocks():
    card_number = '7158300734726758'
    result = Payment.split_card_number_by_blocks(number)
    assert result == '7158 3007 3472 6758'

def test_init_operation_from_dict(operation_data_without_from):
    data: dict = {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод с карты на карту",
        "to": "Visa Platinum 8990922113665229"
    }
    op = Operation.init_from_dict(data)
    assert op.id == 895315941
    assert op.state == 'EXECUTED'
    assert op.date == datetime(2018, 8, 19, 4, 27, 37, 904916)
    assert op.amount.value == 56883.54
    assert op.amount.currency_name == 'USD'
    assert op.amount.currency_code == 'USD'
    assert op.description == 'Перевод с карты на карту'
    assert op.payment_to.name == 'Visa Platinum'
    assert op.payment_to.number == '8990922113665229'
    assert op.payment_from is None

def test_save_operation_with_from(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    expected_result = (
        '19.08.2018 Перевод с карты на карту\n'
        'Visa Classic 6831 98** **** 7658 -> Visa Platinum 8990 92** **** 5229'
        '56883.54 USD'
    )
    assert operation.save() == expected_result

def test_save_operation_with_from(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)
    expected_result = (
        '19.08.2018 Перевод с карты на карту\n'
        'Visa Platinum 8990 92** **** 5229'
        '56883.54 USD'
    )
    assert operation.save() == expected_result