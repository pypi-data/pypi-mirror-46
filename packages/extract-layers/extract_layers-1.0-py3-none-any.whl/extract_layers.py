"""CLI for extracting layers from an Illustrator-exported SVG"""

import sys
import os
import copy

import click
import xmltodict

class Catchable(Exception):
    """An exception that the CLI can catch"""
class NoChildrenException(Catchable):
    """We expect a node to have children, but it has none"""
class FileExistsException(Catchable):
    """We want to write to a file but it already exists"""
class DuplicateLayerException(Catchable):
    """A layer name already exists"""

def sanitize(string):
    """Make a string safe for use as a filename"""
    return string.replace("/", "-")

def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)

def warn(message):
    """Print a warning message"""
    eprint(f"Warning: {message}")

def error(message):
    """Print an error message"""
    eprint(f"Error: {message}")

def get_children(node):
    """Finds the key/value pair of the given node dictionary that represents
    the list of its children
    """
    for tag, element in node.items():
        if isinstance(element, list):
            return tag, element
    raise NoChildrenException("No layers found.")

def extract_layers(output_directory, overwrite):
    """Extracts layers from stdin and places them in output_directory"""

    eprint("Reading from stdin...")
    tree = xmltodict.parse(sys.stdin.read())

    if os.listdir(output_directory) and not overwrite:
        warn(f'output directory "{output_directory}" is not empty!')

    # mkdir -p
    os.makedirs(output_directory, exist_ok=True)

    children_key, children = get_children(tree["svg"])
    group_indices = [index for index, child in enumerate(children) if "@data-name" in child]

    already_extracted = set()

    # for each direct child of the SVG with the "data-name" attribute
    for active_group_index in group_indices:
        # make a copy of the entire tree
        working_tree = copy.deepcopy(tree)

        # filter out all layers except the current one
        filtered = [child for index, child in enumerate(children) if index is active_group_index]
        working_tree["svg"][children_key] = filtered

        # unparse dictionary back to XML
        unparsed = xmltodict.unparse(working_tree, pretty=True)

        name = children[active_group_index]["@data-name"]
        sanitized = sanitize(name)
        if sanitized in already_extracted:
            raise DuplicateLayerException(f'Duplicate layer name "{sanitized}"!')

        output_file = os.path.join(output_directory, f"{sanitized}.svg")
        if os.path.exists(output_file) and not overwrite:
            raise FileExistsException(f'File "{output_file}" already exists!')
        if os.path.isdir(output_file):
            raise FileExistsException(f'File "{output_file}" is a directory!')

        with open(output_file, "w") as output_pointer:
            output_pointer.write(unparsed)
        eprint(f'Successfully extracted "{output_file}"')

        # mark the layer as extracted
        already_extracted.add(sanitized)

@click.command()
@click.option("--output-directory", required=True, help="Directory in which to save the layers.")
@click.option("--overwrite", is_flag=True, help="Clobber existing files.")
def interface(**args):
    """Extracts layers of an Illustrator-exported SVG and saves them as individual SVG files"""
    try:
        extract_layers(**args)
    except Catchable as exception:
        error(exception)

if __name__ == "__main__":
    interface()
