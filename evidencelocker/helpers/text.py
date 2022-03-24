import bleach
from bleach.linkifier import LinkifyFilter
from functools import partial
import mistletoe
import werkzeug.security

_allowed_tags = [
    'a',
    'b',
    'blockquote',
    'br',
    'code',
    'del',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'i',
    'li',
    'ol',
    'p',
    'pre',
    'span',
    'strong',
    'sub',
    'sup',
    'table',
    'tbody',
    'th',
    'thead',
    'td',
    'tr',
    'ul'
    ]

_allowed_attributes = {
    'a': ['href', 'target'],
    'i': [],
    'span': ['style', 'class', 'data-toggle', 'title'],
    }

_allowed_protocols = [
    'http', 
    'https'
    ]

_allowed_styles =[
    'color'
]

def a_modify(attrs, new=False):

    #callback function that adds target=_blank
    attrs[(None, "target")] = "_blank"

    return attrs

cleaner=bleach.Cleaner(
    tags=_allowed_tags,
    attributes=_allowed_attributes,
    protocols=_allowed_protocols,
    filters=[
        partial(
            LinkifyFilter,
            skip_tags=["pre"],
            parse_email=False,
            callbacks=[a_modify]
            )
        ]
    )


def raw_to_html(text):

    text=text.replace('\r','') #compensate for windows being silly

    return cleaner.clean(mistletoe.markdown(text))
