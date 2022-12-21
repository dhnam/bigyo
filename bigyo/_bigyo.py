"""
File with main bigyo class
"""

import difflib
from typing import Sequence, Iterator, Optional
from wcwidth import wcswidth
from bigyo.bigyo_renderer import BigyoRenderer, SimpleBigyoRenderer

class Bigyo:
    """
    Bigyo (ko: 비교, comparison) is class for side-by-side comparison, using `difflib` as its engine.

    Simply replace::

       difflib.Differ().compare(a, b)

    to::

       Bigyo().compare()

    and you'll get nice side-by-side comparison.

    :param bigyo_renderer: Bigyo rendering strategy, which decides way to render comparison. It can be :class:`BigyoRenderer` object, or None (which uses :class:`SimpleBigyoRenderer`), defaults to None
    """
    def __init__(self, bigyo_renderer: Optional[BigyoRenderer]=None):
        self._recent_indicator: str = ''
        self._recent_lines: list[str] = []
        if bigyo_renderer is None:
            bigyo_renderer = SimpleBigyoRenderer()
        self.bigyo_renderer = bigyo_renderer

    # new line patterns: " ", "-", "+", "-+", "-?+", "-+?", "-?+?"
    # tokens: " ", "-", "+", "?"
    def _completed_pattern(self, indicator: str) -> Iterator[str]:
        assert self._recent_indicator.startswith(indicator)
        if indicator == " ":
            yield self.bigyo_renderer.render(
                left=self._recent_lines[0],
                right=self._recent_lines[0],
                )
            self._recent_indicator = self._recent_indicator[1:]
            self._recent_lines = self._recent_lines[1:]
        elif indicator == "+":
            yield self.bigyo_renderer.render(
                right=self._recent_lines[0],
                )
            self._recent_indicator = self._recent_indicator[1:]
            self._recent_lines = self._recent_lines[1:]
        elif indicator == "-":
            yield self.bigyo_renderer.render(
                left=self._recent_lines[0],
                )
            self._recent_indicator = self._recent_indicator[1:]
            self._recent_lines = self._recent_lines[1:]
        elif indicator == "-+":
            yield self.bigyo_renderer.render(
                left=self._recent_lines[0],
                right=self._recent_lines[1],
                )
            self._recent_indicator = self._recent_indicator[2:]
            self._recent_lines = self._recent_lines[2:]
        elif indicator == "-?+":
            if self.bigyo_renderer.mark_unchanged:
                self._recent_lines[2] = " " + self._recent_lines[2][1:]
            yield self.bigyo_renderer.render(
                left=self._recent_lines[0],
                right=self._recent_lines[2],
                left_replace=self._recent_lines[1],
                )
            self._recent_indicator = self._recent_indicator[3:]
            self._recent_lines = self._recent_lines[3:]
        elif indicator == "-+?":
            if self.bigyo_renderer.mark_unchanged:
                self._recent_lines[0] = " " + self._recent_lines[0][1:]
            yield self.bigyo_renderer.render(
                left=self._recent_lines[0],
                right=self._recent_lines[1],
                right_replace=self._recent_lines[2],
                )
            self._recent_indicator = self._recent_indicator[3:]
            self._recent_lines = self._recent_lines[3:]
        elif indicator == "-?+?":
            yield self.bigyo_renderer.render(
                left=self._recent_lines[0],
                right=self._recent_lines[2],
                left_replace=self._recent_lines[1],
                right_replace=self._recent_lines[3],
                )
            self._recent_indicator = self._recent_indicator[4:]
            self._recent_lines = self._recent_lines[4:]

    def compare(self, left: Sequence[str], right: Sequence[str]) -> Iterator[str]:
        """
        Generator for generating side-by-side comparison.

        :param left: Left sequence to compare
        :param right: Right sequence to compare
        :return: Iterator, where `next()` call returns line with its difference.
        """
        self.bigyo_renderer.maxlen = max(map(wcswidth, map(lambda x: x.strip("\n"), left))) + 2
        lines = difflib.Differ().compare(left, right)

        for next_line in lines:
            next_line = next_line.strip("\n")
            self._recent_indicator += next_line[0]
            self._recent_lines.append(next_line)

            if self._recent_indicator == " ":
                yield from self._completed_pattern(" ")
            elif self._recent_indicator == "+":
                yield from self._completed_pattern("+")
            elif self._recent_indicator == "- ":
                yield from self._completed_pattern("-")
                yield from self._completed_pattern(" ")
            elif self._recent_indicator == "--":
                yield from self._completed_pattern("-")
            elif self._recent_indicator == "-+ ":
                yield from self._completed_pattern("-+")
                yield from self._completed_pattern(" ")
            elif self._recent_indicator == "-+-":
                yield from self._completed_pattern("-+")
            elif self._recent_indicator == "-++":
                yield from self._completed_pattern("-+")
                yield from self._completed_pattern("+")
            elif self._recent_indicator == "-+?":
                yield from self._completed_pattern("-+?")
            elif self._recent_indicator in ("-? ",  "-?-" , "-??"):
                raise Exception(self._recent_indicator)
            elif self._recent_indicator == "-?+ ":
                yield from self._completed_pattern("-?+")
                yield from self._completed_pattern(" ")
            elif self._recent_indicator == "-?+-":
                yield from self._completed_pattern("-?+")
            elif self._recent_indicator == "-?++":
                yield from self._completed_pattern("-?+")
                yield from self._completed_pattern("+")
            elif self._recent_indicator == "-?+?":
                yield from self._completed_pattern("-?+?")

        if self._recent_indicator != "":
            yield from self._completed_pattern(self._recent_indicator)

    def comparison_string(self, left: Sequence[str], right: Sequence[str]) -> str:
        """
        Return full compared string at once.

        Is just ``return ''.join(self.compare(left, right))``. Guess it will quite comes in handy.

        :param left: Left sequence to compare
        :param right: Right sequence to compare
        """
        return ''.join(self.compare(left, right))

if __name__ == "__main__":
    a = ["Hello, World\n", "안녕, 세계"]
    b = ["Helo, Wold!\n", "안넝, 새개!"]
    print(Bigyo().comparison_string(a, b))
