from setuptools import setup


setup(name='qreport',
      version='0.1',
      description='Simple report',
      url='https://github.com/rvettori/qfilter',
      author='Rafael Vettori',
      author_email='rafael.vettori@gmail.com',
      license='MIT',
      packages=['qreport'],
      install_requires=[
            'records',
            'qfilter',
            'jinja2',
      ],
      zip_safe=False,
)
