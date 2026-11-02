// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.15
import calamares.slideshow 1.0

Presentation {
    id: presentation
    property bool german: Qt.locale().name.indexOf("de") === 0
    property var headings: german
        ? ["Willkommen bei AikaOS", "Dein Desktop mit Aika", "Gleich bereit"]
        : ["Welcome to AikaOS", "Your desktop with Aika", "Nearly ready"]
    property var descriptions: german
        ? ["Dein KDE-Plasma-Desktop wird eingerichtet.",
           "Wallpaper, Symbole und Fastfetch bringen Aika auf deinen Desktop.",
           "Nach der Installation bleiben deine Dateien und Einstellungen gespeichert."]
        : ["Your KDE Plasma desktop is being prepared.",
           "Wallpapers, icons and Fastfetch bring Aika to your desktop.",
           "Your files and settings will be saved on the installed system."]

    function onActivate() { currentSlide = 0; german = Qt.locale().name.indexOf("de") === 0 }
    function onLeave() {}

    Rectangle { anchors.fill: parent; color: "#071424"; z: -1 }

    Timer {
        interval: 9000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Repeater {
        model: 3
        Slide {
            x: 0
            y: 0
            width: parent.width
            height: parent.height
            Rectangle { anchors.fill: parent; color: "#071424" }
            Image { anchors.fill: parent; source: "wallpaper.png"; fillMode: Image.PreserveAspectCrop }
            Rectangle { anchors.fill: parent; color: "#071424"; opacity: 0.37 }
            Rectangle {
                width: parent.width * 0.53
                height: parent.height
                gradient: Gradient {
                    GradientStop { position: 0; color: "#ed071424" }
                    GradientStop { position: 1; color: "#d9081b2e" }
                }
            }
            Column {
                anchors.left: parent.left
                anchors.leftMargin: 28
                anchors.verticalCenter: parent.verticalCenter
                width: parent.width * 0.43
                spacing: 17
                Text { text: "AikaOS"; color: "#72d4ff"; font.pixelSize: 20; font.bold: true }
                Text { width: parent.width; text: presentation.headings[index]; color: "white"; font.pixelSize: 28; font.bold: true; wrapMode: Text.WordWrap }
                Text { width: parent.width; text: presentation.descriptions[index]; color: "#deebfb"; font.pixelSize: 17; wrapMode: Text.WordWrap; lineHeight: 1.25 }
            }
        }
    }
}
