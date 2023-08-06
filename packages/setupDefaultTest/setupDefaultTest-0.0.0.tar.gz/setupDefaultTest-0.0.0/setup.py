from setuptools import setup, find_packages

configFile=open('CONF.txt', 'r').read().splitlines()
parameters =['name','version', 'desc','longdesc', 'url', 'author','author_email', 'license', 'python_version', 'keywords']
conf ={}
for each in configFile:
    for param in parameters:
        if param in each:
            conf[param]=''.join(each.split(':')[1:]).strip()

# specify requirements of your package here 
REQUIREMENTS = [''] 
#CLASSIFIERS=['']

# calling the setup function  
setup(name=conf['name'], 
      version=conf['version'], 
      description='A log writer function for py based docker containers.', 
      long_description=conf['longdesc'],
      url=conf['url'],
      author=conf['author'], 
      author_email=conf['author_email'],
      license=conf['license'],
      packages=find_packages(exclude=['']), 
#      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      python_requires='~=3.6',
      keywords=conf['keywords']
      ) 

