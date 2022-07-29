def _replace_register(flow_params, register_number, register_value):
    """Replace value from flows to given register number

    'register_value' key in dictionary will be replaced by register number
    given by 'register_number'

    :param flow_params: Dictionary containing defined flows
    :param register_number: The number of register where value will be stored
    :param register_value: Key to be replaced by register number

    """
    try:
        reg_port = flow_params[register_value]
        del flow_params[register_value]
        flow_params['reg{:d}'.format(register_number)] = reg_port
    except KeyError:
        pass
    return flow_params # expose the observer to the test_module


def test__replace_register():
    """
    Check the corretness of _replace_register
    """
    assert _replace_register({'reg1': 1, 'reg2': 2, 'reg3': 3}, 1, 'reg1') == {'reg1': 1, 'reg2': 2, 'reg3': 3}
    assert _replace_register({'reg1': 1, 'reg2': 2, 'reg3': 3}, 2, 'reg2') == {'reg1': 1, 'reg2': 2, 'reg3': 3}
    assert _replace_register({'reg1': 1, 'reg2': 2, 'reg3': 3}, 3, 'reg3') == {'reg1': 1, 'reg2': 2, 'reg3': 3}
    assert _replace_register({'reg1': 1, 'reg2': 2, 'reg3': 3}, 1, 'reg2') == {'reg1': 2, 'reg3': 3}
    assert _replace_register({'reg1': 1, 'reg2': 2, 'reg3': 3}, 2, 'reg3') == {'reg1': 1, 'reg2': 3}
    assert _replace_register({'reg1': 1, 'reg2': 2, 'reg3': 3}, 3, 'reg1') == {'reg2': 2, 'reg3': 1}