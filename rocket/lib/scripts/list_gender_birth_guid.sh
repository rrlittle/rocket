# HEADER - should be present for jsut about all scripts
cd "$( dirname "${BASH_SOURCE[0]}" )" # move to scripts
source prep_environment.sh # give this terminal access to dependencies
# END OF HEADER

ruby_ship.sh list_gender_birth_guid.rb %* # run the script to get  
