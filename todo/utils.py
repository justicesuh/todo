from typing import Any

from todo.styles import Background, Foreground, Style


def format(text: str, bg: Any = None, fg: Any = None, style: Any = None, end: str =''):
    if bg is not None:
        text = bg + text + Background.RESET
    if fg is not None:
        text = fg + text + Foreground.RESET
    if style is not None:
        text = style + text + Style.RESET
    return text + end


def tabulate(data: list[list[Any]], headers: list[str] | None):
    column_widths = [max(len(str(item)) for item in col) for col in zip(*(data + [headers if headers else []]))]

    def format_row(row: list[Any]) -> str:
        return ' | '.join(f'{str(item):{column_widths[i]}}' for i, item in enumerate(row))
    
    table: list[str] = []
    if headers is not None:
        table.append(format_row(headers))
        table.append('-' * (sum(column_widths) + 3 * (len(headers) - 1)))

    for row in data:
        table.append(format_row(row))
    
    return '\n'.join(table)
