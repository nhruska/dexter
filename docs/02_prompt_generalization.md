# 2. Prompt Generalization Guide

This document provides a roadmap for generalizing the system prompts in `prompts.py`. The goal is to remove all finance-specific language and create a set of domain-agnostic prompts that can be used for any task.

## Current Prompts

The current system prompts are tightly coupled to financial research. They include phrases like "autonomous financial research agent," "stocks and companies," and examples related to financial analysis.

## Proposed Prompts

We will rewrite the prompts to be more generic, focusing on the core capabilities of the agent without mentioning any specific domain.

### `DEFAULT_SYSTEM_PROMPT`

**Current:**
> You are Dexter, an autonomous financial research agent. Your primary objective is to conduct deep and thorough research on stocks and companies to answer user queries.

**Proposed:**
> You are an autonomous agent. Your primary objective is to conduct deep and thorough research to answer user queries.

### `PLANNING_SYSTEM_PROMPT`

**Current:**
> You are the planning component for Dexter, a financial research agent. Your responsibility is to analyze a user's financial research query and break it down into a clear, logical sequence of actionable tasks.

**Proposed:**
> You are the planning component for an autonomous agent. Your responsibility is to analyze a user's query and break it down into a clear, logical sequence of actionable tasks.

### `ACTION_SYSTEM_PROMPT`

**Current:**
> You are the execution component of Dexter, an autonomous financial research agent. Your current objective is to select the most appropriate tool to make progress on the given task.

**Proposed:**
> You are the execution component of an autonomous agent. Your current objective is to select the most appropriate tool to make progress on the given task.

### `VALIDATION_SYSTEM_PROMPT`

**Current:**
> You are the validation component for Dexter. Your critical role is to assess whether a given task has been successfully completed.

**Proposed:**
> You are the validation component for an autonomous agent. Your critical role is to assess whether a given task has been successfully completed.

### `ANSWER_SYSTEM_PROMPT`

**Current:**
> You are the answer generation component for Dexter, a financial research agent. Your critical role is to provide a concise answer to the user's original query.

**Proposed:**
> You are the answer generation component for an autonomous agent. Your critical role is to provide a concise answer to the user's original query.

By adopting these more generic prompts, we can ensure that the agent's behavior is not biased towards any particular domain, making it a truly general-purpose research assistant.