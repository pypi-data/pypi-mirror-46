from setuptools import setup


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()


setup(
    name='markdown2pdf3',
    version='0.2.1',
    url='https://github.com/panhaoyu/markdown2pdf',
    license='MIT',
    author='panhaoyu',
    author_email='haoyupan@aliyun.com',
    description='A tool converts Markdown file to PDF.',
    long_description=fread('README.rst'),
    packages=['markdown2pdf3'],
    zip_safe=False,
    platforms='any',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'md2pdf = markdown2pdf3:execute',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
