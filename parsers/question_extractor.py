QUESTION_TYPES = {
    "Single",
    "Multi",
    "Open",
    "Numeric",
    "Grid",
    "Ranking",
    "Info"
}


def extract_questions(root):

    questions = []

    hidden_count = 0

    for elem in root.iter():

        if elem.tag not in QUESTION_TYPES:
            continue

        variable_type = elem.attrib.get(
            "VariableType",
            "Normal"
        )

        if variable_type == "Hidden":
            hidden_count += 1

        name_node = elem.find("Name")

        question_name = (
            name_node.text
            if name_node is not None
            else f"Entity_{elem.attrib.get('EntityId')}"
        )

        questions.append({
            "name": question_name,
            "type": elem.tag,
            "variable_type": variable_type,
            "entity_id": elem.attrib.get("EntityId")
        })

    return questions, hidden_count