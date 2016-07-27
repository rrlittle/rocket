DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
# echo $DIR

OLDPATH=$PATH
PATH=bin;\
lib/ruby/gems/2.1.0/bin;\
lib/ruby/2.1.0;\
scripts;\
$OLDPATH
 
