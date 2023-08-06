"""
Module with helper classes to generate Sphinx RST documents.
"""


class RSTDocument(object):
    """
    Helper class for generating an reStructuredText (RST) document

    :ivar document: The string with the RST document
    :ivar newline: Newline string
    """
    ADMONITIONS = ['attention', 'caution', 'danger', 'error', 'hint', 'important', 'note', 'tip', 'warning']
    ALIGN = ['top', 'middle', 'bottom', 'left', 'center', 'right']

    def __init__(self):
        """Initialize empty RST document"""
        self.document = ""
        self.newline = "\n"
        self.default_indent = '    '

    @staticmethod
    def __get_headingline(title, heading_char):
        """Create a heading line for a given title"""
        heading = ""
        for i in range(len(title)):
            heading += heading_char
        return heading

    def add_text(self, text):
        """
        Add the given text to the document
        :param text: String with the text to be added
        """
        self.document += text

    def add_part(self, title):
        """
        Add a document part heading

        :param title: Title of the reading
        """
        heading = RSTDocument.__get_headingline(title, '#')
        self.document += (heading + self.newline)
        self.document += (title + self.newline)
        self.document += (heading + self.newline)
        self.document += self.newline

    def add_chapter(self, title):
        """
        Add a document chapter heading

        :param title: Title of the reading
        """
        heading = RSTDocument.__get_headingline(title, '*')
        self.document += (heading + self.newline)
        self.document += (title + self.newline)
        self.document += (heading + self.newline)
        self.document += self.newline

    def add_label(self, label):
        """
        Add a section label
        :param label: name of the label
        """
        self.document += ".. _%s:" % label
        self.document += self.newline + self.newline

    @staticmethod
    def get_reference(label, link_title=None):
        """
        Get RST text to create a reference to the given label
        :param label: Name of the label to link to
        :param link_title: Text for the link
        :return: String with the inline reference text
        """
        if link_title is not None:
            return ":ref:`%s <%s>`" % (link_title, label)
        else:
            return ":ref:`%s`" % label

    @staticmethod
    def get_numbered_reference(label):
        return ":numref:`%s`" % label

    def add_section(self, title):
        """
        Add a document section heading

        :param title: Title of the reading
        """
        heading = RSTDocument.__get_headingline(title, '=')
        self.document += (title + self.newline)
        self.document += (heading + self.newline)
        self.document += self.newline

    def add_subsection(self, title):
        """
        Add a document subsection heading

        :param title: Title of the reading
        """
        heading = RSTDocument.__get_headingline(title, '-')
        self.document += (title + self.newline)
        self.document += (heading + self.newline)
        self.document += self.newline

    def add_subsubsection(self, title):
        """
        Add a document subsubsection heading

        :param title: Title of the reading
        """
        heading = RSTDocument.__get_headingline(title, '^')
        self.document += (title + self.newline)
        self.document += (heading + self.newline)
        self.document += self.newline

    def add_paragraph(self, title):
        """
        Add a document paragraph heading

        :param title: Title of the reading
        """
        heading = RSTDocument.__get_headingline(title, '"')
        self.document += (title + self.newline)
        self.document += (heading + self.newline)
        self.document += self.newline

    def add_code(self, code_block, code_type='python', show_line_numbers=True, emphasize_lines=None):
        """
        Add code block to the document
        :param code_block: String with the code block
        :param show_line_numbers: Bool indicating whether line number should be shown
        :param emphasize_lines: None or list of int with the line numbers to be highlighted
        :param code_type: The language type to be used for source code highlighting in the doctools doc
        """
        self.document += ".. code-block:: %s%s" % (code_type, self.newline)
        if show_line_numbers:
            self.document += self.indent_text(':linenos:') + self.newline
        if emphasize_lines is not None:
            self.document += self.indent_text(':emphasize-lines: ')
            for i, j in enumerate(emphasize_lines):
                self.document += str(j)
                if i < len(emphasize_lines)-1:
                    self.document += ','
            self.document += self.newline
        self.document += self.newline
        self.document += self.indent_text(code_block)  # Indent text by 4 spaces
        self.document += self.newline
        self.document += self.newline

    def indent_text(self, text, indent=None):
        """
        Helper function used to indent a given text by a given prefix. Usually 4 spaces.

        :param text: String with the text to be indented
        :param indent: String with the prefix to be added to each line of the string. If None then self.default_indent
                       will be used.

        :return: New string with each line indented by the current indent
        """
        curr_indent = indent if indent is not None else self.default_indent
        return curr_indent + curr_indent.join(text.splitlines(True))

    def add_list(self, content, indent=None, item_symbol='*'):
        """
        Recursively add a list with possibly multiple levels to the document
        :param content: Nested list of strings with the content to be rendered
        :param indent: Indent to be used for the list. Required for recursive indentation of lists.
        :param item_symbol: String with the symbol used to start a list item. Default: item='*'
        """
        indent = '' if indent is None else indent
        for item in content:
            if isinstance(item, list) or isinstance(item, tuple):
                self.add_list(item,
                              indent=indent+self.default_indent,
                              item_symbol=item_symbol)
            else:
                self.document += ('%s%s %s%s' % (indent, item_symbol, item, self.newline))
        self.document += self.newline

    def add_admonitions(self, atype, text):
        """
        Add an admonition to the text. Admonitions are specially marked "topics"
        that can appear anywhere an ordinary body element can

        :param atype: One of RTDDocument.ADMONITIONS
        :param text: String with the RTD formatted text to be shown or an RTDDocument object
                     containing the text to be rendered as part of the admonition
        """
        curr_text = text if not isinstance(text, RSTDocument) else text.document
        self.document += self.newline
        self.document += ".. %s::" % atype
        self.document += self.newline
        self.document += self.indent_text(curr_text)
        self.document += self.newline
        self.document += self.newline

    def add_include(self, filename, indent=None):
        """
        Include the file with the given name as part of this RST document

        :param filename: Name of the file to be included
        :param indent: Indent to be used for the include.

        """
        indent = '' if indent is None else indent
        self.document += "%s.. include:: %s" % (indent, filename)
        self.document += self.newline

    def add_figure(self,
                   img,
                   caption=None,
                   legend=None,
                   alt=None,
                   height=None,
                   width=None,
                   scale=None,
                   align=None,
                   target=None):
        """

        :param img: Path to the image to be shown as part of the figure.
        :param caption: Optional caption for the figure
        :type caption: String or RSTDocument
        :param legend: Figure legend
        :type legend: String or RST Document
        :param alt: Alternate text.  A short description of the image used when the image cannot be displayed.
        :param height: Height of the figure in pixel
        :type height: Int
        :param width: Width of the figure in pixel
        :type width: Int
        :param scale: Uniform scaling of the figure in %. Default is 100.
        :type scale: Int
        :param align: Alignment of the figure. One of RTDDocument.ALIGN
        :param target: Hyperlink to be placed on the image.
        """
        self.document += self.newline
        self.document += ".. figure:: %s" % img
        self.document += self.newline
        if scale is not None:
            self.document += (self.indent_text(':scale: %i' % scale) + ' %' + self.newline)
        if alt is not None:
            self.document += (self.indent_text(':alt: %s' % alt) + self.newline)
        if height is not None:
            self.document += (self.indent_text(':height: %i px' % height) + self.newline)
        if width is not None:
            self.document += (self.indent_text(':width: %i px' % width) + self.newline)
        if align is not None:
            if align not in self.ALIGN:
                raise ValueError('align not valid. Found %s expected one of %s' % (str(align), str(self.ALIGN)))
            self.document += (self.indent_text(':align: %s' % align) + self.newline)
        if target is not None:
            self.document += (self.indent_text(':target: %s' % target) + self.newline)
        self.document += self.newline
        if caption is not None:
            curr_caption = caption if not isinstance(caption, RSTDocument) else caption.document
            self.document += (self.indent_text(curr_caption) + self.newline)
        if legend is not None:
            if caption is None:
                self.document += (self.indent_text('.. ') + self.newline + self.default_indent + self.newline)
            curr_legend = legend if not isinstance(legend, RSTDocument) else legend.document
            self.document += (self.indent_text(curr_legend) + self.newline)
        self.document += self.newline

    def add_sidebar(self, text, title, subtitle=None):
        """
        Add a sidebar. Sidebars are like miniature, parallel documents that occur inside other
        documents, providing related or reference material.

        :param text: The content of the sidebar
        :type text: String or RSTDocument
        :param title: Title of the sidebar
        :type title: String
        :param subtitle: Optional subtitel of the sidebar
        :type subtitle: String
        """
        self.document += self.newline
        self.document += '.. sidebar:: ' + title + self.newline
        if subtitle is not None:
            self.document += (self.indent_text(':subtitle: %s' % subtitle) + self.newline)
        self.document += self.newline
        curr_text = text if not isinstance(text, RSTDocument) else text.document
        self.document += (self.indent_text(curr_text)) + self.newline + self.newline

    def add_topic(self, text, title):
        """
        Add a topic. A topic is like a block quote with a title, or a self-contained section with no subsections.

        :param text: The content of the sidebar
        :type text: String or RSTDocument
        :param title: Title of the sidebar
        :type title: String
        """
        self.document += self.newline
        self.document += '.. sidebar:: ' + title + self.newline
        self.document += self.newline
        curr_text = text if not isinstance(text, RSTDocument) else text.document
        self.document += (self.indent_text(curr_text)) + self.newline + self.newline

    @staticmethod
    def spec_to_yaml(spec):
        """
        Convert a given specification to yaml. Used by the add_spec function to render a spec
        as YAML in the RST document

        :param spec: Specification data structure
        :type spec: GroupSpec, DatasetSpec, AttributeSpec, LinkSpec

        :return: YAML string for the current specification
        """
        import json
        import sys

        try:
            from ruamel import yaml
        except ImportError:
            import yaml
        clean_spec = json.loads(json.dumps(spec, sort_keys=True, indent=4, separators=(',', ': ')))
        if sys.version_info[0] == 3:
            return yaml.dump(clean_spec, default_flow_style=False)
        else:
            return yaml.safe_dump(clean_spec, default_flow_style=False)

    def add_spec(self, spec):
        """
        Convert the given spec to RST and add it to the document

        :param spec: Specification data structure
        :type spec: GroupSpec, DatasetSpec, AttributeSpec, LinkSpec
        """
        self.add_code(RSTDocument.spec_to_yaml(spec), code_type='yaml')

    def add_latex_clearpage(self):
        self.document += self.newline
        self.document += ".. raw:: latex" + self.newline + self.newline
        self.document += self.default_indent + '\clearpage \\newpage' + self.newline + self.newline

    def add_table(self, rst_table, **kwargs):
        """
        Render an RSTtable in this document

        :param rst_table: RSTTable object to be rendered in this document
        :param kwargs: Arguments to be passed to the RSTTable.render
        """
        rst_table.render(self, **kwargs)

    def write(self, filename, mode='w'):
        """
        Write the document to file

        :param filename: Name of the output file
        :param mode: file open mode
        """
        outfile = open(filename, mode=mode)
        outfile.write(self.document)
        outfile.flush()
        outfile.close()


class RSTSectionLabelHelper(object):
    """
    Simple helper class used to generate section, table and other labels in the RST document
    to support cross-referencing.
    """

    @staticmethod
    def get_section_label(neurodata_type):
        """
        Get the label of the section with the documentation for the given neurodata_type

        :param neurodata_type: String with the name of the neurodata_type
        :return: String with the section label where the neurodatatype is described
        """
        return 'sec-' + neurodata_type

    @staticmethod
    def get_src_section_label(neurodata_type, generate_src_file=True, show_yaml_src=True):
        """
        Get the label for the section with the source YAML/JSON of the given neurodata_type.

        :param neurodata_type: String with the name of the neurodata_type
        :param generate_src_file: Bool indicating whether the source is rendered in a separate file
        :param show_yaml_src: Bool indicating whether the YAML source is being rendered at al.
        :return: String with the section label or None in case no sources are included as part of the documentation
        """
        if generate_src_file:
            return 'sec-' + neurodata_type + "-src"
        elif show_yaml_src:
            return RSTSectionLabelHelper.get_section_label(neurodata_type)
        else:
            None

    @staticmethod
    def get_group_table_label(parent):
        """
        Get the name of the reference for the table listing all subgroups for the parent neurodata_type

        :param parent: String with the name of the parent neurodata_type
        :return: String with label of the table
        """
        return 'table-'+parent+'-groups'

    @staticmethod
    def get_data_table_label(parent):
        """
        Get the name of the reference for the table listing all data for the parent

        :param parent: String with the name of the parent neurodata_type
        :return: String with label of the table
        """
        return 'table-'+parent+'-data'


class RSTTable(object):
    """
    Helper class to generate RST tables
    """

    def __init__(self, cols):
        """
        Initialize the RSTTable

        :param cols: List of strings with the column labels. Or int with the number of columns
        """
        self.__table = []
        self.__cols = cols if not isinstance(cols, int) else ([''] * cols)
        self.newline = "\n"

    def set_cell(self, row, col, text):
        if col >= len(self.__cols):
            raise ValueError('Column index out of bounds: col=%i , max_index=%i' % (col, len(self.__cols)-1))
        if row >= len(self.__table):
            raise ValueError('Row index out of bounds: row=%i , max_index=%i' % (row, len(self.__table)-1))
        self.__table[row][col] = text

    def __len__(self):
        return self.num_rows()

    def num_rows(self):
        """
        :return: Number of rows in the table
        """
        return len(self.__table)

    def num_cols(self):
        """
        :return: Number of columns in the table
        """
        return len(self.__cols)

    def add_row(self, row_values=None, replace_none=None, convert_to_str=True):
        """
        Add a row of values to the table
        :param row_values: List of all values for the current row (or None if an empty row should be added).
                           If values in the list contain newline strings then this will result in the creation
                           of a multiline row with as many lines as the larges cell (i.e. the cell with the largest
                           number of newline symbols).
        :param replace_none:  String to be used to replace None values in the row data (default=None, i.e., do not
                              replace None values)
        :param convert_to_str: Boolean indicating whether all row values should be converted to strings. (default=True)
        """
        row_vals = row_values if row_values is not None else ([''] * len(self.__cols))
        if replace_none:
            for i, v in enumerate(row_values):
                if v is None:
                    row_vals[i] = replace_none
        if convert_to_str:
            row_vals = [str(v) for v in row_vals]
        self.__table.append(row_vals)

    def set_col(self, col, text):
        if col >= len(self.__cols):
            raise ValueError('Column index out of bounds: col=%i , max_index=%i' % (col, len(self.__cols)-1))
        self.__cols[col] = text

    @staticmethod
    def table_row_divider(col_widths, style='='):
        """
        Create row divider for use in an RST table. This is mostly an internal helper function
        used by RSTTable.render but can be useful otherwise as well.

        :param col_widths: List of ints with the width of the columns of the table
        :param style: string with the style to be used for the row divider. Default: style='='
        :return: Python string with the row divider text
        """
        out = "    "
        for cw in col_widths:
            out += '+' + (cw+2) * style
        out += "+\n"
        return out

    @staticmethod
    def normalize_cell(cell, col_width):
        """
        Given the text for a cell create a fixed length string to fit a column with width col_width.
        This is mostly an internal helper function  used by RSTTable.render but can be useful
        otherwise as well.

        :param cell: String with the text content for the cell
        :param col_width: Target width for the column
        :return: cell text string padded with spaces to fit the column width
        """
        return " " + cell + (col_width - len(cell) + 1) * " "

    @staticmethod
    def render_row(col_widths, row, newline='\n'):
        """
        Render the text for a single row of an RSTTable. This is mostly an internal helper function
        used by RSTTable.render but can be useful otherwise as well.

        :param col_widths: List of ints with the width of the columns of the table
        :param row: List of strings with the text for each column. The text in each column may also contain
                    multiple lines indicated by the newline.
        :param newline: Newline symbol to be used for linebreaks. Default: newline='\n'
        :return: String with the text defining the rwo
        """
        row_lines = [r.split(newline) for r in row]
        num_lines = max([len(r) for r in row_lines])
        for r in row:
            if newline in r:
                max(num_lines, len(r.split(newline)))
        row_text = ''
        for l in range(num_lines):
            row_text += '    |'
            for ri in range(len(row)):
                cell = row_lines[ri][l] if len(row_lines[ri]) > l else ''
                row_text += RSTTable.normalize_cell(cell, col_width=col_widths[ri]) + '|'
            row_text += newline
        return row_text

    @staticmethod
    def cell_len(cell, newline='n'):
        """
        Simple helper function used to determine the width of a cell given by the longest
        text in a line. The text in a cell may consists of multiple lines separated by
        newline.
        :param cell: Text content of the cell
        :param newline: Newline symbol to be used for linebreaks. Default: newline='\n'
        :return: Integer indicating the max length of a line in the cell
        """
        return max(len(r) for r in cell.split(newline))

    def render(self,
               rst_doc=None,
               title=None,
               table_class='longtable',
               widths=None,
               ignore_empty=True,
               table_ref=None,
               latex_tablecolumns=None):
        """
        Render the table to an RSTDocument

        :param rst_doc: RSTDocument where the table should be rendered in or None if a new document should be created
        :param title: String with the optional title for the table
        :param table_class: Optional class for the table.  We here use 'longtable' as default. Set to None to use
                     the Sphinx default. Other table classes are: 'longtable', 'threeparttable', 'tabular', 'tabulary'
        :param widths: Optional list of width for the columns
        :param ignore_empty: Boolean indicating whether empty tables should be rendered (i.e., if False then
                    headings with no additional rows will be rendered) or if no table should be created
                    if no data rows exists (if set to True). (default=True)
        :param table_ref: Name of the reference to be used for the table
        :param latex_tablecolumns: Latex columns description to be rendered as part of the Sphinx tabularcolumns::
                    argument. E.g. '|p{3.5cm}|p{1cm}|p{10.5cm}|'
        """
        if len(self.__table) == 0 and ignore_empty:
            return rst_doc if rst_doc is not None else RSTDocument()

        col_widths = [max(out)+2 for out in map(list,
                                                zip(*[[RSTTable.cell_len(item, rst_doc.newline) for item in row]
                                                      for row in ([self.__cols, ] + self.__table)]))]
        rst_doc = rst_doc if rst_doc is not None else RSTDocument()
        rst_doc.add_text(rst_doc.newline)
        if latex_tablecolumns:
            rst_doc.add_text('.. tabularcolumns:: %s%s' % (latex_tablecolumns, rst_doc.newline))
        if table_ref is not None:
            rst_doc.add_label(table_ref)
        rst_doc.add_text('.. table::')
        if title:
            rst_doc.add_text(' ' + title)
        rst_doc.add_text(rst_doc.newline)
        if widths:
            rst_doc.add_text('    :widths:')
            for i in widths:
                rst_doc.add_text(' %i' % i)
            rst_doc.add_text(rst_doc.newline)
        if table_class is not None:
            rst_doc.add_text('    :class: ' + table_class + rst_doc.newline)
        rst_doc.add_text(rst_doc.newline)

        # Render the table header
        rst_doc.add_text(RSTTable.table_row_divider(col_widths=col_widths, style='-'))
        rst_doc.add_text(RSTTable.render_row(col_widths, self.__cols, rst_doc.newline))
        rst_doc.add_text(RSTTable.table_row_divider(col_widths=col_widths, style='='))

        # Render the main table contents
        for row in self.__table:
            rst_doc.add_text(RSTTable.render_row(col_widths, row, rst_doc.newline))
            rst_doc.add_text(RSTTable.table_row_divider(col_widths=col_widths, style='-'))
        rst_doc.add_text(rst_doc.newline)
        rst_doc.add_text(rst_doc.newline)

        # Return the table
        return rst_doc
