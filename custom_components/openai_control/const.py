"""Constants for the OpenAI Control integration."""

DOMAIN = "openai_control"

ENTITY_TEMPLATE = """$id<>$name<>$status<>$action
"""
TEST_ENTITY_TEMPLATE = """$id<>$name<>$status<>$action<>$brightness<>$color_temp_kelvin<>$hs_color
"""

PROMPT_TEMPLATE = """Below is a list of devices, containing the device id, name, state, and actions to perform.
The sections of the string are delimited by the string "<>"

Entities:
$entities

Prompt: "$prompt"

JSON Template: { "entities": [ { "id": "", "action": "" } ], "assistant": "" }

Determine if the above prompt is a command related to the above entities. Respond only in JSON.

If the prompt is a command then determine which entities relate to the above prompt and which action should be taken on those entities.
Respond only in the format of the above JSON Template.
Fill in the "assistant" field as a natural language responds for the action being taken.
Respond only with the JSON Template.
"""
DUTCH_PROMPT_TEMPLATE = """Hieronder staat een lijst van devices, met daarin de device id, name, state en acties die uitgevoerd moeten worden.
De secties van de string worden gescheiden door de string "<>"

Entities:
$entities

Prompt: "$prompt"

JSON Template: { "entities": [ { "id": "", "action": "" } ], "assistant": "" }

Bepaal of de bovenstaande prompt een opdracht is die gerelateerd is aan de bovengenoemde entities. Antwoord alleen in JSON.

Als de prompt een opdracht is, bepaal dan welke entities betrekking hebben op de bovenstaande prompt en welke actie ondernomen moet worden voor die entities.
Antwoord enkel in het formaat van het bovenstaande JSON Template.
Vul het "assistant" veld in met een antwoord in natuurlijke taal voor de actie die wordt ondernomen.
Antwoord alleen met het JSON Template.
"""

TEST_TEMPLATE = """Below is a list of devices, containing the device id, name, state, actions to perform, brightness, color temperature (in Kelvin), and HS color. The sections of the string are delimited by the string "<>"

Entities:
$entities

Prompt: "$prompt"

JSON Template: { "entities": [ { "id": "", "action": "", "brightness": "", "color_temp_kelvin": "", "hs_color": "" } ], "assistant": "" }

Determine if the above prompt is a command related to the above entities. Respond only in JSON.

If the prompt is a command then determine which entities relate to the above prompt and which action should be taken on those entities. Additionally, determine the desired brightness, color temperature or HS color if mentioned.

Respond only in the format of the above JSON Template.
Fill in the "assistant" field as a natural language response for the action being taken.
Respond only with the JSON Template.
"""

"""Options"""

CONF_PROMPT = "prompt"
DEFAULT_PROMPT = """This smart home is controlled by Home Assistant."""

CONF_CHAT_MODEL = "chat_model"
DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"

PROMPT_LANGUAGE = "test"
DEFAULT_PROMPT_LANGUAGE = "English"

CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 250

CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 1

CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.5