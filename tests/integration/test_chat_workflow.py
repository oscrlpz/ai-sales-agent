import pytest

from workflows.chat_workflow import run_chat


@pytest.mark.integration
def test_run_chat(user_inputs_1, user_inputs_2, set_env_var):
    """
    Test the run_chat function with a list of user inputs.
    """
    # Call the function with the user inputs
    set_env_var
    run_chat(user_inputs_1)
    run_chat(user_inputs_2)
    assert True
