"""Constants for the OpenAI Control integration."""

DOMAIN = "openai_control"

ENTITY_TEMPLATE = """$id<>$status<>$action
"""
COLOR_ENTITY_TEMPLATE = """$id<>$status<>$action<>$brightness<>$hs_color
"""
TEST_ENTITY_TEMPLATE = """$id<>$status<>$action<>$brightness<>$hs_color
"""

PROMPT_TEMPLATE = """
Based on the given prompt, you need to identify the relevant entities in the list below and perform the appropriate actions.

Prompt: "$prompt"

Entities: $entities

Each entity has an entity id, state, possible actions to perform, separated by "<>".
Use this information to complete the following tasks:

Identify each entity in the prompt. The room of the entity can always be found in the name of the entity immediately after "light.", for example in "kitchenlamp_roof", "kitchen" is the room.
Select only the entities that match the description in the prompt.
Determine the desired action for each entity, taking into account its current state.
Your answer should conform to the following JSON Template format:
JSON Template: { "entities": [ { "id": "", "action": "" } ], "assistant": "" }

In the "assistant" field, provide a natural language explanation of the actions taken.
"""
DUTCH_PROMPT_TEMPLATE = """
Op basis van de gegeven prompt, moet je de relevante entiteiten identificeren in de onderstaande lijst en de juiste acties uitvoeren.

Prompt: "$prompt"

Entities: $entities

Elke entiteit heeft een entity id, state, possible actions to perform, gescheiden door "<>".
Gebruik deze informatie om de volgende taken uit te voeren:

- Identificeer elke entiteit in de prompt. De ruimte van de entiteit is altijd te vinden in de naam van de entiteit direct na "light.", bijvoorbeeld in "keukenlamp_zijkant", is "keuken" de ruimte.
- Kies alleen de entiteiten die overeenkomen met de omschrijving in de prompt.
- Bepaal de gewenste actie voor elke entiteit, rekening houdend met de huidige status.

Je antwoord moet voldoen aan het volgende JSON Template formaat:
JSON Template: { "entities": [ { "id": "", "action": "" } ], "assistant": "" }

In het "assistant" veld geef je in natuurlijke taal uitleg over de uitgevoerde acties.
"""
COLOR_PROMPT_TEMPLATE = """
Based on the given prompt, you need to identify the relevant entities in the list below and perform the appropriate actions.

Prompt: "$prompt"

Entities: $entities

Each entity has an entity id, state, possible actions to perform, brightness (0-255), and HS color (Hue(0-360), Saturation(0-100)), separated by "<>".
Use this information to complete the following tasks:

Identify each entity in the prompt. The room of the entity can always be found in the name of the entity immediately after "light.", for example in "kitchenlamp_roof", "kitchen" is the room.
Select only the entities that match the description in the prompt.
Determine the desired action for each entity, taking into account its current state.
Add brightness (0-255) if specified, otherwise leave blank. Note: "bright" is interpreted as a brightness value of 255 and "soft" can be interpreted as a lower value, for example 50.
Add HS color as "Hue(0-360),Saturation(0-100)" if specified, otherwise leave blank.
Your answer should conform to the following JSON Template format:
{ "entities": [ { "id": "", "action": "", "brightness": "", "hs_color": "" } ], "assistant": "" }

In the "assistant" field, provide a natural language explanation of the actions taken.
"""
DUTCH_COLOR_PROMPT_TEMPLATE = """
Op basis van de gegeven prompt, moet je de relevante entiteiten identificeren in de onderstaande lijst en de juiste acties uitvoeren.

Prompt: "$prompt"

Entities: $entities

Elke entiteit heeft een entity id, state, possible actions to perform, brightness (0-255), en HS color (Hue(0-360),Saturation(0-100)), gescheiden door "<>".
Gebruik deze informatie om de volgende taken uit te voeren:

- Identificeer elke entiteit in de prompt. De ruimte van de entiteit is altijd te vinden in de naam van de entiteit direct na "light.", bijvoorbeeld in "keukenlamp_plafond", is "keuken" de ruimte.
- Kies alleen de entiteiten die overeenkomen met de omschrijving in de prompt.
- Bepaal de gewenste actie voor elke entiteit, rekening houdend met de huidige status.
- Voeg brightness (0-255) toe indien gespecificeerd, laat anders leeg. Let op: "fel" wordt geïnterpreteerd als brightness waarde van 255 en "zacht" kan worden geïnterpreteerd als een lagere waarde van bijvoorbeeld 50.
- Voeg HS color als "Hue(0-360),Saturation(0-100)" toe indien gespecificeerd, laat anders leeg.

Je antwoord moet voldoen aan het volgende JSON Template formaat:
{ "entities": [ { "id": "", "action": "", "brightness": "", "hs_color": "" } ], "assistant": "" }

In het "assistant" veld geef je in natuurlijke taal uitleg over de uitgevoerde acties.
"""
TEST_PROMPT_TEMPLATE = """
Below is a list of devices with device id, name, state, possible actions, brightness, and HS color, delimited by "<>"

Entities:
$entities

Prompt: "$prompt"

JSON Template: { "entities": [ { "id": "", "action": "", "brightness": "", "hs_color": "" } ], "assistant": "" }

Using the above prompt, respond in JSON format.

Identify:
1. Relevant entities from the prompt.
2. Desired action for each entity.
3. Brightness (0-100) if mentioned and supported; leave blank if not.
4. HS color as "Hue,Saturation" if mentioned and supported; leave blank if not.

Use the above JSON Template format for the response, including a natural language explanation in the "assistant" field.
"""

"""Options"""

CONF_PROMPT = "prompt"
DEFAULT_PROMPT = """This smart home is controlled by Home Assistant."""

CONF_CHAT_MODEL = "chat_model"
DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"

CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 250

CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 1

CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.5

LANGUAGE_AND_MODE_OPTIONS = [
    "Dutch + brightness + color control",
    "English + brightness + color control",
    "English",
    "Dutch",
    "Test",
]

LANGUAGE_AND_MODE = "language_and_mode"
DEFAULT_LANGUAGE_AND_MODE = "English"