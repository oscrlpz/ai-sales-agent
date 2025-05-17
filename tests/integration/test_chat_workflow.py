import pytest

from api.services.sales_agent import run_chat


@pytest.mark.integration
def test_run_chat(user_inputs_1, user_inputs_2, session_id):
    """
    Test the run_chat function with a list of user inputs.
    """
    # Call the function with the user inputs
    for user_inputs in user_inputs_1:
        run_chat(user_inputs, session_id)
    for user_inputs in user_inputs_2:
        run_chat(user_inputs, session_id)
    assert True
