from parse import parse
from typing import Tuple, Optional, Union

try:
    # MCDReforged 1.0+
    from mcdreforged.api.rtext import RColor, RStyle, RText, RTextBase, RAction
except ImportError:
    try:
        # MCDReforged 0.8.1+
        from utils.rtext import RColor, RStyle, RText, RTextBase, RAction
    except ImportError:
        # MCDReforged 0.8.0
        try:
            from utils.stext import SColor, SStyle, SText, STextBase, SAction as RColor, RStyle, RText, RTextBase, \
                RAction
        except:
            # Even lower versions with stext (DO NOT support Python 2.x and MCDeamon)
            from plugins.stext import SColor, SStyle, SText, STextBase, SAction as RColor, RStyle, RText, RTextBase, \
                RAction

PLUGIN_METADATA = {
    "id": "powerful_rtext_api_legacy",
    "version": "0.1.0",
    "name": "Powerful RText API (Legacy)",
    "description": "An RText extension",
    "author": [
        "Ra1ny_Yuki"
    ],
    "link": "https://github.com/Lazy-Bing-Server/PowerfulRTextAPI"
}

COLORS = {
    '%0': 'black',
    '%1': 'dark_blue',
    '%2': 'dark_green',
    '%3': 'dark_aqua',
    '%4': 'dark_red',
    '%5': 'dark_purple',
    '%6': 'gold',
    '%7': 'gray',
    '%8': 'dark_gray',
    '%9': 'blue',
    '%a': 'green',
    '%b': 'aqua',
    '%c': 'red',
    '%d': 'light_purple',
    '%e': 'yellow',
    '%f': 'white',
    '%r': 'reset'
    }

STYLES = {
    '%k': 'obfuscated',
    '%l': 'bold',
    '%m': 'strikethrough',
    '%n': 'underlined',
    '%o': 'italic',
}


def text_to_rtext(text: str) -> Tuple[Optional[RTextBase], str]:
    """
    Transfer a text in following format to RText objects:
    [{style_marks} {msg}]<{hover_text}>({click_events}||{click_contents})
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
