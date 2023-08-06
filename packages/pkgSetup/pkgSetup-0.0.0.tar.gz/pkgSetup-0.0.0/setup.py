from setuptools import setup, find_packages

configFile=open('CONF.txt', 'r').read().splitlines()
parameters =['name','version', 'description','long_description', 'url', 'author','author_email', 'license', 'install_requires', 'python_requires', 'keywords']

conf ={}
for each in configFile:
    for param in parameters:
        if param in each:
            conf[param]=''.join(each.split(':')[1:]).strip()
conf['packages']=find_packages(exclude=[''])
# specify requirements of your package here 
REQUIREMENTS = [''] 
#CLASSIFIERS=['']

confArr= []
for each in conf:
    confArr.append(str(each)+'='+str(conf[each]))
confStr = ', '.join(confArr)

setup(**conf)

# calling the setup function  
#setup(name=conf['name'], 
#      version=conf['version'], 
#      description=conf['desc'],
#      long_description=conf['longdesc'],
#      url=conf['url'],
#      author=conf['author'], 
#      author_email=conf['author_email'],
#      license=conf['license'],
#      packages=find_packages(exclude=['']), 
#      classifiers=CLASSIFIERS, 
#      install_requires=conf['requirements'], 
#      python_requires=conf['python_requires'],
#      keywords=conf['keywords']
#      ) 

