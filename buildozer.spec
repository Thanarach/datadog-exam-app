[app]
title = Datadog Exam Simulator
package.name = datadogexam
package.domain = org.ntt.thailand
source.dir = .
# รวมไฟล์ทุกประเภทที่คุณใช้
source.include_exts = py,png,json,ttf
version = 7.3

# สเปคเครื่องที่ต้องการ
requirements = python3,kivy==2.3.0,pillow
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# ไอคอนแอป (ถ้ามี)
#icon.filename = datadog.png
