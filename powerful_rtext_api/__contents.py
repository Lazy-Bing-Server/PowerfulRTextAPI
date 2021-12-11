from mcdreforged.api.rtext import RColor, RStyle, RText, RTextBase, RAction
from parse import parse
from typing import Tuple, Optional, Union

from .__constants import *


def text_to_rtext(text: str) -> Tuple[Optional[RTextBase], str]:
    """
    Transfer a text in following format to RText objects:

    [{style_marks} {msg}]<{hover_text}>}>({click_events}||{click_contents})

    :param text: The original text to transfer
    :return: An RTextBase object that can be easily edited by Python programs
    """
    result, others = __base_rtext_convert(text)
    if result == text:
        return None, text

    if others is not None:
        parsed = parse("<{hover}>{others}", others.rstrip() + ' ')
        if parsed is not None:
            hover, others = parsed['hover'], parsed['others'] if parsed['others'] != ' ' else ''
            result.h(__base_rtext_convert(hover)[0])
        parsed = parse("({event} {contents}){others}", others)
        if parsed is not None and parsed['event'] in list(item.name for item in list(RAction)):
            event, content, others = RAction[parsed['event']], parsed['contents'], parsed['others']
            result.c(event, content)

    return result, others


def __base_rtext_convert(text: str) -> Tuple[Union[str, RText], str]:
    parsed, others = parse("[{msg}]{others}", text.strip() + ' '), ''
    if parsed is not None:
        msg, others = parsed["msg"], parsed["others"] if parsed["others"] != ' ' else ''
        color, styles = None, set()
        if msg.startswith("%"):
            while True:
                parameter: str = msg[:2]
                if parameter in COLORS.keys() and color is None:
                    color = RColor[COLORS[parameter]]
                    print(color)
                elif parameter in STYLES.keys():
                    styles.add(RStyle[STYLES[parameter]])
                else:
                    break
                msg = msg[2:]
        if len(styles) == 0:
            styles = None
        if msg.startswith(' '):
            msg = msg[1:]
        return RText(msg, color=color, styles=styles), others
    return text, others
