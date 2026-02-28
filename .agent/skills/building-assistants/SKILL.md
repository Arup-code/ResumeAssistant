---
name: building-assistants
description: Builds an AI assistant for a given prompt using the LLM provider mentioned in the prompt. Configures provider SDKs with custom instructions.
---

# Assistant Builder Skill

## When to use this skill
- The user asks to "build an assistant" or "create an agent" based on a prompt.
- The user specifies an LLM provider (e.g., OpenAI, Anthropic, Google/Gemini) alongside the prompt.
- You need to generate boilerplate code to instantiate an LLM client and pass a specific system prompt or instructions list.

## Workflow
- [ ] **Parse Input**: Analyze the user's request to extract the core Assistant logic (Role, Goals, Instructions) and the requested Provider.
- [ ] **Validate Provider**: Ensure the requested provider is supported (e.g., check against `resources/supported_providers.json` if available).
- [ ] **Generate Code**: Use the appropriate code block template to instantiate the provider's SDK, injecting the parsed prompt as the system context.
- [ ] **Handle Credentials**: Ensure the generated code uses environment variables for API keys (never hardcode keys).
- [ ] **Verify Dependencies**: Instruct the user on which pip/npm packages must be installed to run the generated code.

## Instructions
- When writing the assistant code, map the user's prompt strictly to the system instruction role or the equivalent top-level configuration for the requested provider.
- Keep the generated assistant class or function self-contained.
- **Provider Nuances**:
    - **OpenAI**: Use the `openai` SDK, construct the `messages` array with a `{"role": "system", "content": "..."}`.
    - **Anthropic**: Use the `anthropic` SDK, pass the prompt directly to the `system` parameter in the `messages.create` call.
    - **Google**: Use the `google-genai` SDK, instantiate the model passing `system_instruction`.

## Resources
- [Look at your existing `llm_file_assistant.py` for inspiration](src/model/llm_file_assistant.py)
