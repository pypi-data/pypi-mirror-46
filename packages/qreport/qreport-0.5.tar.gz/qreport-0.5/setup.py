from setuptools import setup


setup(name='qreport',
      version='0.5',
      description='Simple Report',
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
      package_data={'qreport': [
          'templates/index.html',
          'templates/_filter.html',
          'templates/_forms.html',
          'templates/_table.html',
          'templates/_title.html',
          'templates/_script.js',
      ]}
)
