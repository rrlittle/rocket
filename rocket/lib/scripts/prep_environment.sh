cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. # move to lib
# echo $DIR

OLDPATH=$PATH
PATH=ruby_ship/bin;\
scripts;\
$OLDPATH

cd "$( dirname "${BASH_SOURCE[0]}" )"  # move to script location
 
