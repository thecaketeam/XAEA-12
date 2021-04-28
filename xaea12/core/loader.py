import os
import ast
import importlib

import discord
from discord.ext import commands

class Loader:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def load_module(self, name):
        name = Loader.filename_to_module(name)
        try:
            self.bot.load_extension(name)
        except commands.ExtensionAlreadyLoaded as err:
            pass

    def unload_module(self, name):
        name = Loader.filename_to_module(name)
        try:
            self.bot.unload_extension(name)
        except commands.ExtensionNotLoaded as err:
            pass

    def reload_module(self, name):
        self.unload_module(name)
        self.load_module(name)

    @staticmethod
    def filename_to_module(filename):
        if filename.endswith('.py'):
            filename = filename.replace('.py', '')
            filename = filename.replace(os.sep, '.')
        if not 'cogs' in filename:
            filename = 'xaea12.cogs.{}'.format(filename)
        return filename

    @staticmethod
    def get_module_class(filename):
        with open(filename) as file:
            node = ast.parse(file.read())

        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        for _class in classes:
            bases = [base.attr == "Cog" for base in _class.bases]
            if True in bases:
                name = Loader.filename_to_module(filename)
                module = importlib.import_module(name)
                obj = getattr(module, _class.name)
                return obj

        return None

    @staticmethod
    def get_modules(path):
        files = [os.path.join(path, file) for file in os.listdir(path)]
        files = [file for file in files if file.endswith('.py')]
        return files
