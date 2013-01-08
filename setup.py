from setuptools import setup, find_packages

setup(
    name = 'fedora-business-cards',
    version = '1.beta1',
    packages = find_packages(),

    author = 'Ian Weller',
    author_email = 'iweller@redhat.com',
    url = 'https://fedoraproject.org/wiki/Business_cards',

    entry_points = {
        'console_scripts': [
            ('fedora-business-cards = '
             'fedora_business_cards.frontend.cmdline:main'),
        ],
    },
)
