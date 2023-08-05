import setuptools

name = 'vmi'
version = '0.1.6'

with open('README.md', 'r', encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author='sjtu_6547',
    author_email='88172828@qq.com',
    description='可视医学创新 (Visual Medical Innovation)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/vmi/',
    keywords='PySide2 SimpleITK vtk pythonocc-core OpenCASCADE',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['PySide2>=5.12',
                      'SimpleITK>=1.2',
                      'vtk>=8.1',
                      'pydicom>=1.2',
                      'numpy'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
