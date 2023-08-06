import os
import sys
import os.path

def j(*args):
    if not args: return
    todo = list(map(str, filter(None, args)))
    return os.path.join(*todo)

if sys.version_info.major < 3:
    print("you need to run koning with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

target = "koning"
upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir):
        print("%s does not exist" % dir)
        os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)

    return upl

setup(
    name='koning',
    version='37',
    url='https://bitbucket.org/bthate/koning',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Het betreft hier echter geen medicatie maar gif",
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj"],
    scripts=["bin/koning"],
    packages=['koning', ],
    long_description="""
         De Koning is op de hoogte (zie http://koning.rtfd.io) dat de medicijnen toegedient met behulp van de nog in te voeren wetten gif zijn en dus moet hij ook weten dat met het in werking laten treden van deze wetten hij zich schuldig maakt aan het opdracht geven tot het toedienen van gif.
         Natuurlijk dient er voor het volksbelang direct opgetreden te worden (zie http://president.rtfd.io) , mischien voor de opvolger van deze minister president die schuldig is aan straffeloosheids zekeringen (zie http://kamer.rtfd.io).
    """,
    data_files=[("docs", ["docs/conf.py","docs/index.rst"]),
               (j('docs', 'jpg'), uploadlist(os.path.join("docs","jpg"))),
               (j('docs', 'txt'), uploadlist(os.path.join("docs", "txt"))),
               (j('docs', '_templates'), uploadlist(os.path.join("docs", "_templates")))
              ],
    package_data={'': ["*.crt"],
                 },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
