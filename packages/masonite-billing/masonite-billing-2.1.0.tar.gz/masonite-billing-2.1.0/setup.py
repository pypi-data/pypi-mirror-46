from setuptools import setup


setup(
    name="masonite-billing",
    version='2.1.0',
    packages=[
        'billing',
        'billing.commands',
        'billing.contracts',
        'billing.controllers',
        'billing.drivers',
        'billing.factories',
        'billing.models',
        'billing.snippets',
    ],
    install_requires=[
        'masonite',
        'cleo',
        'stripe',
    ],
    include_package_data=True,
)
