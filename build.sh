
repo_name="/static_site_gen/"

echo "\n[[ $0 : executing src/main.py with arg '$repo_name' for GH Pages deployment ]]\n\n"

python3 src/main.py $repo_name
