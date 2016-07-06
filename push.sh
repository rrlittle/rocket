print_doc(){
	echo  "this is used to commit all the current files and push them to the remote.";
	echo "do not use this for anything complex";
	echo "usage: ./pull.sh {message}";
}

git add -A
git commit -m "$*" || (print_doc && exit 1)
git push