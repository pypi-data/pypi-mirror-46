from distutils.core import setup

setup(name='ybc_art',
      version='1.0.11',
      description='text to art chars',
      long_description='trans the text to art text',
      author='zhangyun',
      author_email='zhangyun@fenbi.com',
      keywords=['pip3', 'arttext', 'python3','python','art'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_art'],
      package_data={'ybc_art': ['*.py']},
      license='MIT',
      install_requires=['ybc_exception'],
)
