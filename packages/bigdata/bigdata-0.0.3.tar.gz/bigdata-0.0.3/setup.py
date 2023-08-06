from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='bigdata',
      version='0.0.3',
      description='IPython magic for running Apache tools for Big Data',
      long_description='IPython magic for running Pig, Hive, Drill inside a Jupyter Notebook',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
      ],
      keywords='big-data database ipython jupyter hadoop pig hive drill',
      url='http://github.com/jdvelasq/ipython-big-data',
      author='Juan D. Velasquez',
      author_email='jdvelasq@unal.edu.co',
      license='MIT',
      packages=['bigdata'],
      include_package_data=True,
      zip_safe=False)
