from distutils.core import setup

setup(
    name='p3sigma',
    version='0.0.10',
    packages=['p3sigma', 'p3sigma.eda', 'p3sigma.eval', 'p3sigma.other', 'p3sigma.outlier', 'p3sigma.visuals',
              'p3sigma.features', 'p3sigma.imbalance', 'p3sigma.clustering', 'p3sigma.preprocess', 'p3sigma.regression',
              'p3sigma.forecasting', 'p3sigma.classification', 'p3sigma.neural_networks'],
    url='',
    license='MIT',
    author='cemkarabulut',
    author_email='',
    download_url='https://github.com/cemkarabulut/p3sigma/archive/v0.0.0.tar.gz',
    description='',
    install_requires=[
          'numpy',
          'pandas',
          'statsmodels'
      ],
)
