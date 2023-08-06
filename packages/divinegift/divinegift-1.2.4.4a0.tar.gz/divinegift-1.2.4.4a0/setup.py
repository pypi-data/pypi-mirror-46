from setuptools import setup, find_packages 

with open('README.md') as f:
    long_description = f.read()

setup(name='divinegift',
      version='1.2.4.4a0',
      description='Functions create_json and create_yaml were reworked',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      classifiers=[
                   'Development Status :: 5 - Production/Stable',
                   #'Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3',
                   "Operating System :: OS Independent", 
                   ],
      keywords='s7_it',
      url='https://gitlab.com/gng-group/divinegift.git',
      author='Malanris',
      author_email='admin@malanris.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=['sqlalchemy', 'requests', 'mailer', 'xlutils', 'xlsxwriter', 
                        'transliterate', 'cryptography', 'openpyxl', 'pyyaml>=5.1'],
      include_package_data=True,
      zip_safe=False)
