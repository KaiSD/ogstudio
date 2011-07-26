#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
НАСТРОЙКИ ТЕМЫ
"""
template = {
'Tiles':[
    'bsd1',
    'bsd2',
    'bsd3',
    'linux1',
    'linux2',
    'linux3',
    'linux4',
    'linux5',
    'linux6',
    'linux7',
    'linux8',
    'linux9',
    'linux10',
    'linux11',
    'linux12',
    'linux13',
    'linux14',
    'linux15',
    'linux16',
    'linux17',
    'linux18',
    'linux19',
    'linux20',
    'linux21',
    'linux22',
    'linux23',
    'linux24',
    'linux25',
    'linux26',
    'linux27',
    'linux28',
    'linux29',
    'linux30',
    'linux31'
],
'TilesMultiple':[
    ('buntu1','buntu2','buntu3','buntu4'),
    ('chars1','chars2','chars3','chars4')
    ],
'Type':'dds',
'YouWin':'msg_win',
'YouLose':'msg_loss',
'Scene':'background',
'Skybox':{
    'lighting':'off',
    'depth_write':'off',
    'texture':'cubescene',
    'tex_address_mode': 'clamp'
    },
}

"""
ГЕНЕРАЦИЯ.
ЗДЕСЬ НИЧЕГО УЖЕ НЕ НАСТРАИВАЕТСЯ.
"""
output = ''
counter = 1

print 'Generating Theme.material file:'

for i in template['Tiles']:
    filename = i+'.'+template['Type']
    print filename
    output += """material ThemeMaterials/Group%i/1
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture %s
            }
        }
    }
}
material ThemeMaterials/Group%i/2 : ThemeMaterials/Group%i/1
{
}
material ThemeMaterials/Group%i/3 : ThemeMaterials/Group%i/1
{
}
material ThemeMaterials/Group%i/4 : ThemeMaterials/Group%i/1
{
}

""" % (counter, filename, counter, counter, counter, counter, counter, counter)
    counter += 1

for i in template['TilesMultiple']:
    for k in i:
        print k+'.'+template['Type']
    output += """material ThemeMaterials/Group%i/1
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture %s
            }
        }
    }
}
material ThemeMaterials/Group%i/2
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture %s
            }
        }
    }
}
material ThemeMaterials/Group%i/3
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture %s
            }
        }
    }
}
material ThemeMaterials/Group%i/4
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture %s
            }
        }
    }
}

""" % (counter, i[0]+'.'+template['Type'], counter, i[1]+'.'+template['Type'],
counter, i[2]+'.'+template['Type'], counter, i[3]+'.'+template['Type'])
    counter += 1

for i in ('YouWin','YouLose','Scene'):
    if i in template:
        filename = template[i]+'.'+template['Type']
        print filename
        output += """material ThemeMaterials/%s
{
    technique
    {
        pass
        {
            texture_unit
            {
                texture %s
            }
        }
    }
}

""" % (i, filename)

if 'Skydome' in template:
    filename = template['Skydome']['texture']+'.'+template['Type']
    print filename
    output += """material ThemeMaterials/SkyDome
{
    technique
    {
        pass
        {
            lighting %s
            depth_write %s

            texture_unit
            {
                texture %s
                scroll_anim %s %s
            }
        }
    }
}


""" % (template['Skydome']['lighting'], template['Skydome']['depth_write'],
filename, template['Skydome']['scroll_anim'][0], template['Skydome']['scroll_anim'][1])

if 'Skybox' in template:
    filename = template['Skybox']['texture']+'.'+template['Type']
    print filename
    output += """material ThemeMaterials/SkyBox
{
    technique
    {
        pass
        {
            lighting %s
            depth_write %s

            texture_unit
            {
                cubic_texture %s separateUV
                tex_address_mode %s
            }
        }
    }
}


""" % (template['Skybox']['lighting'], template['Skybox']['depth_write'],
filename, template['Skybox']['tex_address_mode'])

f = open('Theme.material', 'w')
f.write(output)
f.close()