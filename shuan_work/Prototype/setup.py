from cx_Freeze import setup, Executable
import os
import game

datafiles = ['launcher.ui', 'stat/.keep']
for i in os.listdir('data'):
    if i.endswith('.png') or i.endswith('.wav') or i.endswith('.mp3'):
        datafiles.append('data/'+i)
modules = ['config.py']
for i in os.listdir('Modules'):
    if i.endswith('.pyc'):
        modules.append('Modules/'+i)
for i in os.listdir('Modules/Avatars'):
    if i.endswith('.pyc'):
        modules.append('Modules/Avatars/'+i)
for i in os.listdir('Modules/Guns'):
    if i.endswith('.pyc'):
        modules.append('Modules/Guns/'+i)
for i in os.listdir('Modules/Weapons'):
    if i.endswith('.pyc'):
        modules.append('Modules/Weapons/'+i)
for i in os.listdir('Modules/HeavyWeapons'):
    if i.endswith('.pyc'):
        modules.append('Modules/HeavyWeapons/'+i)
for i in os.listdir('Modules/Bullets'):
    if i.endswith('.pyc'):
        modules.append('Modules/Bullets/'+i)
for i in os.listdir('Modules/Enemies'):
    if i.endswith('.pyc'):
        modules.append('Modules/Enemies/'+i)
for i in os.listdir('Modules/EnemyWeapons'):
    if i.endswith('.pyc'):
        modules.append('Modules/EnemyWeapons/'+i)
for i in os.listdir('Modules/Effects'):
    if i.endswith('.pyc'):
        modules.append('Modules/Effects/'+i)
for i in os.listdir('Modules/Core'):
    if i.endswith('.pyc'):
        modules.append('Modules/Core/'+i)
include = datafiles+modules

setup(
        name = game.NAME,
        version = str(game.VERSION),
        description = game.DESC,
        options = {'build_exe':dict(
                                optimize = 0,
                                include_files = include
                                )},
        executables = [Executable(
                                  'launcher.py',
                                  targetName='ShuanPrototype.exe',
                                  excludes=['Modules', 'config'],
                                  copyDependentFiles=True
                                  )])