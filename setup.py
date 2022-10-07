from distutils.core import setup
import py2exe


setup(name='PipeDiffuser',
     version='1.0.1',
     description='Design Pipe Diffuser for Centrifugal Compressor',
     author='Sergey Kokorev',
     author_email='skokorev1981@gmail.com',
     packages=['mathlib', 'nx', 'chart', 'utils', 'diffuser', 'nx']
     )
