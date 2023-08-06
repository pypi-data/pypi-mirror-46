PACKAGE_NAME='cfg2'
MODULE_NAME='cfg'
PACKAGE_AUTHOR='neze'
AUTHOR_EMAIL='neze@melix.org'
PACKAGE_URL='https://framagit.org/1ohmatr/sw/py/cfg2'

PACKAGE_DESCRIPTION='Python package generated from template https://framagit.org/1ohmatr/sw/py/template'

PACKAGE_CLASSIFIERS=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]

ENTRY_POINTS={
    'console_scripts': [],
}

if __name__=='__main__':
    import setuptools,sys,os.path
    try:
        from sphinx.setup_command import BuildDoc
        cmdclass = { 'doc': BuildDoc, 'cov': BuildDoc }
    except ImportError:
        cmdclass = {}
    vstring = None
    if os.path.exists('version.py'):
        try:
            import version
            vstring = version.vstring
            rstring = version.rstring
        except ImportError:
            pass
    if vstring is None:
        try:
            from importlib import import_module
            version = import_module('{}.__version__'.format(PACKAGE_NAME))
            rstring = version.VERSION
        except ImportError:
            rstring = 'unknown'
        vstring = rstring
    doc_opt = {
        'project': ('setup.py',PACKAGE_NAME),
        'version': ('setup.py',vstring),
        'release': ('setup.py',rstring),
        'source_dir': ('setup.py','docs'),
    }
    cov_opt = dict(doc_opt)
    cov_opt.update({
        'builder': ('setup.py','coverage'),
    })
    if len(sys.argv) < 2:
        dist = 'dist'
        wheel = '-'.join([
            PACKAGE_NAME.replace('-','_'),
            rstring,
            'py3','none','any']) + '.whl'
        print(os.path.join(dist,wheel))
        sdist = '-'.join([
            PACKAGE_NAME,
            rstring]) + '.tar.gz'
        print(os.path.join(dist,sdist))
    else:
        with open('README.rst','r') as f:
            long_description = f.read()
        with open('requirements.txt','r') as f:
            install_requires = list(
                                filter(lambda x: x,
                                map(lambda x: x.strip(),
                                    f.readlines()
                                )))
        setuptools.setup(
            name=PACKAGE_NAME,
            version=rstring,
            author=PACKAGE_AUTHOR,
            author_email=AUTHOR_EMAIL,
            description=PACKAGE_DESCRIPTION,
            long_description=long_description,
            long_description_content_type='text/x-rst',
            url=PACKAGE_URL,
            packages=setuptools.find_packages(),
            data_files=['requirements.txt','LICENSE.txt'],
            classifiers=PACKAGE_CLASSIFIERS,
            entry_points=ENTRY_POINTS,
            install_requires=install_requires,
            cmdclass=cmdclass,
            command_options={
                'doc': doc_opt,
                'cov': cov_opt,
            }
        )
