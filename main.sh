

echo "\n[[ $0 : executing src/main.py ]]\n\n"
python3 src/main.py

echo "\n\n[[ $0: starting web server in docs/ ]]\n\n"
cd docs && python3 -m http.server 8888
