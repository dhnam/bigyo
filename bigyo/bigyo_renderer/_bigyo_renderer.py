"""
Bigyo renderer file
"""

from abc import ABC, abstractmethod
from typing import Optional
from wcwidth import wcswidth, wcwidth


class BigyoRenderer(ABC):
    """
    Abstract Base Bigyo rendering strategy.

    Bigyo rendering strategy defines how :class:`Bigyo` generates side by side comparison lines.

    :param sep: Separator for separate two compared lines, defaults to "|"
    :param mark_unchanged: Flag to decide :class:`Bigyo` whether it passes line as-is
                          or mark unchanged line with "  " indicator, defaultes to False
    """
    def __init__(self, sep: str="|", mark_unchanged: bool=False):
        self.maxlen = -1
        self.sep = sep
        self.mark_unchanged = mark_unchanged

    def join_with_spaces(self, left: str, right: str) -> str:
        """
        Joins two string with separater `self.sep`.

        Spacing is added to make it look nicer.

        :param left: Left string to be printed
        :param right: Right string to be printed
        :return: joined string with appropriate spacing and separater
        """
        left_width = wcswidth(left)
        if left_width == -1 or wcswidth(right) == -1:
            raise ValueError("Control character was included in string which has unknown effect while printing.")
        return f"{left}{' '*(self.maxlen - left_width)}{self.sep}{right}" + "\n"

    @abstractmethod
    def render(self, *, left: str="", right: str="",\
               left_replace: Optional[str]=None, right_replace: Optional[str]=None) -> str:
        """
        Function to actually build comparison lines.

        :param left: Left string compared
        :param right: Right string compared
        :param left_replace: Diff line generated by :class:`Bigyo`
                            for :param:`left`, defaults to None
        :param right_replace: Diff line generated by :class:`Bigyo`
                            for :param:`right`, defaults to None
        :return: Compared line
        """

class SimpleBigyoRenderer(BigyoRenderer):
    """
    Simple Bigyo rendering stratgy.

    Will produce side-by-side comparison, with difference is displayed as separated line.

    :param sep: Separator for separate two compared lines, defaults to "|"
    :param mark_unchanged: Flag to decide :class:`Bigyo` whether it passes line as-is
                          or mark unchanged line with "  " indicator, defaultes to False
    """
    def render(self, *, left: str="", right: str="",\
               left_replace: Optional[str]=None, right_replace: Optional[str]=None) -> str:
        def replace_unicode_match(string: str, replace: str) -> str:
            ret = ""
            for next_char, next_replace in zip(string, replace):
                if wcwidth(next_char) == 1:
                    ret += next_replace
                elif wcwidth(next_char) == 2:
                    ret += next_replace * 2
            return ret

        diff_line = self.join_with_spaces(left, right)
        if any([left_replace, right_replace]):
            diff_line += self.join_with_spaces(
                "" if left_replace is None else replace_unicode_match(left, left_replace),
                "" if right_replace is None else replace_unicode_match(right, right_replace),
                )
        return diff_line


class OnelineBigyoRenderer(BigyoRenderer):
    """
    One-line Bigyo rendering stratgy.

    Will produce side-by-side comparison, with difference is displayed in-line with marks.

    Mark is changable by __init__ method.

    Default mark is ("<", ">") for added difference, (">", "<") for removed difference.

    So <added difference will be shown like this>, and >removed difference will be shown like this<.

    :param sep: Separator for separate two compared lines, defaults to "|"
    :param mark_unchanged: Flag to decide :class:`Bigyo` whether it passes line as-is
                          or mark unchanged line with "  " indicator, defaultes to True
    :param add_mark: Characters to mark range of added difference, defaultes to ("<", ">")
    :param delete_mark: Characters to mark range of removed difference, defaultes to (">", "<")
    """
    def __init__(self, sep="|", mark_unchanged=True,\
                 add_mark: tuple[str, str]=("<", ">"), delete_mark: tuple[str, str]=(">", "<")):
        super().__init__(sep, mark_unchanged)
        self.add_mark = add_mark
        self.delete_mark = delete_mark

    def render(self, *, left: str = "", right: str = "",\
               left_replace: Optional[str] = None, right_replace: Optional[str] = None) -> str:
        delete = 0
        add = 1
        def combine_str(string, op, place:list[bool] = None):
            combined: str = ""
            if place is None:
                place = [True] * len(string)
            assert len(place) == len(string)
            in_editing: bool = False
            for next_char, is_combined in zip(string, place):
                if is_combined != in_editing:
                    if not in_editing:
                        combined += self.delete_mark[0] if op == delete else self.add_mark[0]
                    else:
                        combined += self.delete_mark[1] if op == delete else self.add_mark[1]
                    in_editing = not in_editing
                combined += next_char
            if in_editing:
                combined += self.delete_mark[1] if op == delete else self.add_mark[1]
            return combined

        processed: list[str] = ["", ""]
        for i, (string, cue) in enumerate([(left, left_replace), (right, right_replace)]):
            if string == "":
                processed[i] = ""
                continue
            line_cue, string = string[:2], string[2:]
            cue_place = [False] * len(string)
            if cue is None:
                cue_place = [True] * len(string)
            else:
                cue = cue[2:]
                for j, next_char in enumerate(cue):
                    cue_place[j] = (next_char != " ")

            if line_cue == "  ":
                processed[i] = string
            elif line_cue == "- ":
                processed[i] = combine_str(string, delete, cue_place)
            elif line_cue == "+ ":
                processed[i] = combine_str(string, add, cue_place)
        return self.join_with_spaces(*processed)
