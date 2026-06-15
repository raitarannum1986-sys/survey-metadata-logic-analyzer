LOGIC_TAGS = {
    "Predicates",
    "Predicate",
    "QuestionTriggers",
    "Routing"
}

def extract_logic(root):

    logic_items = []

    for elem in root.iter():

        if elem.tag in LOGIC_TAGS:

            logic_items.append({
                "tag": elem.tag,
                "entity_id": elem.attrib.get(
                    "EntityId",
                    ""
                )
            })

    return logic_items