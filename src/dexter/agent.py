from typing import List

from langchain_core.messages import AIMessage

from dexter.model import call_llm
from dexter.prompts import (
    ACTION_SYSTEM_PROMPT,
    ANSWER_SYSTEM_PROMPT,
    PLANNING_SYSTEM_PROMPT,
    TOOL_ARGS_SYSTEM_PROMPT,
    VALIDATION_SYSTEM_PROMPT,
)
from dexter.schemas import Answer, IsDone, OptimizedToolArgs, Task, TaskList
from dexter.utils.logger import Logger
from dexter.config import settings


class Agent:
    def __init__(self, tools: List):
        self.logger = Logger()
        self.tools = tools
        self.max_steps = settings.AGENT_MAX_STEPS
        self.max_steps_per_task = settings.AGENT_MAX_STEPS_PER_TASK

    # ---------- task planning ----------
    def plan_tasks(self, query: str) -> List[Task]:
        tool_descriptions = "\n".join([f"- {t.name}: {t.description}" for t in self.tools])
        prompt = f"""
        Given the user query: "{query}",
        Create a list of tasks to be completed.
        Example: {{"tasks": [{{"id": 1, "description": "some task", "done": false}}]}}
        """
        system_prompt = PLANNING_SYSTEM_PROMPT.format(tools=tool_descriptions)
        self.logger.info("agent.plan.start")
        try:
            response = call_llm(prompt, system_prompt=system_prompt, output_schema=TaskList)
            tasks = response.tasks
            self.logger.info("agent.plan.end", tasks=tasks)
        except Exception as e:
            self.logger.error("agent.plan.error", error=str(e))
            tasks = [Task(id=1, description=query, done=False)]
        
        return tasks

    # ---------- ask LLM what to do ----------
    def ask_for_actions(self, task_desc: str, last_outputs: str = "") -> AIMessage:
        # last_outputs = textual feedback of what we just tried
        prompt = f"""
        We are working on: "{task_desc}".
        Here is a history of tool outputs from the session so far: {last_outputs}

        Based on the task and the outputs, what should be the next step?
        """
        self.logger.info("agent.think.start")
        try:
            response = call_llm(prompt, system_prompt=ACTION_SYSTEM_PROMPT, tools=self.tools)
            self.logger.info("agent.think.end", tool_calls=response.tool_calls)
            return response
        except Exception as e:
            self.logger.error("agent.think.error", error=str(e))
            return AIMessage(content="Failed to get actions.")

    # ---------- ask LLM if task is done ----------
    def ask_if_done(self, task_desc: str, recent_results: str) -> bool:
        prompt = f"""
        We were trying to complete the task: "{task_desc}".
        Here is a history of tool outputs from the session so far: {recent_results}

        Is the task done?
        """
        self.logger.info("agent.validate.start")
        try:
            resp = call_llm(prompt, system_prompt=VALIDATION_SYSTEM_PROMPT, output_schema=IsDone)
            self.logger.info("agent.validate.end", done=resp.done)
            return resp.done
        except Exception as e:
            self.logger.error("agent.validate.error", error=str(e))
            return False

    # ---------- optimize tool arguments ----------
    def optimize_tool_args(self, tool_name: str, initial_args: dict, task_desc: str) -> dict:
        """Optimize tool arguments based on task requirements."""
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return initial_args
        
        # Get tool schema info
        tool_description = tool.description
        tool_schema = tool.args_schema.schema() if hasattr(tool, 'args_schema') and tool.args_schema else {}
        
        prompt = f"""
        Task: "{task_desc}"
        Tool: {tool_name}
        Tool Description: {tool_description}
        Tool Parameters: {tool_schema}
        Initial Arguments: {initial_args}
        
        Review the task and optimize the arguments to ensure all relevant parameters are used correctly.
        Pay special attention to filtering parameters that would help narrow down results to match the task.
        """
        self.logger.info("agent.optimize_args.start")
        try:
            response = call_llm(prompt, system_prompt=TOOL_ARGS_SYSTEM_PROMPT, output_schema=OptimizedToolArgs)
            # Handle case where LLM returns dict directly instead of OptimizedToolArgs
            if isinstance(response, dict):
                optimized_args = response if response else initial_args
            else:
                optimized_args = response.arguments
            self.logger.info("agent.optimize_args.end", optimized_args=optimized_args)
            return optimized_args
        except Exception as e:
            self.logger.error("agent.optimize_args.error", error=str(e))
            return initial_args

    # ---------- tool execution ----------
    def _execute_tool(self, tool, tool_name: str, inp_args):
        """Execute a tool with progress indication."""
        return tool.run(inp_args)
    
    # ---------- confirm action ----------
    def confirm_action(self, tool: str, input_str: str) -> bool:
        # In production you'd ask the user; here we just log and auto-confirm
        # Risky tools are not implemented in this version.
        return True

    # ---------- main loop ----------
    def run(self, query: str):
        """
        Executes the main agent loop to process a user query.

        This method orchestrates the entire process of understanding a query,
        planning tasks, executing tools to gather information, and synthesizing
        a final answer.

        Args:
            query (str): The user's natural language query.

        Returns:
            str: A comprehensive answer to the user's query.
        """
        self.logger.info("agent.run.start", query=query)
        
        # Initialize agent state for this run.
        step_count = 0
        last_actions = []
        session_outputs = []

        # 1. Decompose the user query into a list of tasks.
        tasks = self.plan_tasks(query)

        # If no tasks were created, the query is likely out of scope.
        if not tasks:
            answer = self._generate_answer(query, session_outputs)
            self.logger.info("agent.run.end", answer=answer)
            return answer

        # 2. Execute tasks until all are complete or max steps are reached.
        while any(not t.done for t in tasks):
            # Global safety break.
            if step_count >= self.max_steps:
                self.logger.warn("agent.run.max_steps_reached")
                break

            # Select the next incomplete task.
            task = next(t for t in tasks if not t.done)
            self.logger.info("task.start", task_id=task.id, description=task.description)

            # Loop for a single task, with its own step limit.
            per_task_steps = 0
            task_outputs = []
            while per_task_steps < self.max_steps_per_task:
                if step_count >= self.max_steps:
                    self.logger.warn("agent.run.max_steps_reached")
                    return

                # Ask the LLM for the next action to take for the current task.
                ai_message = self.ask_for_actions(task.description, last_outputs="\n".join(task_outputs))
                
                # If no tool is called, the task is considered complete.
                if not ai_message.tool_calls:
                    task.done = True
                    self.logger.info("task.done", task_id=task.id, description=task.description)
                    break

                # Process each tool call returned by the LLM.
                for tool_call in ai_message.tool_calls:
                    if step_count >= self.max_steps:
                        break

                    tool_name = tool_call["name"]
                    initial_args = tool_call["args"]
                    
                    # Refine tool arguments for better performance.
                    optimized_args = self.optimize_tool_args(tool_name, initial_args, task.description)
                    
                    # Create a signature of the action to be taken.
                    action_sig = f"{tool_name}:{optimized_args}"

                    # Detect and prevent repetitive action loops.
                    last_actions.append(action_sig)
                    if len(last_actions) > 4:
                        last_actions = last_actions[-4:]
                    if len(set(last_actions)) == 1 and len(last_actions) == 4:
                        self.logger.warn("agent.run.repeating_action_loop_detected")
                        return
                    
                    # Execute the tool.
                    tool_to_run = next((t for t in self.tools if t.name == tool_name), None)
                    if tool_to_run and self.confirm_action(tool_name, str(optimized_args)):
                        self.logger.info("tool.run.start", tool_name=tool_name, args=optimized_args)
                        try:
                            result = self._execute_tool(tool_to_run, tool_name, optimized_args)
                            self.logger.info("tool.run.end", tool_name=tool_name, result=result)
                            output = f"Output of {tool_name} with args {optimized_args}: {result}"
                            session_outputs.append(output)
                            task_outputs.append(output)
                        except Exception as e:
                            self.logger.error("tool.run.error", tool_name=tool_name, error=str(e))
                            error_output = f"Error from {tool_name} with args {optimized_args}: {e}"
                            session_outputs.append(error_output)
                            task_outputs.append(error_output)
                    else:
                        self.logger.warn("agent.run.invalid_tool", tool_name=tool_name)

                    step_count += 1
                    per_task_steps += 1

                # After a batch of tool calls, check if the task is complete.
                if self.ask_if_done(task.description, "\n".join(task_outputs)):
                    task.done = True
                    self.logger.info("task.done", task_id=task.id, description=task.description)
                    break

        # 3. Synthesize the final answer from all collected tool outputs.
        answer = self._generate_answer(query, session_outputs)
        self.logger.info("agent.run.end", answer=answer)
        return answer
    
    # ---------- answer generation ----------
    def _generate_answer(self, query: str, session_outputs: list) -> str:
        """Generate the final answer based on collected data."""
        self.logger.info("agent.answer.start")
        all_results = "\n\n".join(session_outputs) if session_outputs else "No data was collected."
        answer_prompt = f"""
        Original user query: "{query}"
        
        Data and results collected from tools:
        {all_results}
        
        Based on the data above, provide a comprehensive answer to the user's query.
        Include specific numbers, calculations, and insights.
        """
        try:
            answer_obj = call_llm(answer_prompt, system_prompt=ANSWER_SYSTEM_PROMPT, output_schema=Answer)
            self.logger.info("agent.answer.end", answer=answer_obj.answer)
            return answer_obj.answer
        except Exception as e:
            self.logger.error("agent.answer.error", error=str(e))
            return "I'm sorry, I was unable to generate an answer."
