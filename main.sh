
public_dir="docs/"

# build static-site for localhost
echo "\n[[ $0 : executing src/main.py ]]\n\n"
python3 src/main.py

# if no error, start python web server
if [ $? -eq 0 ]; then

  echo "\n\n[[ $0: starting web server in $public_dir ]]\n\n"
  cd $public_dir && python3 -m http.server 8888

else

  echo
  echo "[[ $0 : Error detected, exiting ]]"

fi
