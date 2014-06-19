#!/usr/bin/python3

from Renderers import AbstractRenderer


class HTMLRenderer(AbstractRenderer):
    def __init__(self):
        super(HTMLRenderer).__init__()
        self.cellct = 800
        self.cellsz = "10"

    def render(self, layoutWrapper):
        lines = layoutWrapper.get()
        table = []
        for ln in lines:
            self.cellsz = str(self.cellct // len(ln))
            table.extend(self.mkRow(self.mkCell(col[r]) for col in ln) for r in range(layoutWrapper.getLineHeight()))
            # Add the gap between lines:
            table.append(self.mkRow(self.mkCell(False) for col in ln))

        return self.mkTable(table)

    def wrapTables(self, tbls):
        return self.mkPage("<hr />".join(tbls))

    def mkCell(self, val):
        return "<td class='{}'>&nbsp;</td>".format("b" if val else "w")

    def mkRow(self, val):
        return "<tr>" + "".join(val) + "</tr>"

    def mkTable(self, table):
        return "<table cellspacing='0' cellpadding='0'>" + "".join(table) + "</table>"

    def mkPage(self, table):
        return """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <title>Render</title>
    <style type="text/css">
        body {
            font-size: 1%;
        }
        td {
            width: """ + self.cellsz + """px;
            height: """ + self.cellsz + """px;
        }
        td.b {
            background-color: #000;
        }
        td.w {
            background-color: #FFF;
        }
        hr {
            margin: """ + self.cellsz + """px auto;
        }
    </style>
  </head>
  <body>
""" + table + """
  </body>
</html>
"""
