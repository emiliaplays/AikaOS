from pathlib import Path
import base64, json, shutil

p = Path(__file__).resolve().parent.parent
r = p / 'profile/airootfs'
a = p / 'assets/branding'

def put(name, value):
    f = r / name
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(value)

def copy(source, dest):
    f = r / dest
    f.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(a / source, f)

copy('aika-logo-v2.png', 'usr/share/pixmaps/aikaos-logo.png')
copy('aika-lockscreen.png', 'usr/share/backgrounds/aikaos/lockscreen.png')
copy('aika-desktop.png', 'usr/share/backgrounds/aikaos/desktop.png')
image = base64.b64encode((a / 'aika-logo-v2.png').read_bytes()).decode()
logo = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="256" height="256" viewBox="0 0 256 256"><image width="256" height="256" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{image}"/></svg>'
icons = r / 'usr/share/icons/Aika/scalable'
for group in ('apps', 'places', 'actions'):
    (icons / group).mkdir(parents=True, exist_ok=True)
put('usr/share/icons/Aika/index.theme', '[Icon Theme]\nName=Aika\nComment=AikaOS midnight and cyan icons\nInherits=breeze-dark,breeze,hicolor\nDirectories=scalable/apps,scalable/places,scalable/actions\n\n' + ''.join(f'[scalable/{g}]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext={c}\n\n' for g,c in [('apps','Applications'),('places','Places'),('actions','Actions')]))
for name in ('aikaos-logo', 'archlinux-logo', 'archlinux', 'arch-linux', 'distributor-logo', 'start-here', 'start-here-kde', 'kde', 'system-logo'):
    (icons / 'apps' / (name + '.svg')).write_text(logo)
for f in (r / 'usr/share/pixmaps').glob('archlinux-logo*.svg'):
    f.write_text(logo)
# Explicit aliases cover package-owned Arch logos when the overlay is applied.
for name in ('archlinux-logo.svg', 'archlinux-logo-text.svg', 'archlinux-logo-text-dark.svg'):
    put('usr/share/pixmaps/' + name, logo)
copy('aika-logo-v2.png', 'usr/share/pixmaps/archlinux-logo.png')

paths = {
 'folder': ('places', '<path d="M8 19h19l6 7h23v27H8z" fill="#102e4e"/><path d="M8 26h48v27H8z" fill="#174c73"/><path d="M24 34l-5-6v14c0 12 26 12 26 0V28l-5 6"/><path d="M26 42h1m10 0h1"/>'),
 'user-home': ('places', '<path d="M8 30L32 10l24 20v25H8z" fill="#123a5c"/><path d="M23 54V35h18v19"/><path d="M18 20l-2-9 9 4m14 0 9-4-2 9"/>'),
 'user-trash': ('places', '<path d="M17 22h30l-3 34H20z" fill="#123a5c"/><path d="M12 19h40M25 12h14M27 29v18m10-18v18"/>'),
 'utilities-terminal': ('apps', '<rect x="6" y="11" width="52" height="43" rx="8" fill="#071829"/><path d="M16 25l9 8-9 8m17 0h14M15 12l-2-7 11 7m17 0 11-7-2 7"/>'),
 'system-file-manager': ('apps', '<path d="M8 19h19l6 7h23v27H8z" fill="#174c73"/><path d="M24 35l-5-7v13c0 13 26 13 26 0V28l-5 7"/><path d="M27 42h1m8 0h1"/>'),
 'preferences-system': ('apps', '<path d="M21 20l-7-9v20c-5 23 41 23 36 0V11l-7 9" fill="#123a5c"/><circle cx="32" cy="35" r="10"/><path d="M32 21v5m0 18v5M18 35h5m18 0h5"/>'),
 'system-lock-screen': ('actions', '<rect x="15" y="27" width="34" height="28" rx="6" fill="#123a5c"/><path d="M22 27v-8c0-16 20-16 20 0v8M23 10l-7-6v15m25-9 7-6v15"/><circle cx="32" cy="39" r="3"/><path d="M32 42v6"/>')
}
for name,(group,body) in paths.items():
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><g stroke="#49cfff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">' + body + '</g></svg>'
    (icons / group / (name + '.svg')).write_text(svg)
for alias, original in [('konsole','utilities-terminal'),('org.kde.konsole','utilities-terminal'),('dolphin','system-file-manager'),('org.kde.dolphin','system-file-manager'),('systemsettings','preferences-system')]:
    shutil.copy2(icons/'apps'/f'{original}.svg', icons/'apps'/f'{alias}.svg')

config = r / 'home/aika/.config'
put('home/aika/.config/kdeglobals', '[General]\nColorScheme=BreezeDark\n[KDE]\nLookAndFeelPackage=org.kde.breezedark.desktop\n[Icons]\nTheme=Aika\n')
put('home/aika/.config/kscreenlockerrc', '[Daemon]\nAutolock=false\n[Greeter]\nWallpaperPlugin=org.kde.image\n[Greeter][Wallpaper][org.kde.image][General]\nImage=file:///usr/share/backgrounds/aikaos/lockscreen.png\nFillMode=2\n')
for splash in ('home/aika/.config/ksplashrc','etc/skel/.config/ksplashrc'):
    (r/splash).unlink(missing_ok=True)
put('home/aika/.face.icon', '')
copy('aika-logo-v2.png', 'home/aika/.face.icon')
put('usr/share/plasma/shells/org.kde.plasma.desktop/contents/updates/aikaos-wallpaper.js', '''var ds = desktops();
for (var i=0; i<ds.length; i++) { ds[i].wallpaperPlugin="org.kde.image"; ds[i].currentConfigGroup=["Wallpaper","org.kde.image","General"]; ds[i].writeConfig("Image", "file:///usr/share/backgrounds/aikaos/desktop.png"); }
var ps=panels();
for(var i=0;i<ps.length;i++){var ws=ps[i].widgets();for(var j=0;j<ws.length;j++){if(ws[j].type==="org.kde.plasma.kickoff"){ws[j].currentConfigGroup=["General"];ws[j].writeConfig("icon","aikaos-logo");}}}
''')
ascii_logo = r'''$1        /\                /\
       /  \______________/  \
      /                      \
     /    /|  /|   |\  |\    \
    |    / | / |   | \ | \    |
    |   |  |/  |___|  \|  |   |
    |   |   $2<>$1       $2<>$1   |   |
    |   |        ^        |   |
     \   \      ___      /   /
      \___\____________/___/
          /   /|  |\   \
         /___/ |__| \___\
                $2AikaOS$1
'''
put('usr/share/aikaos/fastfetch-logo.txt', ascii_logo)
ff = {'logo':{'type':'file','source':'/usr/share/aikaos/fastfetch-logo.txt','color':{'1':'cyan','2':'blue'}}, 'modules':['title','separator','os','host','kernel','uptime','packages','shell','display','de','wm','theme','icons','terminal','cpu','gpu','memory','disk','break','colors']}
put('etc/xdg/fastfetch/config.jsonc', json.dumps(ff, indent=2)+'\n')
put('home/aika/.config/fastfetch/config.jsonc', json.dumps(ff, indent=2)+'\n')
put('etc/skel/.config/fastfetch/config.jsonc', json.dumps(ff, indent=2)+'\n')
user_fastfetch=p/'assets/fastfetch'
if (user_fastfetch/'config.jsonc').exists():
    for name in ('config.jsonc','config-compact.jsonc','config-full.jsonc'):
        supplied=json.loads((user_fastfetch/name).read_text(encoding='utf-8-sig'))
        assert supplied['logo']['type']=='data-raw'
        assert all(isinstance(m,str) and m.lower()!='command' for m in supplied['modules'])
        for dest in ('home/aika/.config/fastfetch','etc/skel/.config/fastfetch','etc/xdg/fastfetch','usr/share/aikaos/fastfetch'):
            target=r/dest/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(user_fastfetch/name,target)
    for source in user_fastfetch.glob('*.txt'):
        target=r/'usr/share/aikaos/fastfetch'/source.name
        shutil.copy2(source,target)
    shutil.copy2(user_fastfetch/'aika.txt',r/'usr/share/aikaos/fastfetch-logo.txt')
for f in (r/'etc/os-release',r/'root/customize_airootfs.sh'):
    f.write_text(f.read_text().replace('LOGO=archlinux-logo','LOGO=aikaos-logo').replace('AikaOS 11"','AikaOS 11.1"').replace('VERSION_ID=11\n','VERSION_ID=11.1\n'))
packages = p/'profile/packages.x86_64'
packages.write_text('\n'.join(sorted(set(packages.read_text().split())|{'fastfetch'}))+'\n')
profiledef=p/'profile/profiledef.sh'
profiledef.write_text(profiledef.read_text().replace('iso_version="11.0"','iso_version="11.1"').replace('AikaOS 11 KDE','AikaOS 11.1 KDE'))
for item in ('kdeglobals','kscreenlockerrc'):
    copy_from = config/item
    target = r/'etc/skel/.config'/item
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(copy_from,target)
put('etc/sddm.conf.d/20-aika-theme.conf', '[Theme]\nCurrent=breeze\nFacesDir=/usr/share/sddm/faces\n')
copy('aika-logo-v2.png','usr/share/sddm/faces/aika.face.icon')
put('usr/share/sddm/themes/breeze/theme.conf.user', '[General]\nbackground=/usr/share/backgrounds/aikaos/lockscreen.png\nshowlogo=hidden\n')
print('Aika branding, icons, wallpaper, lockscreen and fastfetch profile ready')
