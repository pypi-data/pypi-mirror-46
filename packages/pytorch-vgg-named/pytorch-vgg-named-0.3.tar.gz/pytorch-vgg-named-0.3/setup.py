from setuptools import setup

setup(name='pytorch-vgg-named',
      version='0.3',
      url='http://github.com/black-puppydog/pytorch_vgg_named',
      author='Daan Wynen',
      author_email='daan.wynen@inria.fr',
      packages=['vgg_named'],
      description="Named VGG feature extraction",
      long_description="Provides a version of the popular VGG networks that can be used as feature extractors similar to how to query nodes in tensorflow. Useful for style transfer code, where you want to do stuff like r11, r31, r51 = net.forward(targets=['relu1_1', 'relu3_1', 'relu5_1']). Also provides simple way to load normalized weights as in Gatys et al.",
      long_description_content_type="text/markdown",
      python_requires='>=3.6',
      install_requires=[
        'torch>=1.0',
        'torchvision>=0.2',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
      ],
      )
