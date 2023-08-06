from setuptools import setup


setup(name='qreport',
      version='0.2',
      description='Simple report',
      url='https://github.com/rvettori/qreport',
      author='Rafael Vettori',
      author_email='rafael.vettori@gmail.com',
      license='MIT',
      packages=['qreport'],
      install_requires=[
            'dataset',
            'qfilter',
            'jinja2',
      ],
      zip_safe=False,
)
