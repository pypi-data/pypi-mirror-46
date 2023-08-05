# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['parse_1c_build']

package_data = \
{'': ['*']}

install_requires = \
['cjk-commons>=3.3,<4.0', 'commons-1c>=3.1,<4.0']

entry_points = \
{'console_scripts': ['p1cb = parse_1c_build.__main__:run']}

setup_kwargs = {
    'name': 'parse-1c-build',
    'version': '5.8.0',
    'description': 'Parse and build utilities for 1C:Enterprise',
    'long_description': 'РЈС‚РёР»РёС‚Р° РґР»СЏ СЂР°Р·Р±РѕСЂРєРё Рё СЃР±РѕСЂРєРё *epf*-, *erf*-, *ert*- Рё *md*-С„Р°Р№Р»РѕРІ\n===\n\nР§С‚Рѕ РґРµР»Р°РµС‚\n---\n\nРџСЂРё СѓСЃС‚Р°РЅРѕРІРєРµ РїР°РєРµС‚Р° РІ РєР°С‚Р°Р»РѕРіРµ СЃРєСЂРёРїС‚РѕРІ РёРЅС‚РµСЂРїСЂРµС‚Р°С‚РѕСЂР° Python СЃРѕР·РґР°С‘С‚СЃСЏ РёСЃРїРѕР»РЅСЏРµРјС‹Р№ С„Р°Р№Р» *p1cb.exe*. Р•РіРѕ РјРѕР¶РЅРѕ \nР·Р°РїСѓСЃС‚РёС‚СЊ СЃ РєРѕРјР°РЅРґРѕР№ *parse* РґР»СЏ СЂР°Р·Р±РѕСЂРєРё *epf*- Рё *erf*-С„Р°Р№Р»РѕРІ СЃ РїРѕРјРѕС‰СЊСЋ [V8Reader][1] РёР»Рё V8Unpack, *ert*- Рё \n*md*-С„Р°Р№Р»РѕРІ СЃ РїРѕРјРѕС‰СЊСЋ [GComp][2], РёР»Рё СЃ РєРѕРјР°РЅРґРѕР№ *build* РґР»СЏ СЃР±РѕСЂРєРё *epf*- Рё *erf*-С„Р°Р№Р»РѕРІ СЃ РїРѕРјРѕС‰СЊСЋ V8Unpack, *ert*- Рё \n*md*-С„Р°Р№Р»РѕРІ СЃ РїРѕРјРѕС‰СЊСЋ [GComp][2].\n\nРџСѓС‚Рё Рє СЃРµСЂРІРёСЃРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅРѕР№ Р±Р°Р·Рµ, *V8Reader.epf*, *V8Unpack.exe* Рё GComp СѓРєР°Р·С‹РІР°СЋС‚СЃСЏ РІ С„Р°Р№Р»Рµ РЅР°СЃС‚СЂРѕРµРє \n*settings.yaml*, РєРѕС‚РѕСЂС‹Р№ СЃРЅР°С‡Р°Р»Р° РёС‰РµС‚СЃСЏ РІ С‚РµРєСѓС‰РµРј РєР°С‚Р°Р»РѕРіРµ, Р·Р°С‚РµРј РІ РєР°С‚Р°Р»РѕРіРµ РґР°РЅРЅС‹С… РїСЂРёР»РѕР¶РµРЅРёСЏ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ \n(РІ Windows 10 РєР°С‚Р°Р»РѕРі *C:\\Users\\\\<РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ>\\AppData\\Roaming\\util-1c\\parse-1c-build\\>*), Р° Р·Р°С‚РµРј РІ РѕР±С‰РµРј РєР°С‚Р°Р»РѕРіРµ \nРґР°РЅРЅС‹С… РїСЂРёР»РѕР¶РµРЅРёСЏ (РІ Windows 10 РєР°С‚Р°Р»РѕРі *C:\\ProgramData\\util-1c\\parse-1c-build\\>*). Р•СЃР»Рё РїСѓС‚СЊ Рє РїР»Р°С‚С„РѕСЂРјРµ \n1РЎ:РџСЂРµРґРїСЂРёСЏС‚РёРµ 8 РІ С„Р°Р№Р»Рµ РЅР°СЃС‚СЂРѕРµРє РЅРµ СѓРєР°Р·Р°РЅ, С‚Рѕ РѕРЅ РёС‰РµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё.\n\nРўСЂРµР±РѕРІР°РЅРёСЏ\n---\n\n- Windows\n- Python 3.7 Рё РІС‹С€Рµ. РљР°С‚Р°Р»РѕРіРё РёРЅС‚РµСЂРїСЂРµС‚Р°С‚РѕСЂР° Рё СЃРєСЂРёРїС‚РѕРІ Python РґРѕР»Р¶РЅС‹ Р±С‹С‚СЊ РїСЂРѕРїРёСЃР°РЅС‹ РІ РїРµСЂРµРјРµРЅРЅРѕР№ РѕРєСЂСѓР¶РµРЅРёСЏ Path\n- РџР»Р°С‚С„РѕСЂРјР° 1РЎ:РџСЂРµРґРїСЂРёСЏС‚РёРµ 8.3\n- РЎРµСЂРІРёСЃРЅР°СЏ РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅР°СЏ Р±Р°Р·Р° (РІ РєРѕС‚РѕСЂРѕР№ Р±СѓРґРµС‚ Р·Р°РїСѓСЃРєР°С‚СЊСЃСЏ *V8Reader.epf*)\n- [V8Reader][1]\n- V8Unpack\n- [GComp][2]\n\n[1]: https://github.com/xDrivenDevelopment/v8Reader\n[2]: http://1c.alterplast.ru/gcomp/\n',
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'url': 'https://github.com/Cujoko/parse-1c-build',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
