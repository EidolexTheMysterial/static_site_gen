
cur_script=${0/#.\//}

public_dir="docs/"

# build static-site for localhost
echo "\n[[ $cur_script : executing src/main.py ]]\n\n"
python3 src/main.py

# if no error, start python web server
if [ $? -eq 0 ]; then

  echo "\n\n[[ $cur_script : starting web server in $public_dir ]]\n\n"
  cd $public_dir && python3 -m http.server 8888

else

  echo
  echo "[[ $cur_script : Error detected, exiting ]]"

fi
