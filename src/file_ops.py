import re, os, shutil

from md_utils import (
    markdown_to_html_node,
)

from blocktype import (
    extract_title,
)


# globals
base_path = "/"

static_path = "./static"
content_path = "./content"
public_path = "./docs"

tmpl_file = "./template.html"


ignore_files = [ ".DS_Store" ]


rxHtmlPath = r'(href|src)="/'


def rmv_dir(path):
    print(f"\n[ removing dir: '{path}/' ]")

    shutil.rmtree(path)

def add_dir(path):
    print(f"\n[ adding dir: '{path}/' ]")

    os.mkdir(path)


def list_dir(path):
    if not os.path.isdir(path):
        print(f"[ path not found: '{path}/' ]\n")
        raise ValueError("invalid path")

    print(f"\n[ retrieving contents of: '{path}/' ]")

    return os.listdir(path)


def cpy_path(src_path, dest_path):
    if not os.path.exists(src_path):
        print(f"\n[ path does not exist: '{src_path}' ]")
        raise ValueError("invalid path")

    if os.path.isdir(src_path):
        if not os.path.isdir(dest_path):
            add_dir(dest_path)

        contents = list_dir(src_path)

        for f in contents:
            if f not in ignore_files:
                new_src_path = os.path.join(src_path, f)
                new_dest_path = os.path.join(dest_path, f)

                cpy_path(new_src_path, new_dest_path)

            else:
                print(f"\n[ ignoring file: '{f}' ]")

    else:
        print(f"\n[ copying '{src_path}' to '{dest_path}' ]")

        shutil.copyfile(src_path, dest_path)


def start_file_ops():
    print("\n\n*[ starting file ops ]*\n")

    print(f"\n[ checking for '{public_path}/' ]")

    public_exists = os.path.isdir(public_path)

    if public_exists:
        rmv_dir(public_path)

    else:
        print(f"[ '{public_path}/' does not exist ]\n")

    print(f"\n\n[ copying '{static_path}/*' to '{public_path}/*' ]:\n")

    cpy_path(static_path, public_path)


def get_contents(path):
    if not os.path.exists(path):
        print(f"[ path does not exist: '{path}' ]")
        raise ValueError("invalid path")

    file = open(path, "r")

    contents = file.read()

    file.close()

    return contents


def write_contents(path, contents):
    if os.path.exists(path):
        print(f"[ path already exists: '{path}' ]")
        raise ValueError("invalid path")

    file = open(path, "w")

    file.write(contents)

    file.close()


def repl_tag(tag, tag_contents, str):
    macro = f"{{{{ {tag} }}}}"

    return str.replace(macro, tag_contents)


def generate_page(from_path, template_path, dest_path):
    print(f"\n\n[ generating page from '{from_path}' to '{dest_path}' using '{template_path}' ]\n")

    md = get_contents(from_path)
    tmpl = get_contents(template_path)

    nodes = markdown_to_html_node(md)

    html = nodes.to_html()

    page_ttl = extract_title(md)

    print(f"[ page title: {page_ttl} ]")

    new_html = repl_tag("Title", page_ttl, tmpl)
    new_html = repl_tag("Content", html, new_html)

    new_html = re.sub(rxHtmlPath, rf'\1="{base_path}', new_html)

    # new_html = new_html.replace('href="/', f'href="{base_path}')
    # new_html = new_html.replace('src="/', f'src="{base_path}')

    # print(new_html)

    dest_dir = os.path.dirname(dest_path)

    if len(dest_dir) > 0:
        os.makedirs(dest_dir, exist_ok=True)

    write_contents(dest_path, new_html)


def gen_path(src_path):
    if not os.path.exists(src_path):
        print(f"[ path does not exist: '{src_path}' ]")
        raise ValueError("invalid path")

    dest_path = os.path.join(public_path, src_path)
    dest_path = dest_path.replace(content_path + "/", "")

    if os.path.isdir(src_path):
        if src_path != content_path and not os.path.isdir(dest_path):
            add_dir(dest_path)

        contents = list_dir(src_path)

        for f in contents:
            if f not in ignore_files:
                new_src_path = os.path.join(src_path, f)

                gen_path(new_src_path)

            else:
                print(f"[ ignoring file: '{f}' ]\n")

    elif src_path.endswith(".md"):
        dest_path = dest_path.replace(".md", ".html")

        # print(f"[ gen'ing '{src_path}' to '{dest_path}' ]")

        generate_page(src_path, tmpl_file, dest_path)

    else:
        print(f"\n[ skipping: {src_path} ]\n")


def start_gen_ops(out_path):
    global base_path

    if out_path != base_path:
        base_path = out_path

    print("\n\n*[ starting gen ops ]*\n")

    gen_path(content_path)


    # generate_page("content/index.md", "template.html", "public/index.html")

    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")

    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")

    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")

    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")

