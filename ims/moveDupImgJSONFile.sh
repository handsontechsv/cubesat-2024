CURR_DIR=${PWD}
SOURCE_DIR=$CURR_DIR/pi
TARGET_DIR=$CURR_DIR/duplicate

for file in $TARGET_DIR/*.jpg
do 
    echo $file
    jpegoptim --size=50% -o $file --dest=$TARGET_DIR
    f="${file##*/}"
    basef="${f%.jpg}"
    metaf=$basef"_metadata.json"
    predictf=$basef".json"
    #echo $metaf
    if [ -f $SOURCE_DIR/$metaf ]; then
        echo "move metadata jsonfile $metaf"
        mv -f $SOURCE_DIR/$metaf  $TARGET_DIR
    fi
    if [ -f $SOURCE_DIR/$predictf ]; then
        echo "move predict jsonfile $predictf"
        mv -f $SOURCE_DIR/$predictf  $TARGET_DIR
    fi
done