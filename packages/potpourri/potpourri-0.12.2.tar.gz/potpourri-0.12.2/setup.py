from setuptools import setup
# from setuptools import setup, find_packages


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='potpourri',
    version='0.12.2',
    description='model zoo of different preconfigured algorithms',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='http://github.com/kmedian/potpourri',
    author='Ulf Hamster',
    author_email='554c46@gmail.com',
    license='MIT',
    packages=['seasalt', 'datasets', 'verto', 'potpourri'],
    # packages=find_packages(),
    install_requires=[
        'setuptools>=40.0.0',
        'nose>=1.3.7',
        'numpy>=1.15.3',
        'scipy>=1.1.0',
        'pandas>=0.23.4',
        'korr>=0.6.0',
        'scikit-learn>=0.20.0',
        'xgboost>=0.80',
        'catboost>=0.11.1',
        'lightgbm>=2.2.2',
        'sklearn-lvq>=1.1.0',
        'umap-learn>=0.3.7',
        'MulticoreTSNE>=0.0.1.1',
        'mlxtend>=0.14.0'],
    python_requires='>=3.6',
    zip_safe=False
)
