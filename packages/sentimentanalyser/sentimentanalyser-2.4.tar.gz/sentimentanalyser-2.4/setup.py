from setuptools import setup, find_packages

setup(
      name='sentimentanalyser',
      version='2.4',
      description='Generic python library to perform sentiment analysis on any dataset, using different models',
      long_description='A generic package to help developers perform analysis on their datasets, powered by SVM and '
                       'Naive-Bayes models and to be followed by many more.',
      url='',
      author='Sanjay Pradeep,Jayanth Anantharapu, Aditya Kumar, Ashhadul Islam',
      author_email='sanjay.sndk@gmail.com, aditya00kumar@gmail.com, ashhadulislam@gmail.com',
      keywords='',
      license='MIT',
      packages=['sentimentanalyser'],
      install_requires=[
            "et-xmlfile",
            "jdcal",
            "nltk",
            "numpy",
            "openpyxl",
            "pandas",
            "psycopg2",
            "python-dateutil",
            "pytz",
            "scikit-learn",
            "scipy",
            "six",
            "whitenoise",
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False
)
