# -*- coding: utf-8 -*-

import docx
from pyloco import Task

class Docx2text(Task):
    """extracts structured texts from a Microsoft Word file

'docx2text' task extracts texts from a Microsoft Word file while keeping
its original structure. For example, it outputs tables of the Word file in
the form of a nested Python dictionary of {<table no.>: {<row no.>:
{<cell no.>: text, ...}, ... }, ...}. A following task may take advantage
of this structural information for selecting a right text in the output.

Example(s)
----------

Assuming my.docx has tables, following command extracts texts from
the tables of the docx file and print extracted texts on screen

>>> pyloco docx2text my.docx -- print
"""

    name = "docx2text"
    version = "0.1.2"

    def __init__(self, parent):

        self.add_data_argument("path", type=str, help="input MS Word file")

        self.add_option_argument("-t", "--type", metavar="type",
                default=["table"], action="append",
                help="docx object type to extract (default='table')") 

        self.register_forward("data", help="output items extracted from "
                              "the input MS Word file")

    def perform(self, targs):

        docf = docx.Document(targs.path)
        items = {}

        for type in targs.type:
            handler = getattr(self, type, None)

            if handler:
                items[type] = handler(docf)

            else:
                raise Exception("Unknown element type: %s" % type)

        self.add_forward(data=items)

    def table(self, df):

        output = {}

        for tidx, table in enumerate(df.tables):
            tdict = {}
            output[tidx] = tdict

            for ridx, row in enumerate(table.rows):
                rdict = {}
                tdict[ridx] = rdict

                for cidx, cell in enumerate(row.cells):
                    rdict[cidx] = cell.text.strip()

        return output

