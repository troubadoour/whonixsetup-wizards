#!/usr/bin/python

import sys
import locale, yaml


DEFAULT_LANG = 'en'

class Translations():
    def __init__(self, section):
        try:
            # credits to nrgaway.
            language = DEFAULT_LANG
            language = locale.getdefaultlocale()[0].split('_')[0]
            if language:
                language = language
            self.translations = '/usr/share/whonix/whonix-shared-translations'
            stream = file(self.translations, 'r')
            data = yaml.load(stream)
            if data:
                self.section = data[section]
                self.language = self.section.get(language, DEFAULT_LANG)

        except (IOError):
            # TODO: add code here.
            pass
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            pass

    def getText(self, key):
        return self.language.get(key, None)

    def error(self):
        print 'errwtwertw'
        return
