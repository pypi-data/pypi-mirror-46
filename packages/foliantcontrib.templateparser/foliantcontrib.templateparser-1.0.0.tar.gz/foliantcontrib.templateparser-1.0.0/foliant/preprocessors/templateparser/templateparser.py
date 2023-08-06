'''
Template parser preprocessor for Foliant.
'''

import pkgutil

import foliant.preprocessors.templateparser.engines
from . import engines
from importlib import import_module
from pathlib import Path, PosixPath
from foliant.preprocessors.base import BasePreprocessor
from foliant.utils import output

from foliant.preprocessors.utils.combined_options import (Options,
                                                          CombinedOptions,
                                                          validate_in,
                                                          yaml_to_dict_convertor)

OptionValue = int or float or bool or str


def get_engines():
    '''
    Get dictionary with available template engines.
    Key - engine name, value - engine class
    '''
    result = {}
    for importer, modname, ispkg in pkgutil.iter_modules(engines.__path__):
        module = import_module(f'foliant.preprocessors.templateparser.engines.{modname}')
        if hasattr(module, 'TemplateEngine'):
            result[modname] = module.TemplateEngine
    return result


def get_context(match, limit=150, full_tag=False):
    '''
    Get context of the match object.

    Returns a string with <limit> symbols before match, the match string and
    <limit> symbols after match.

    If full_tag == False, matched string is limited too: first <limit>/2
    symbols of match and last <limit>/2 symbols of match.
    '''

    source = match.string
    start = max(0, match.start() - limit)  # index of context start
    end = min(len(source), match.end() + limit)  # index of context end
    span = match.span()  # indeces of match (start, end)
    result = '...' if start != 0 else ''  # add ... at beginning if cropped
    if span[1] - span[0] > limit and not full_tag:  # if tag contents longer than limit
        bp1 = match.start() + limit // 2
        bp2 = match.end() - limit // 2
        result += f'{source[start:bp1]} <...> {source[bp2:end]}'
    else:
        result += source[start:end]
    if end != len(source):  # add ... at the end if cropped
        result += '...'
    return result


class Preprocessor(BasePreprocessor):
    defaults = {
        'engine_params': {}
    }
    engines = get_engines()
    tags = ('template', *engines.keys())
    tag_params = ('engine',
                  'context',
                  'engine_params')  # all other params will be redirected to template

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = self.logger.getChild('templateparser')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def process_templates(self, content_file: PosixPath or str) -> str:
        """
        Go through <content_file> and look for template tags.
        For each tag send the contents to the corresponging template engine
        along with parameters from tag and config, and <content_file> path.
        Replace the tag with output from the enginge.
        """
        def _sub(block) -> str:
            tag_options = Options(self.get_options(block.group('options')),
                                  validators={'engine': validate_in(self.engines.keys())},
                                  convertors={'context': yaml_to_dict_convertor,
                                              'engine_params': yaml_to_dict_convertor})
            options = CombinedOptions({'config': self.options,
                                       'tag': tag_options},
                                      priority='tag')

            tag = block.group('tag')
            if tag == 'template':  # if "template" tag is used — engine must be specified
                if 'engine' not in options:
                    ref = current_filename.relative_to(self.working_dir.absolute())
                    output(f'WARNING [{ref}]: Engine must be specified in the <template> tag. Skipping.',
                           quiet=self.quiet)
                    self.logger.warning(f'[{ref}] Engine not specified in the <template> tag, skipping. Context:'
                                        '\n' + get_context(block))
                    return block.string
                engine = self.engines[options['engine']]
            else:
                engine = self.engines[tag]
            # all unrecognized params are redirected to template engine params
            context = {p: options[p] for p in options if p not in self.tag_params}
            # add options from "context" param
            context.update(options.get('context', {}))

            template = engine(block.group('body'),
                              context,
                              options.get('engine_params', {}),
                              current_filename)
            return template.build()
        current_filename = Path(content_file).absolute()
        with open(content_file, encoding='utf8') as f:
            content = f.read()

        return self.pattern.sub(_sub, content)

    def apply(self):
        self.logger.info('Applying preprocessor')

        for markdown_file_path in self.working_dir.rglob('*.md'):
            processed = self.process_templates(markdown_file_path)

            with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                markdown_file.write(processed)

        self.logger.info('Preprocessor applied')
