from setuptools import setup

setup(
    name='typescript-protobuf',
    version='0.1',
    description='Generate d.ts files for JSON objects from protobuf specs',
    keywords='typescript proto',
    license='The MIT License (MIT)',
    author='Cyrille Corpet',
    author_email='cyrille@bayesimpact.org',
    py_modules=[],
    url='https://github.com/bayesimpact/json-ts-protobuf',
    download_url='https://github.com/bayesimpact/json-ts-protobuf/archive/v0.1.tar.gz',
    scripts=['src/protoc-gen-json-ts'],
)
