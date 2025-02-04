"""The OpenAI Control integration."""
from __future__ import annotations

import json
import re

from functools import partial
import logging
from typing import Any, Literal

from string import Template

import openai
from openai import error

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, TemplateError
from homeassistant.helpers import intent, template, entity_registry
from homeassistant.util import ulid

from .const import (
    CONF_CHAT_MODEL,
    CONF_MAX_TOKENS,
    CONF_PROMPT,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    DEFAULT_CHAT_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_PROMPT,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    ENTITY_TEMPLATE,
    COLOR_ENTITY_TEMPLATE,
    PROMPT_TEMPLATE,
    COLOR_PROMPT_TEMPLATE,
    DUTCH_PROMPT_TEMPLATE,
    DUTCH_COLOR_PROMPT_TEMPLATE,
    LANGUAGE_AND_MODE,
    TEST_PROMPT_TEMPLATE,
    TEST_ENTITY_TEMPLATE,
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.info("Testing the logs")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up OpenAI Agent from a config entry."""

    openai.api_key = entry.data[CONF_API_KEY]

    try:
        await hass.async_add_executor_job(
            partial(openai.Model.list, request_timeout=10)
        )
    except error.AuthenticationError as err:
        _LOGGER.error("Invalid API key: %s", err)
        return False
    except error.OpenAIError as err:
        raise ConfigEntryNotReady(err) from err

    conversation.async_set_agent(hass, entry, OpenAIAgent(hass, entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload OpenAI Agent."""
    openai.api_key = None
    conversation.async_unset_agent(hass, entry)
    return True


def _entry_ext_dict(entry: er.RegistryEntry) -> dict[str, Any]:
    """Convert entry to API format."""
    data = entry.as_partial_dict
    data["aliases"] = entry.aliases
    data["capabilities"] = entry.capabilities
    data["device_class"] = entry.device_class
    data["original_device_class"] = entry.original_device_class
    data["original_icon"] = entry.original_icon
    return data

class OpenAIAgent(conversation.AbstractConversationAgent):
    """OpenAI Control Agent."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.history: dict[str, list[dict]] = {}

    @property
    def attribution(self):
        """Return the attribution."""
        return {"name": "Powered by OpenAi", "url": "https://openai.com"}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        
        _LOGGER.info("LANGUAGE_AND_MODE =  %s ", self.entry.options.get(LANGUAGE_AND_MODE))

        """ Options input """

        raw_prompt = self.entry.options.get(CONF_PROMPT, DEFAULT_PROMPT)
        model = self.entry.options.get(CONF_CHAT_MODEL, DEFAULT_CHAT_MODEL)
        max_tokens = self.entry.options.get(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS)
        top_p = self.entry.options.get(CONF_TOP_P, DEFAULT_TOP_P)
        temperature = self.entry.options.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)

        """ Start a sentence """

        # check if the conversation is continuing or new

        # generate the prompt to be added to the sending messages later
        try:
            prompt = self._async_generate_prompt(raw_prompt)
        except TemplateError as err:

            _LOGGER.error("Error rendering prompt: %s", err)

            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Sorry, I had a problem with my template: {err}",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        # if continuing then get the messages from the conversation history
        if user_input.conversation_id in self.history:
            conversation_id = user_input.conversation_id
            messages = self.history[conversation_id]
        # if new then create a new conversation history
        else:
            conversation_id = ulid.ulid()
            # add the conversation starter to the begining of the conversation
            # this is to give the assistant more personality
            messages = [{"role": "system", "content": prompt}]

        # Standaardwaarden
        prompt_template = Template(PROMPT_TEMPLATE)
        entity_template = Template(ENTITY_TEMPLATE)

        # Check voor "color" modus in combinatie met taal
        if "color" in self.entry.options.get(LANGUAGE_AND_MODE):
            entity_template = Template(COLOR_ENTITY_TEMPLATE)
            
            if "English" in self.entry.options.get(LANGUAGE_AND_MODE):
                prompt_template = Template(COLOR_PROMPT_TEMPLATE)
                _LOGGER.info("Mode: English color mode")
            elif "Dutch" in self.entry.options.get(LANGUAGE_AND_MODE):
                prompt_template = Template(DUTCH_COLOR_PROMPT_TEMPLATE)
                _LOGGER.info("Mode: Dutch color mode")
            else:
                _LOGGER.warning("Color mode active but unknown language.")
            
        elif "English" in self.entry.options.get(LANGUAGE_AND_MODE):
            _LOGGER.info("Mode: English mode")

        elif "Dutch" in self.entry.options.get(LANGUAGE_AND_MODE):
            prompt_template = Template(DUTCH_PROMPT_TEMPLATE)
            _LOGGER.info("Mode: Dutch mode")

        elif self.entry.options.get(LANGUAGE_AND_MODE) == "Test":
            prompt_template = Template(TEST_PROMPT_TEMPLATE)
            entity_template = Template(TEST_ENTITY_TEMPLATE)
            _LOGGER.info("Mode: Test mode")

        else:
            _LOGGER.warning("Default mode active, unknown language or mode value.")

        """ Entities """

        # Get all entities exposed to the Conversation Assistant
        # NOTE: for the first release only lights and switches are supported

        registry = entity_registry.async_get(self.hass)
        entity_ids = self.hass.states.async_entity_ids(['light', 'switch'])

        entities_template = ''

        for entity_id in entity_ids:
            # get entities from the registry
            # to determine if they are exposed to the Conversation Assistant
            # registry entries have the propert "options['conversation']['should_expose']"
            entity = registry.entities.get(entity_id)

            if entity.options['conversation']['should_expose'] is not True:
                continue

            if "color" in self.entry.options.get(LANGUAGE_AND_MODE):
                # get the status string
                status_object = self.hass.states.get(entity_id)
                status_string = status_object.state

                _LOGGER.info("status_object  %s ", status_object)
                _LOGGER.info("status_string  %s ", status_string)

                # Extract brightness and color if they exist.
                brightness = status_object.attributes.get('brightness', None)
                hs_color = status_object.attributes.get('hs_color', None)

                _LOGGER.debug("Entity ID: %s, Brightness: %s, HS_Color: %s", entity_id, brightness, hs_color)

                # Basislijst met services
                services = ['toggle', 'turn_off', 'turn_on']  # 'turn_on' is al aanwezig voor zowel helderheid als kleur.

                # Update the entity_template population code.
                entities_template += entity_template.substitute(
                    id=entity_id,
                    # name=entity.name or entity_id,
                    status=status_string or "unknown",
                    action=','.join(services),
                    brightness=brightness if brightness is not None else "",
                    hs_color=",".join(map(str, hs_color)) if hs_color is not None else ""
                )
            else:
                # get the status string
                status_object = self.hass.states.get(entity_id)
                status_string = status_object.state

                # TODO: change this to dynamic call once more than lights are supported
                services = ['toggle', 'turn_off', 'turn_on']

                # append the entitites tempalte
                entities_template += entity_template.substitute(
                    id=entity_id,
                    # name=entity.name or entity_id,
                    status=status_string or "unknown",
                    action=','.join(services),
                )

        # generate the prompt using the prompt_template
        prompt_render = prompt_template.substitute(
            entities=entities_template,
            prompt=user_input.text
        )

        messages.append({"role": "user", "content": prompt_render})

        _LOGGER.debug("Prompt for %s: %s", model, messages)

        """ OpenAI Call """

        # NOTE: this version does not support a full conversation history
        # this is because the prompt_template and entities list
        # can quickly increase the size of a conversation
        # causing an error where the payload is too large

        # to that end we create a new list of messages to be sent
        # sending only the system role message and the current user message
        sending_messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": prompt_render}
        ]

        # call OpenAI
        try:
            result = await openai.ChatCompletion.acreate(
                model=model,
                messages=sending_messages,
                max_tokens=max_tokens,
                top_p=top_p,
                temperature=temperature,
                user=conversation_id
            )
        except error.OpenAIError as err:
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Sorry, I had a problem talking to OpenAI: {err}",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        content = result["choices"][0]["message"]["content"]

        # set a default reply
        # this will be changed if a better reply is found
        reply = content

        _LOGGER.debug("Response for %s: %s", model, content)

        json_response = None

        # all responses should come back as a JSON, since we requested such in the prompt_template
        try:
            json_response = json.loads(content)
        except json.JSONDecodeError as err:
            _LOGGER.error('Error on first parsing of JSON message from OpenAI %s', err)

        # if the response did not come back as a JSON
        # attempt to extract JSON from the response
        # this is because GPT will sometimes prefix the JSON with a sentence

        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1

        if start_idx is not -1 and end_idx is not -1:
            json_string = content[start_idx:end_idx]
            try:
                json_response = json.loads(json_string)
            except json.JSONDecodeError as err:
                _LOGGER.error('Error on second parsing of JSON message from OpenAI %s', err)
        else:
            _LOGGER.error('Error on second extraction of JSON message from OpenAI, %s', content)

        # only operate on JSON actions if JSON was extracted
        if json_response is not None:

            # call the needed services on the specific entities
            call_action = None

            try:
                for entity in json_response["entities"]:
                    entity_id = entity['id']
                    entity_action = entity['action']
                    service_data = {'entity_id': entity_id}
                    
                    if "color" in self.entry.options.get(LANGUAGE_AND_MODE):
                        status_object = self.hass.states.get(entity_id)  # Definieer status_object

                        if 'brightness' in entity and entity['brightness']:
                            try:
                                service_data['brightness'] = int(entity['brightness'])
                            except ValueError:
                                _LOGGER.error("Invalid brightness value for entity: %s. Expected integer or convertible string, got: %s.", entity_id, entity['brightness'])
                        if 'hs_color' in entity and entity['hs_color']:
                            try:
                                hs_values = [float(value) for value in entity['hs_color'].split(',')]
                                if len(hs_values) == 2:
                                    service_data['hs_color'] = hs_values
                                else:
                                    _LOGGER.error("Invalid hs_color value for entity: %s. Expected two convertible strings or numbers separated by a comma, got: %s.", entity_id, entity['hs_color'])
                            except ValueError:
                                _LOGGER.error("Invalid hs_color value for entity: %s. Expected two convertible strings or numbers, got: %s.", entity_id, entity['hs_color'])

                    if entity_id.startswith("switch."):
                        call_action = "switch"
                    elif entity_id.startswith("light."):
                        call_action = "light"
                    
                    await self.hass.services.async_call(call_action, entity_action, service_data)
                    _LOGGER.info("Executed %s action with data %s on entity: %s", entity_action, service_data, entity_id)

            except KeyError as err:
                _LOGGER.warn('Error processing entity: %s. Missing key: %s', entity_id, err)

            # resond with the "assistant" field of the json_response

            try:
                reply = json_response['assistant']
            except KeyError as err:
                _LOGGER.error('Error extracting assistant response %s', user_input.text)
                intent_response = intent.IntentResponse(language=user_input.language)
                intent_response.async_set_error(
                    intent.IntentResponseErrorCode.UNKNOWN,
                    f"Sorry, there was an error understanding OpenAI: {err}",
                )
                return conversation.ConversationResult(
                    response=intent_response, conversation_id=conversation_id
                )

        messages.append(reply)
        self.history[conversation_id] = messages

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(reply)
        return conversation.ConversationResult(
            response=intent_response, conversation_id=conversation_id
        )

    def _async_generate_prompt(self, raw_prompt: str) -> str:
        """Generate a prompt for the user."""
        return template.Template(raw_prompt, self.hass).async_render(
            {
                "ha_name": self.hass.config.location_name,
            },
            parse_result=False,
        )