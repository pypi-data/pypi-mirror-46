# -*- coding: utf-8 -*-

"pyloco task setup script"

if __name__ == "__main__":

    from setuptools import setup, find_packages
    __taskname__ = "docx2text"

    setup(
        name="pyloco_task_"+__taskname__,
        version="0.1.2",
        packages=find_packages(),
        install_requires=['python-docx>=0.8.10', 'pyloco>=0.0.90'],
        entry_points = {"pyloco_tasks": ["{name} = pyloco_task_{name}:entry_task".format(name=__taskname__)]},
    )
