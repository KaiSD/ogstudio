#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
НАСТРОЙКИ ТЕМЫ
"""
template = {
'Tiles':[
    'dots1',
    'dots2',
    'dots3',
    'dots4',
    'dots5',
    'dots6',
    'dots7',
    'dots8',
    'dots9',
    'dragons1',
    'dragons2',
    'dragons3',
    'winds1',
    'winds2',
    'winds3',
    'winds4',
    'bamboo1',
    'bamboo2',
    'bamboo3',
    'bamboo4',
    'bamboo5',
    'bamboo6',
    'bamboo7',
    'bamboo8',
    'bamboo9',
    'symbols1',
    'symbols2',
    'symbols3',
    'symbols4',
    'symbols5',
    'symbols6',
    'symbols7',
    'symbols8',
    'symbols9'
],
'TilesMultiple':[
    ('flowers1','flowers2','flowers3','flowers4'),
    ('seasons1','seasons2','seasons3','seasons4')
    ],
'Type':'dds',
'YouWin':'win',
'YouLose':'lose',
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