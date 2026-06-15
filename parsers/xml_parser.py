from lxml import etree

def load_xml(uploaded_file):
    tree = etree.parse(uploaded_file)
    return tree.getroot()


def get_tag_counts(root):
    counts = {}

    for elem in root.iter():
        counts[elem.tag] = counts.get(elem.tag, 0) + 1

    return counts