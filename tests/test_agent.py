import pytest
from dexter.agent import Agent
from dexter.tools import DEFAULT_TOOLS
from dexter.schemas import Task, TaskList, Answer
from langchain_core.messages import AIMessage

@pytest.fixture
def agent():
    """
    Provides a test instance of the Agent class.
    """
    return Agent(tools=DEFAULT_TOOLS)

def test_agent_plan_tasks(agent, mocker):
    """
    Tests that the agent can plan tasks correctly.
    """
    mock_call_llm = mocker.patch('dexter.agent.call_llm')
    mock_task_list = TaskList(tasks=[Task(id=1, description="Test task", done=False)])
    mock_call_llm.return_value = mock_task_list

    query = "Test query"
    tasks = agent.plan_tasks(query)

    assert len(tasks) == 1
    assert tasks[0].description == "Test task"
    mock_call_llm.assert_called_once()

def test_agent_run(agent, mocker):
    """
    Tests the full run method of the agent.
    """
    # Mock the external calls
    mock_plan_tasks = mocker.patch.object(agent, 'plan_tasks', return_value=[Task(id=1, description="Search for cats", done=False)])
    mock_ask_for_actions = mocker.patch.object(agent, 'ask_for_actions', return_value=AIMessage(content="", tool_calls=[{"name": "search_web", "args": {"query": "cats"}, "id": "1"}]))
    mock_optimize_tool_args = mocker.patch.object(agent, 'optimize_tool_args', return_value={"query": "cats"})
    mock_execute_tool = mocker.patch.object(agent, '_execute_tool', return_value="Search results for: cats")
    mock_ask_if_done = mocker.patch.object(agent, 'ask_if_done', return_value=True)
    mock_generate_answer = mocker.patch.object(agent, '_generate_answer', return_value="The answer is cats.")

    query = "What are cats?"
    result = agent.run(query)

    assert result == "The answer is cats."
    mock_plan_tasks.assert_called_once_with(query)
    mock_ask_for_actions.assert_called_once()
    mock_optimize_tool_args.assert_called_once()
    mock_execute_tool.assert_called_once()
    mock_ask_if_done.assert_called_once()
    mock_generate_answer.assert_called_once()

def test_agent_run_no_tasks(agent, mocker):
    """
    Tests that the agent handles the case where no tasks are planned.
    """
    mocker.patch.object(agent, 'plan_tasks', return_value=[])
    mock_generate_answer = mocker.patch.object(agent, '_generate_answer', return_value="I can't help with that.")

    query = "A query that results in no tasks"
    result = agent.run(query)

    assert result == "I can't help with that."
    mock_generate_answer.assert_called_once()