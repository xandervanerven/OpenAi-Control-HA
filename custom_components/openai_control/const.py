"""Constants for the OpenAI Control integration."""

DOMAIN = "openai_control"

ENTITY_TEMPLATE = """$id<>$status<>$action
"""
COLOR_ENTITY_TEMPLATE = """$id<>$status<>$action<>$brightness<>$hs_color
"""
TEST_ENTITY_TEMPLATE = """$id<>$status<>$action<>$brightness<>$hs_color
"""

PROMPT_TEMPLATE = """
Based on the given prompt, you need to identify the relevant entities in the list below and perform the appropriate actions for each.

Prompt: "$prompt"

Entities: $entities

Each entity has an entity id, state, possible actions to perform, separated by "<>".
Use this information to complete the following tasks:

- Identify and select the entity or entities from the prompt that match the description. The room of the entity can always be found in the name of the entity immediately after "light.", for example in "kitchenlamp_ceiling", "kitchen" is the room. If a general room, such as "living room" is mentioned, then select all entities that have this room in their name.
- Determine the desired action for each selected entity, taking into account their current state.

Your answer should conform to the following JSON Template format:
JSON Template: { "entities": [ { "id": "", "action": "" } ], "assistant": "" }

In the "assistant" field, provide a natural language response of the actions taken.
"""
DUTCH_PROMPT_TEMPLATE = """
Op basis van de gegeven prompt, moet je de relevante entiteiten identificeren in de onderstaande lijst en de juiste acties uitvoeren voor elk van hen.

Prompt: "$prompt"

Entities: $entities

Elke entiteit heeft een entity id, state, possible actions to perform, gescheiden door "<>".
Gebruik deze informatie om de volgende taken uit te voeren:

- Identificeer en kies de entiteit of entiteiten in de prompt die overeenkomen met de omschrijving. De ruimte van de entiteit is altijd te vinden in de naam van de entiteit direct na "light.", bijvoorbeeld in "keukenlamp_plafond" is "keuken" de ruimte. Als er wordt verwezen naar een algemene ruimte zoals "woonkamer", selecteer dan alle entiteiten die deze ruimte in hun naam hebben.
- Bepaal de gewenste actie voor elke geselecteerde entiteit, rekening houdend met hun huidige status.

Je antwoord moet voldoen aan het volgende JSON Template formaat:
{ "entities": [ { "id": "", "action": "" } ], "assistant": "" }

In het "assistant" veld geef je in natuurlijke taal antwoord over de uitgevoerde acties.
"""
COLOR_PROMPT_TEMPLATE = """
Based on the given prompt, you need to identify the relevant entities in the list below and perform the appropriate actions for each.

Prompt: "$prompt"

Entities: $entities

Each entity has an entity id, state, possible actions to perform, brightness (0-255), and HS color (Hue(0-360), Saturation(0-100)), separated by "<>".
Use this information to complete the following tasks:

- Identify and select the entity or entities from the prompt that match the description. The room of the entity can always be found in the name of the entity immediately after "light.", for example in "kitchenlamp_ceiling", "kitchen" is the room. If a general room, such as "living room" is mentioned, then select all entities that have this room in their name.
- Determine the desired action for each selected entity, taking into account their current state.
- If the brightness is mentioned in the prompt, it can be a specific value or a descriptive term indicating the brightness. Interpret the user's intention accordingly. The brightness value must be between 0 (off) and 255 (maximum). If brightness is not specified do not change it.
- Add HS color as "Hue(0-360),Saturation(0-100)" if specified, if color is not specified, do not change it.

Your answer should conform to the following JSON Template format:
{ "entities": [ { "id": "", "action": "", "brightness": "", "hs_color": "" } ], "assistant": "" }

In the "assistant" field, provide a natural language response of the actions taken.
"""
DUTCH_COLOR_PROMPT_TEMPLATE = """
Op basis van de gegeven prompt, moet je de relevante entiteiten identificeren in de onderstaande lijst en de juiste acties uitvoeren voor elk van hen.

Prompt: "$prompt"

Entities: $entities

Elke entiteit heeft een entity id, state, possible actions to perform, brightness (0-255), en HS color (Hue(0-360),Saturation(0-100)), gescheiden door "<>".
Gebruik deze informatie om de volgende taken uit te voeren:

- Identificeer en kies de entiteit of entiteiten in de prompt die overeenkomen met de omschrijving. De ruimte van de entiteit is altijd te vinden in de naam van de entiteit direct na "light.", bijvoorbeeld in "keukenlamp_plafond" is "keuken" de ruimte. Als er wordt verwezen naar een algemene ruimte zoals "woonkamer", selecteer dan alle entiteiten die deze ruimte in hun naam hebben.
- Bepaal de gewenste actie voor elke geselecteerde entiteit, rekening houdend met hun huidige status.
- Als de brightness in de prompt wordt vermeld, dit kan een specifieke waarde of een beschrijvende term zijn die de brightness aangeeft, interpreteer dan de intentie van de gebruiker. De brightness waarde moet liggen tussen 0 (uit) en 255 (maximaal). Als brightness niet wordt vermeld verander deze dan niet.
- Voeg HS color als "Hue(0-360),Saturation(0-100)" toe indien gespecificeerd, als kleur niet wordt vermeld verander deze dan niet.

Je antwoord moet voldoen aan het volgende JSON Template formaat:
{ "entities": [ { "id": "", "action": "", "brightness": "", "hs_color": "" } ], "assistant": "" }

In het "assistant" veld geef je in natuurlijke taal antwoord over de uitgevoerde acties.
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