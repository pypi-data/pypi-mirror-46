from setuptools import setup, Extension

import sys
import platform

if platform.system() != 'Darwin':
    print("The macos_display package can only be installed on macOS", file=sys.stderr)
    sys.exit(1)

setup(
    name='macos_display',
    author='rob@sixty-north.com',
    author_email="rob@sixty-north.com",
    description="Retrieve information about macOS displays",
    version='1.0',
    packages = ['macos_display'],
    ext_modules=[
        Extension(
            'macos_display.display',
            ['macos_display/display_module.c',
             'macos_display/display.c'],
            extra_link_args = [
                '-framework', 'IOKit',
                '-framework', 'CoreFoundation',
                '-framework', 'ApplicationServices'
            ]
        )
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: zlib/libpng License',
    ]
)
