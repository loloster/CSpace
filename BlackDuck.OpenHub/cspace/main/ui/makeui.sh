#/bin/sh
for F in *.ui
 do
  echo $F "Ui_"$(basename $F ".ui")".py"
  pyuic4 $F -o "Ui_"$(basename $F ".ui")".py"
 done
pyrcc4 images.qrc -o images_rc.py
