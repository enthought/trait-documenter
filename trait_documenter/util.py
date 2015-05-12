import ast
import inspect
from _ast import ClassDef, Assign


def get_trait_definition(parent, name, container='class_attribute'):
    """ Retrieve the Trait attribute definition
    """
    # Get the class source.
    source = inspect.getsource(parent)

    # Get the HasTraits class definition
    nodes = ast.parse(source)
    for node in ast.iter_child_nodes(nodes):
        if isinstance(node, ClassDef):
            parent_node = node
            break
    else:
        message = 'Could not find parent definition {} for {}'
        raise RuntimeError(message.format(parent, name))

    # Get the trait definition
    for node in ast.iter_child_nodes(parent_node):
        if isinstance(node, Assign):
            name = node.targets[0]
            if name.id == name:
                break
    else:
        raise RuntimeError('Could not find trait definition')

    endlineno = name.lineno
    for item in ast.walk(node):
        if hasattr(item, 'lineno'):
            endlineno = max(endlineno, item.lineno)

    definition_lines = [
        line.strip()
        for line in source.splitlines()[name.lineno-1:endlineno]]
    definition = ''.join(definition_lines)
    equal = definition.index('=')
    return definition[equal + 1:].lstrip()
