import logging
from .commit_formats import ConventionalCommit, format_conventional_commit, CommitType
from .config import config

import outlines
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic
import groq
import requests

logger = logging.getLogger(__name__)


def generate_commit_message(diff, model_name=None, use_emoji=False, include_description=True, description_length=100,
                            debug=False):
    if model_name is None:
        model_name = config.DEFAULT_MODEL

    logger.debug(f"Generating commit message using model: {model_name}")
    logger.debug(f"Diff: {diff[:100]}...")  # print first 100 characters of diff

    try:
        if model_name.startswith("openai/"):
            commit = generate_openai_commit(diff, model_name.split("/")[1], include_description, description_length,
                                            debug)
        elif model_name.startswith("gemini/"):
            commit = generate_gemini_commit(diff, model_name.split("/")[1], include_description, description_length,
                                            debug)
        elif model_name.startswith("claude/"):
            commit = generate_claude_commit(diff, model_name.split("/")[1], include_description, description_length,
                                            debug)
        elif model_name.startswith("groq/"):
            commit = generate_groq_commit(diff, model_name.split("/")[1], include_description, description_length,
                                          debug)
        elif model_name.startswith("ollama/"):
            commit = generate_ollama_commit(diff, model_name.split("/")[1], include_description, description_length,
                                            debug)
        else:
            commit = generate_outlines_commit(diff, model_name, include_description, description_length, debug)

        formatted_commit = format_conventional_commit(commit, use_emoji, include_description, description_length)
        logger.debug(f"Generated commit message: {formatted_commit}")
        return formatted_commit
    except Exception as e:
        logger.error(f"Error generating commit message with {model_name}: {str(e)}")
        error_description = f"An error occurred while generating the commit message: {str(e)}"
        default_commit = ConventionalCommit(type="chore", scope="error",
                                            description="Failed to generate commit message",
                                            long_description=error_description[:description_length])
        return format_conventional_commit(default_commit, use_emoji, include_description, description_length)


def get_commit_prompt(diff, include_description=True, description_length=100):
    prompt = f"""Generate a conventional commit message for the following git diff:

{diff}

The commit message should strictly follow the Conventional Commits specification:
<type>[optional scope]: <description>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

Respond with ONLY the commit message, nothing else. For example:
feat(ui): add new button component"""

    if include_description:
        prompt += f"""

Additionally, provide a more detailed description of the changes in a separate paragraph. 
The description should be no longer than {description_length} characters.

Example:
feat(auth): implement two-factor authentication

Add support for two-factor authentication using SMS and email. This includes new UI components for the setup process and backend logic for verification."""

    return prompt


def generate_openai_commit(diff, model_name, include_description, description_length, debug=False):
    logger.debug(f"Generating OpenAI commit with model: {model_name}")

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    prompt = get_commit_prompt(diff, include_description, description_length)
    logger.debug(f"Sending prompt to OpenAI: {prompt}")

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that generates concise and informative git commit messages."},
                {"role": "user", "content": prompt}
            ]
        )

        commit_message = response.choices[0].message.content.strip()
        logger.debug(f"Received response from OpenAI: {commit_message}")
        return parse_commit_message(commit_message, include_description, description_length, debug)
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {str(e)}")
        raise


def generate_gemini_commit(diff, model_name, include_description, description_length, debug=False):
    logger.debug(f"Generating Gemini commit with model: {model_name}")

    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)

    prompt = get_commit_prompt(diff, include_description, description_length)
    logger.debug(f"Sending prompt to Gemini: {prompt}")

    try:
        response = model.generate_content(prompt)
        commit_message = response.text.strip()
        logger.debug(f"Received response from Gemini: {commit_message}")
        return parse_commit_message(commit_message, include_description, description_length, debug)
    except Exception as e:
        logger.error(f"Error in Gemini API call: {str(e)}")
        raise


def generate_claude_commit(diff, model_name, include_description, description_length, debug=False):
    logger.debug(f"Generating Claude commit with model: {model_name}")

    client = Anthropic(api_key=config.CLAUDE_API_KEY)

    prompt = get_commit_prompt(diff, include_description, description_length)
    logger.debug(f"Sending prompt to Claude: {prompt}")

    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        commit_message = response.content[0].text.strip()
        logger.debug(f"Received response from Claude: {commit_message}")
        return parse_commit_message(commit_message, include_description, description_length, debug)
    except Exception as e:
        logger.error(f"Error in Claude API call: {str(e)}")
        raise


def generate_groq_commit(diff, model_name, include_description, description_length, debug=False):
    logger.debug(f"Generating Groq commit with model: {model_name}")

    client = groq.Groq(api_key=config.GROQ_API_KEY)

    prompt = get_commit_prompt(diff, include_description, description_length)
    logger.debug(f"Sending prompt to Groq: {prompt}")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model_name,
        )

        commit_message = chat_completion.choices[0].message.content.strip()
        logger.debug(f"Received response from Groq: {commit_message}")
        return parse_commit_message(commit_message, include_description, description_length, debug)
    except Exception as e:
        logger.error(f"Error in Groq API call: {str(e)}")
        raise


def generate_ollama_commit(diff, model_name, include_description, description_length, debug=False):
    logger.debug(f"Generating Ollama commit with model: {model_name}")

    url = f"{config.OLLAMA_BASE_URL}/api/generate"

    prompt = get_commit_prompt(diff, include_description, description_length)
    logger.debug(f"Sending prompt to Ollama: {prompt}")

    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        commit_message = response.json()["response"].strip()
        logger.debug(f"Received response from Ollama: {commit_message}")
        return parse_commit_message(commit_message, include_description, description_length, debug)
    except requests.RequestException as e:
        logger.error(f"Error in Ollama API call: {str(e)}")
        raise


def generate_outlines_commit(diff, model_name, include_description, description_length, debug=False):
    logger.debug(f"Generating Outlines commit with model: {model_name}")

    model = outlines.models.transformers(model_name)
    generator = outlines.generate.text(model)

    prompt = get_commit_prompt(diff, include_description, description_length)
    logger.debug(f"Sending prompt to Outlines: {prompt}")

    try:
        commit_message = generator(prompt)
        logger.debug(f"Received response from Outlines: {commit_message}")
        return parse_commit_message(commit_message, include_description, description_length, debug)
    except Exception as e:
        logger.error(f"Error in Outlines generation: {str(e)}")
        raise


def parse_commit_message(commit_message, include_description, description_length, debug=False):
    logger.debug(f"Parsing commit message: {commit_message}")

    lines = commit_message.split('\n')
    first_line = lines[0]

    # remove any prefixes like "Here is the conventional commit message:"
    if ":" in first_line and not any(first_line.lower().startswith(t.value) for t in CommitType):
        _, first_line = first_line.split(":", 1)
        first_line = first_line.strip()

    parts = first_line.split(":", 1)

    if len(parts) == 2:
        type_scope, short_description = parts
    else:
        type_scope, short_description = "chore", first_line

    type_scope_parts = type_scope.split("(", 1)
    commit_type = type_scope_parts[0].strip().lower()

    # ensure commit_type is valid, default to 'chore' if not
    if commit_type not in CommitType.__members__:
        logger.warning(f"Invalid commit type '{commit_type}', defaulting to 'chore'")
        commit_type = "chore"

    scope = ""
    if len(type_scope_parts) > 1:
        scope = type_scope_parts[1].rstrip(")").strip()

    short_description = short_description.strip()

    long_description = ""
    if include_description and len(lines) > 1:
        long_description = "\n".join(lines[1:]).strip()[:description_length]

    logger.debug(
        f"Parsed commit: type={commit_type}, scope={scope}, short_description={short_description}, long_description={long_description}")

    return ConventionalCommit(type=commit_type, scope=scope, description=short_description,
                              long_description=long_description)
