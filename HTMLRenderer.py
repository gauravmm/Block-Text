#!/usr/bin/python3

from Renderer import AbstractRenderer


class HTMLRenderer(AbstractRenderer):
    def render(self, layoutWrapper):
        lines = layoutWrapper.get()
        for ln in lines:
            for r in range(0, layoutWrapper.getLineHeight()):
                print("".join(self.glyphTransform(col[r]) for col in ln))
            print()
            print("".join(self.glyphTransform(c) for c in
                  [True, False] * (layoutWrapper.getLineWidth() // 2)))
            print()
