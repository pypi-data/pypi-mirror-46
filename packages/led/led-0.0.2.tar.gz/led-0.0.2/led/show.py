import ast
from textwrap import TextWrapper

from led import core

OUTPUT_WIDTH = 120
ITEM_KEY_WIDTH = 20
NUMBER_PREFIX_SIZE = 7
TAB_SIZE = 4
DEFAULT_INDENT = (TAB_SIZE ^ 3)


def _show_config(args):
    header = '  LED Config'
    data = vars(core.config)
    _show_result(header, data, args)


def _show_status(args):
    header = 'Reverse Proxy Status'
    data = core._get_sources()
    _show_result(header, data, args)


def _show_result(header, data, args):
    global DEFAULT_INDENT
    if args.count:
        DEFAULT_INDENT += NUMBER_PREFIX_SIZE
    if isinstance(data, dict):
        record_enum, format_record = _format_dict(data)
    else:
        record_enum = enumerate(iter(data), start=1)
        format_record = _format_kv

    # HEADER
    _print_header(header)

    # BODY
    i, records = _format_records(args, record_enum, format_record)
    _print_records(records)

    # FOOTER
    _print_footer(i, args)


def _format_dict(data):
    record_enum = enumerate(sorted(data.items()), start=1)
    format_record = _format_kv

    return record_enum, format_record


def _print_header(header):
    header = '\n' + header
    header += f'\n{"=" * OUTPUT_WIDTH}\n'
    print(header)


def _format_records(args, record_enum, format_record):
    records = []
    for i, item in record_enum:
        if i <= args.limit:
            count_string = _get_count_string(i, args)
            item_string = format_record(args, item)
            item_string = count_string + item_string
            records.append(item_string)
        else:
            i -= 1
            break

    return i, records


def _print_records(records):
    for record in records:
        _print_record(record)


def _print_record(record):
    wrapper = TextWrapper(
        width=OUTPUT_WIDTH,
        tabsize=TAB_SIZE,
        subsequent_indent=' ' * DEFAULT_INDENT
    )
    if '|' in record:
        k, v = record.split('|')
        k = wrapper.fill(f'\t{k}')
        print(k)
        v = v.strip()
        v = ast.literal_eval(v)
        for i, record in enumerate(v):
            record.strip()
            record = wrapper.fill(f'\t{record}')
            print(f"\t{record}")
        print("\n")
    else:
        record = wrapper.fill(f'\t{record}')
        print(record)


def _print_footer(i, args):
    if args.total:
        footer = f'\n{"-" * OUTPUT_WIDTH}'
        footer += f'\nTotal: {i}'
        print(footer)
    print('\n')


def _format_kv(args, item):
        k, v = item
        if isinstance(v, dict):
            record_enum, format_record = _format_dict(v)
            i, v = _format_records(args, record_enum, format_record)
            item_string = f"{k:>{ITEM_KEY_WIDTH}}:|{v}"
        else:
            item_string = f"{k:>{ITEM_KEY_WIDTH}}:\t{v}"

        return item_string


def _format_string(args, item):
    item_string = f'{item}'

    return item_string


def _get_count_string(i, args):
    if args.count:
        count_string = (f'{i:>{NUMBER_PREFIX_SIZE}}.  ')
    else:
        count_string = ''

    return count_string
