from setuptools import setup, find_packages

import vk_text_parser

setup(
    name='vk_text_parser',
    version=vk_text_parser.__version__,
    author='Ruzzy Rullezz',
    author_email='ruslan@lemimi.ru',
    packages=find_packages(),
    package_dir={'vk_text_parser': 'vk_text_parser'},
    package_data={
        'vk_text_parser': [
            'drivers/linux/*',
            'drivers/mac/*'
        ]
    },
    install_requires=[
        'selenium',
    ],
)
