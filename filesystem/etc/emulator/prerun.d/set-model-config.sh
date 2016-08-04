if [ ! -z $1 ]; then
        NEW_ROOT=$1
else
        NEW_ROOT=
fi


CMDLINE=/proc/cmdline
XML=$NEW_ROOT/etc/config/model-config.xml

echo -e "*** Setting model-config.xml"

if [ ! -f $XML ] ; then
    echo -e "- model-config.xml does not exist"
    exit
fi

# display resolution
if grep -q "video=" $CMDLINE ; then
        VIDEO=`sed s/.*video=// $CMDLINE | cut -d ' ' -f1`
        FORMAT=`echo $VIDEO | cut -d ':' -f2 | cut -d ',' -f2`
        RESOLUTION=`echo $FORMAT | cut -d '-' -f1`
        WIDTH=`echo $RESOLUTION | cut -d 'x' -f1`
        HEIGHT=`echo $RESOLUTION | cut -d 'x' -f2`

        TR_NUM=`echo $WIDTH$HEIGHT | tr -d '[0-9]'`
        if [ "$TR_NUM" != "" ] ; then
            echo -e "- resolution value is non-integer argument"
        else
            WIDTH_KEY="tizen.org\/feature\/screen.width\" type=\"int\""
            WIDTH_KEY_NAME="tizen.org/feature/screen.width"
            sed -i s/"$WIDTH_KEY".*\</"$WIDTH_KEY"\>"$WIDTH"\</ $XML
            ${NEW_ROOT}/usr/bin/system_info_update_db -r ${NEW_ROOT} -k ${WIDTH_KEY_NAME} -t int -g platform -v ${WIDTH}
            HEIGHT_KEY="tizen.org\/feature\/screen.height\" type=\"int\""
            HEIGHT_KEY_NAME="tizen.org/feature/screen.height"
            sed -i s/"$HEIGHT_KEY".*\</"$HEIGHT_KEY"\>"$HEIGHT"\</ $XML
            ${NEW_ROOT}/usr/bin/system_info_update_db -r ${NEW_ROOT} -k ${HEIGHT_KEY_NAME} -t int -g platform -v ${HEIGHT}
            echo -e "- width=$WIDTH, height=$HEIGHT"

            # screen size
            SCREENSIZE_KEY="tizen.org\/feature\/screen.size"
            SCREENSIZE_KEY_NORMAL=""$SCREENSIZE_KEY".normal"
            SCREENSIZE_KEY_NORMAL_RESOLUTION=""$SCREENSIZE_KEY_NORMAL"."$WIDTH"."$HEIGHT"\" type=\"bool\""
            SCREENSIZE_KEY_NORMAL_NAME="tizen.org/feature/screen.size.normal"

            sed -i s/"$SCREENSIZE_KEY_NORMAL".[0-9].*"type=\"bool\"".*true/"&!!!"/ $XML
            TMP_RESOLUTION=`grep "true!!!" $XML | sed s/.*normal\.// | cut -d '"' -f1`
            ${NEW_ROOT}/usr/bin/system_info_update_db -r ${NEW_ROOT} -k ${SCREENSIZE_KEY_NORMAL_NAME}.${TMP_RESOLUTION} -t bool -g platform -v false
            sed -i s/true!!!/false/ $XML
            sed -i s/"$SCREENSIZE_KEY_NORMAL_RESOLUTION".*\</"$SCREENSIZE_KEY_NORMAL_RESOLUTION"\>true\</ $XML
            ${NEW_ROOT}/usr/bin/system_info_update_db -r ${NEW_ROOT} -k ${SCREENSIZE_KEY_NORMAL_NAME}.${WIDTH}.${HEIGHT} -t bool -g platform -v true
        fi
fi

# dot per inch
if grep -q "dpi=" $CMDLINE ; then
        DPI=`sed s/.*dpi=// $CMDLINE | cut -d ' ' -f1`

        TR_NUM=`echo $DPI | tr -d '[0-9]'`
        if [ "$TR_NUM" != "" ] ; then
            echo -e "- dpi value is non-integer argument"
        else
            #temp
            if [ "$DPI" -gt "999" ] ; then
                SCREEN_DPI=`expr "$DPI" "/" 10`
            else
                SCREEN_DPI="$DPI"
            fi

            DPI_KEY="tizen.org\/feature\/screen.dpi\" type=\"int\""
            DPI_KEY_NAME="tizen.org/feature/screen.dpi"
            sed -i s/"$DPI_KEY".*\</"$DPI_KEY"\>"$SCREEN_DPI"\</ $XML
            ${NEW_ROOT}/usr/bin/system_info_update_db -r ${NEW_ROOT} -k ${DPI_KEY_NAME} -t int -g platform -v ${SCREEN_DPI}
            echo -e "- dpi=$SCREEN_DPI"
        fi
fi

