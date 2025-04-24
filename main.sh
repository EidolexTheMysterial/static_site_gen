echo "\n[[ main.sh : executing src/main.py ]]\n\n"
python3 src/main.py

echo "\n\n[[ main.sh : starting web server in public/ ]]\n\n"
cd public && python3 -m http.server 8888
