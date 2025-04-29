
cur_script=${0/#.\//}

repo_name="/static_site_gen/"

echo "\n[[ $cur_script : executing src/main.py with arg '$repo_name' for GH Pages deployment ]]\n\n"

python3 src/main.py $repo_name
