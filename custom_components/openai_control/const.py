"""Constants for the OpenAI Control integration."""

DOMAIN = "openai_control"

ENTITY_TEMPLATE = """$id<>$name<>$status<>$action
"""
COLOR_ENTITY_TEMPLATE = """$id<>$name<>$status<>$action<>$brightness<>$hs_color
"""
TEST_ENTITY_TEMPLATE = """$id<>$name<>$status<>$action<>$brightness<>$hs_color
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
COLOR_PROMPT_TEMPLATE = """Below is a list of devices, containing the device id, name, state, and actions to perform.
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

DUTCH_COLOR_PROMPT_TEMPLATE = """
Op basis van de gegeven prompt, moet je de relevante entiteiten identificeren en de juiste acties uitvoeren.

Prompt: "$prompt"

Entities: $entities

Elke entiteit heeft een device id, name, state, actions to perform, brightness(0-255), en HS color(Hue(0-360),Saturation(0-100)), gescheiden door "<>". Gebruik deze informatie om de volgende taken uit te voeren:

- Identificeer elke entiteit in de prompt. De locatie of ruimte van de entiteit is altijd te vinden in de naam van de entiteit direct na "light" of "lamp". Bijvoorbeeld, in "keukenlamp_zijkant", is "keuken" de locatie. Baseer je beslissing verder op details zoals kleur en helderheid (fel of zacht).
- Kies alleen de entiteiten die exact overeenkomen met de beschrijvingen in de prompt.
- Bepaal de gewenste actie voor elk entity, rekening houdend met de huidige status.
- Voeg brightness (0-255) toe indien gespecificeerd; anders laat leeg.
- Voeg HS color als "Hue(0-360),Saturation(0-100)" toe indien gespecificeerd; anders laat leeg.

Je antwoord moet voldoen aan het volgende JSON Template formaat:
{ "entities": [ { "id": "", "action": "", "brightness": "", "hs_color": "" } ], "assistant": "" }

In het "assistant" veld, geef in natuurlijke taal een duidelijke uitleg over de uitgevoerde acties."""
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