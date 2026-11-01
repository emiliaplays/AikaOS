var ds = desktops();
for (var i=0; i<ds.length; i++) { ds[i].wallpaperPlugin="org.kde.image"; ds[i].currentConfigGroup=["Wallpaper","org.kde.image","General"]; ds[i].writeConfig("Image", "file:///usr/share/backgrounds/aikaos/desktop.png"); }
var ps=panels();
for(var i=0;i<ps.length;i++){var ws=ps[i].widgets();for(var j=0;j<ws.length;j++){if(ws[j].type==="org.kde.plasma.kickoff"){ws[j].currentConfigGroup=["General"];ws[j].writeConfig("icon","aikaos-logo");}}}
