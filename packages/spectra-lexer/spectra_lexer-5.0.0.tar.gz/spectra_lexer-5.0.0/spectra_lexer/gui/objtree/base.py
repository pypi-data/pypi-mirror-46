from .collection import ContainerCollection
from spectra_lexer.core import Component
from spectra_lexer.system import file


class ObjectTreeTool(Component):
    """ Component for interactive tree operations. """

    file = resource("cmdline:objtree-icons", ":/assets/treeicons.svg", desc="File with all object tree icons")
    m_tree = resource("menu:Debug:View Object Tree...", ["tree_dialog_open"])
    debug_vars = resource("debug", {})  # Root variables to load on dialog open.

    resources: dict = None  # Dict of all resources such as object type icons.

    @on("tree_dialog_open")
    def open(self) -> None:
        """ Create the dialog and all resources using the current root vars dict. """
        if self.resources is None:
            # Make a raw root item by making an initial container from a 1-tuple containing the actual root object.
            # Rows of item data are produced upon iterating over the contents. Take the first item from the only row.
            container = ContainerCollection((self.debug_vars,))
            root = next(iter(container))[0]
            # Load the SVG XML icons. On failure, don't use icons.
            xml_dict = file.load(self.file, ignore_missing=True)
            # Each element ID without a starting underline is a valid icon.
            # Optional aliases for each icon may be present, separated by spaces.
            icon_ids = {d["id"]: k.split() for k, v in xml_dict["spectra_types"].items() for d in v}
            self.resources = {"root_item": root, "xml_bytes": xml_dict["raw"], "icon_ids": icon_ids}
        self.open_dialog(self.resources)

    def open_dialog(self, resources:dict) -> None:
        raise NotImplementedError
