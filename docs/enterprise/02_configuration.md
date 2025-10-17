# 2. Enterprise Configuration Management

A robust and flexible configuration system is essential for an enterprise-grade application. It allows administrators to easily customize the agent's behavior without modifying the code, and it provides a clear separation of configuration from the application logic.

## Key Features

### 1. Centralized Configuration Model

We will create a centralized Pydantic `Settings` model to define all configurable parameters. This will provide a single source of truth for all configuration settings and enable type validation and clear default values.

**Key Parameters to Configure:**
-   `LOG_LEVEL`: The logging level (e.g., `info`, `debug`, `warn`, `error`).
-   `LLM_MODEL`: The language model to use (e.g., `gpt-4.1`, `gpt-3.5-turbo`).
-   `LLM_TEMPERATURE`: The temperature for the language model.
-   `AGENT_MAX_STEPS`: The global maximum number of steps for the agent.
-   `AGENT_MAX_STEPS_PER_TASK`: The maximum number of steps per task.
-   `MONITORING_PLATFORM`: The target platform for logs (e.g., `datadog`, `newrelic`, `none`).
-   `PROMETHEUS_PORT`: The port for the Prometheus metrics endpoint.

### 2. Configuration Sources

The agent will support multiple configuration sources, with a clear order of precedence:

1.  **Environment Variables:** The highest priority, allowing for easy overrides in containerized environments.
2.  **`.env` File:** For local development, loaded automatically.
3.  **Default Values:** Defined in the Pydantic `Settings` model.

### 3. Dynamic Tool Loading

We will implement a dynamic tool loading mechanism that allows users to specify which toolsets to load via configuration. This will make it easy to extend the agent with custom tools without modifying the core application.

**Example Configuration:**
```
# .env
TOOL_MODULES=my_company.tools.billing,my_company.tools.support
```

The agent will automatically discover and load all `BaseTool` instances from the specified modules.

## Implementation Plan

1.  **Create `Settings` Model:** Create a `src/dexter/config.py` file with a Pydantic `Settings` model that defines all configurable parameters.
2.  **Integrate `Settings` Model:** Refactor the codebase to use the `Settings` model for all configuration values, instead of hardcoded values or direct `os.getenv()` calls.
3.  **Implement Dynamic Tool Loader:** Create a `ToolLoader` class that can discover and load tools from specified Python modules.
4.  **Update `cli.py`:** Modify the CLI to use the `ToolLoader` to load tools based on the `TOOL_MODULES` configuration.
5.  **Update `README.md`:** Add a new "Configuration" section to the `README.md` that documents all the available configuration options.