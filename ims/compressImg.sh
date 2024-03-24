CURR_DIR=${PWD}
SOURCE_DIR=$CURR_DIR/pi
TARGET_DIR=$CURR_DIR/compressed

for file in $SOURCE_DIR/*.jpg
do 
    echo $file
    jpegoptim --size=50% -o $file --dest=$TARGET_DIR
    f="${file##*/}"
    basef="${f%.jpg}"
    metaf=$basef"_metadata.json"
    #echo $metaf
    if [ -f $SOURCE_DIR/$metaf ]; then
        echo "copy metadata jsonfile $metaf"
        cp -f $SOURCE_DIR/$metaf  $TARGET_DIR
    fi
done