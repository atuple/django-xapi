from setuptools import setup, find_packages

readme = 'README.md'

with open(readme, 'rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='xapi',
    version='0.1.0',
    author='sai',
    author_email='3030159@qq.com',
    url='https://github.com/atuple/xapi',
    keywords='django, rest, api',
    description=u'django-xapi',
    license='MIT',
    include_package_data=True,
    packages=["xapi", "xapi.views"],
    package_data={'xapi': ['static/xapi/css/*.css', 'static/xapi/js/*.js', 'static/xapi/fonts/*', 'templates/*.html']},
    zip_safe=False,
    install_requires=[
        "django >= 1.11.0",
        "markdown"
    ]
)
