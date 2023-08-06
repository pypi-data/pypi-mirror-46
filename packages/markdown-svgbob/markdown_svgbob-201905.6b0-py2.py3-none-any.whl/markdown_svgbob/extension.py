# -*- coding: utf-8 -*-
# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import json
import base64
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import typing as typ
str = getattr(builtins, 'unicode', str)
try:
    try:
        from urllib.parse import quote
    except ImportError:
        from urlparse import quote
except ImportError:
    from urllib import quote
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
import markdown_svgbob.wrapper as wrapper
TagType = str


def svg2html(svg_data, tag_type='inline_svg'):
    svg_data = svg_data.replace(b'\n', b'')
    if tag_type == 'img_base64_svg':
        img_b64_data = base64.standard_b64encode(svg_data)
        img_text = img_b64_data.decode('ascii')
        return '<img src="data:image/svg+xml;base64,{0}"/>'.format(img_text)
    elif tag_type == 'img_utf8_svg':
        img_text = svg_data.decode('utf-8')
        img_text = quote(img_text)
        return '<img src="data:image/svg+xml;utf-8,{0}"/>'.format(img_text)
    elif tag_type == 'inline_svg':
        return svg_data.decode('utf-8')
    else:
        err_msg = "Invalid tag_type='{0}'".format(tag_type)
        raise NotImplementedError(err_msg)


def _clean_block_text(block_text):
    if block_text.startswith('```bob'):
        block_text = block_text[len('```bob'):]
    elif block_text.startswith('~~~bob'):
        block_text = block_text[len('~~~bob'):]
    if block_text.endswith('```'):
        block_text = block_text[:-len('```')]
    elif block_text.endswith('~~~'):
        block_text = block_text[:-len('~~~')]
    return block_text


def draw_bob(block_text, default_options=None):
    options = {}
    if default_options:
        options.update(default_options)
    block_text = _clean_block_text(block_text)
    header, rest = block_text.split('\n', 1)
    if '{' in header and '}' in header:
        options.update(json.loads(header))
        block_text = rest
    tag_type = typ.cast(str, options.pop('tag_type', 'inline_svg'))
    svg_data = wrapper.text2svg(block_text, options)
    return svg2html(svg_data, tag_type=tag_type)


class SvgbobExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {'tag_type': ['inline_svg',
            'Format to use (inline_svg|img_utf8_svg|img_base64_svg)']}
        for name, options_text in wrapper.parse_options().items():
            self.config[name] = ['', options_text]
        self.images = {}
        super(SvgbobExtension, self).__init__(**kwargs)

    def reset(self):
        self.images.clear()

    def extendMarkdown(self, md, *args, **kwargs):
        preproc = SvgbobPreprocessor(md, self)
        md.preprocessors.register(preproc, name='svgbob_fenced_code_block',
            priority=50)
        postproc = SvgbobPostprocessor(md, self)
        md.postprocessors.register(postproc, name=
            'svgbob_fenced_code_block', priority=0)
        md.registerExtension(self)


class SvgbobPreprocessor(Preprocessor):
    RE = re.compile('^(```|~~~)bob')

    def __init__(self, md, ext):
        super(SvgbobPreprocessor, self).__init__(md)
        self.ext = ext

    def run(self, lines):
        is_in_fence = False
        out_lines = []
        block_lines = []
        default_options = {'tag_type': self.ext.getConfig('tag_type',
            'inline_svg')}
        for name in self.ext.config.keys():
            val = self.ext.getConfig(name, '')
            if val != '':
                default_options[name] = val
        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if not ('```' in line or '~~~' in line):
                    continue
                is_in_fence = False
                block_text = '\n'.join(block_lines)
                del block_lines[:]
                img_tag = draw_bob(block_text, default_options)
                img_id = id(img_tag)
                marker = "<p id='svgbob{0}'>svgbob{1}</p>".format(img_id,
                    img_id)
                tag_text = '<p>{0}</p>'.format(img_tag)
                out_lines.append(marker)
                self.ext.images[marker] = tag_text
            elif self.RE.match(line):
                is_in_fence = True
                block_lines.append(line)
            else:
                out_lines.append(line)
        return out_lines


class SvgbobPostprocessor(Postprocessor):

    def __init__(self, md, ext):
        super(SvgbobPostprocessor, self).__init__(md)
        self.ext = ext

    def run(self, text):
        for marker, img in self.ext.images.items():
            wrapped_marker = '<p>' + marker + '</p>'
            if wrapped_marker in text:
                text = text.replace(wrapped_marker, img)
            elif marker in text:
                text = text.replace(marker, img)
        return text
