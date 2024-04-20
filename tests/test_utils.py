import pytest
from dir.dto import Operation
from tests.test_dto import operation_data_with_from
from dir.utils import filter_operation_by_state

@pytest.fixture
def executed_operation(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    operation.state = 'EXECUTED'
    return operation

@pytest.fixture
def canceled_operation(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    operation.state = 'CANCELED'
    return operation

def test_filtered_operations(executed_operation, canceled_operation):
    operation = executed_operation, canceled_operation
    result = filter_operation_by_state(*operation, state='EXECUTED')
    assert result == [executed_operation]

    result = filter_operation_by_state(*operation, state='CANCELED')
    assert result == [canceled_operation]
