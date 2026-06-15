from graphviz import Digraph

def build_basic_flow(questions):

    dot = Digraph()

    for q in questions:

        dot.node(
            q["name"],
            f"{q['name']}\n({q['type']})"
        )

    for i in range(len(questions)-1):

        dot.edge(
            questions[i]["name"],
            questions[i+1]["name"]
        )

    return dot