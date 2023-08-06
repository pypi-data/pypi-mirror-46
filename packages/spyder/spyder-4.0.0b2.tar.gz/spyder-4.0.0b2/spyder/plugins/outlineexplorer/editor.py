# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""Outline explorer editor server"""

from spyder.plugins.outlineexplorer.api import OutlineExplorerProxy


class OutlineExplorerProxyEditor(OutlineExplorerProxy):
    def __init__(self, editor, fname):
        self._editor = editor
        self.fname = fname

    def is_python(self):
        return self._editor.is_python()

    def get_id(self):
        return self._editor.get_document_id()

    def give_focus(self):
        self._editor.clearFocus()
        self._editor.setFocus()

    def get_cursor_line_number(self):
        return self._editor.get_cursor_line_number()

    def get_outlineexplorer_data(self):
        oe_data = self._editor.get_outlineexplorer_data()
        self._editor.has_cell_separators = oe_data.pop(
            'found_cell_separators', False)
        return oe_data

    def get_line_count(self):
        return self._editor.get_line_count()

    def parent(self):
        return self._editor.parent()
