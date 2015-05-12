import ast
import inspect
from _ast import ClassDef, Assign


def get_trait_definition(parent, trait_name):
    """ Retrieve the Trait attribute definition from the source file.

    Parameters
    ----------
    parent :
        The module or class where the trait is defined.

    trait_name : string
        The name of the trait.

    Returns
    -------
    definition : string
        The trait definition from the source.

    """
    # Get the class source.
    source = inspect.getsource(parent)
    nodes = ast.parse(source)

    if not inspect.ismodule(parent):
        # Get the HasTraits class definition
        for node in ast.iter_child_nodes(nodes):
            if isinstance(node, ClassDef):
                parent_node = node
                break
            else:
                message = 'Could not find class definition {} for {}'
            raise RuntimeError(message.format(parent, trait_name))
    else:
        parent_node = nodes

    # Get the trait definition
    for node in ast.iter_child_nodes(parent_node):
        if isinstance(node, Assign):
            name = node.targets[0]
            if name.id == trait_name:
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
