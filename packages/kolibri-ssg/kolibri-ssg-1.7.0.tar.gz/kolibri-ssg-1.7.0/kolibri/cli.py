
import os
import sys
import time
import click
import pkg_resources
from livereload import Server, shell
from . import Kolibri
from .kolibri import PAGE_FORMAT
from .__about__ import *

CWD = os.getcwd()


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    

TPL_HEADER = """
---
title: Page Title
description: Page Description
meta:
    key: value
---

"""

TPL_BODY = {
    # HTML

    "html": """
<template>
    <div>
        <h1>{{ page.title }}</h1>
    </div>
</template>

<script>

</script>

<style>

</style>
""",

    # MD
    "md": """

# My markdown Kolibri!

"""

}


def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    package_name = "kolibri"
    dest = (dest + "/" + os.path.basename(src)).rstrip("/")
    if pkg_resources.resource_isdir(package_name, src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + "/" + res, dest)
    else:
        if not os.path.isfile(dest) \
                and os.path.splitext(src)[1] not in [".pyc"]:
            with open(dest, "wb") as f:
                f.write(pkg_resources.resource_string(__name__, src))
        else:
            print("File exists: %s " % dest)


def stamp_kolibri_current_version(dir):
    f = os.path.join(dir, "kolibri.yml")
    if os.path.isfile(f):
        with open(f, "r+") as file:
            content = file.read()
            content = content.replace("##VERSION##", __version__)
            file.seek(0)
            file.write(content)
            file.truncate()


def title(txt):
    message = "%s" % txt
    print(color.BOLD + message + color.END)


def footer():
    print("-" * 80)

def done():
    info('DONE!')
    footer()

def error(message):
    print(color.BOLD + color.RED + "::ERROR::" + color.END)
    print(color.RED + message + color.END )

def error_exit(message):
    error(message)
    footer()
    exit()

def info(message):
    print(color.DARKCYAN + message + color.END )

def log(message): 
    print(message)

@click.group()
def cli():
    """
    Kolibri: An elegant static site generator
    """
    pass


@cli.command("version")
def version():
    """Return the vesion of Kolibri"""
    print(__version__)
    footer()


@cli.command("create")
@click.argument("sitename")
def create_site(sitename):
    """Create a new site directory and init Kolibri"""
    title('Create new site')
    kolibri_conf = os.path.join(CWD, "kolibri.yml")
    if os.path.isfile(kolibri_conf):
        error_exit("Can't create new site in a directory that contain 'kolibri.yml'")
    
    sitepath = os.path.join(CWD, sitename)
    if os.path.isdir(sitepath):
        error_exit("Site directory '%s' exists already!" % sitename)
    else:
        info("Creating site: %s..." % sitename)
        os.makedirs(sitepath)
        copy_resource("skel/", sitepath)
        stamp_kolibri_current_version(sitepath)
        info("Site created successfully!")
        info("CD into '%s' and run 'kolibri serve' to view the site" % sitename)

    done()


@cli.command("init")
def init():
    """Initialize Kolibri in the current directory """
    title("Init Kolibri...")
    kolibri_conf = os.path.join(CWD, "kolibri.yml")
    if os.path.isfile(kolibri_conf):
        error_exit("Kolibri already initialized in '%s'. Or delete 'kolibri.yml' if a mistake " % CWD)
    else:
        copy_resource("skel/", CWD)
        stamp_kolibri_current_version(CWD)
        info("Kolibri init successfully!")
        info("Run 'kolibri serve' to view the site")
    done()


@cli.command("page")
@click.argument("pagenames", nargs=-1)
def create_page(pagenames):
    """Create new pages"""
    K = Kolibri(CWD)
    defaultExt = "html"
    pages = []
    title("Creating new pages...")

    # Prepare and check the files
    for pagename in pagenames:
        page = pagename.lstrip("/").rstrip("/")
        _, _ext = os.path.splitext(pagename)

        # If the file doesn't have an extension, we'll just create one
        if not _ext or _ext == "":
            page += ".%s" % defaultExt

        # Destination file
        dest_file = os.path.join(K.pages_dir, page)
        if not page.endswith(PAGE_FORMAT):
            error_exit("Invalid file format: '%s'. Only '%s'" %
                       (page, " ".join(PAGE_FORMAT)))
        elif os.path.isfile(dest_file):
            error_exit("File exists already: '%s'" % dest_file)
        else:
            pages.append((page, dest_file))

    for page, dest_file in pages:
        # Making sure dir is created
        dest_dir = os.path.dirname(dest_file)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        markup = os.path.splitext(page)[1].strip('.')
        content = TPL_HEADER
        content += TPL_BODY[markup]
        with open(dest_file, "w") as f:
            f.write(content)
        log("- %s" % page)
    done()


@cli.command("build")
@click.option("-i", "--info", is_flag=True)
@click.option("--env", default=None)
def build(info, env):
    """Build the site"""
    title("Building site...")
    K = Kolibri(CWD, {"env": env, "build": "build"})
    log('Env: %s' % K.site_env)
    log('Base Url: %s' % K.base_url)
    log('Static Url: %s' % K.static_url)    
    K.build(print_info=info)
    done()

@cli.command()
@click.option("-p", "--port", default=None)
@click.option("--no-livereload", default=None)
@click.option("--open-url", default=None)
@click.option("--env", default=None)
def serve(port, no_livereload, open_url, env):
    """Serve the site """
    
    K = Kolibri(CWD, {"env": env, "build": "serve"})
    if not port:
        port = K.config.get("serve.port", 8000)
    if no_livereload is None:
        no_livereload = True if K.config.get(
            "serve.livereload") is False else False
    if open_url is None:
        open_url = False if K.config.get(
            "serve.open_url") is False else True
    title('Serving on port %s' % port)
    log('Env: %s' % K.site_env)
    log('Base Url: %s' % K.base_url)
    log('Static Url: %s' % K.static_url)
    log("Livereload: %s" % ("OFF" if no_livereload else "ON"))

    def build_static():
        K.build_static()

    def build_pages():
        K.build_pages()

    K.build()

    server = Server()
    if no_livereload is False:
        server.watch(K.static_dir + "/", build_static)
        for c in [K.pages_dir, K.templates_dir, K.content_dir, K.data_dir]:
            server.watch(c + "/", build_pages)

    server.serve(open_url_delay=open_url, port=str(port), root=K.build_dir)


@cli.command("clean")
def clean():
    """Clean the build dir """
    title("Cleaning build dir...")
    Kolibri(CWD).clean_build_dir()
    done()

@cli.command("macros")
def macros():
    """Clean the build dir """
    title("Kolibri macros")
    K = Kolibri(CWD)
    macros = K.kolibri_macros
    for m in sorted(macros):
        log("- %s: %s" % (m, macros[m]))
    done()


def cmd():
    try:
        print("*" * 80)
        print("=" * 80)
        title("Kolibri %s!" % __version__)
        print("-" * 80)
        sys_argv = sys.argv
        exempt_argv = ["init", "create", "version", "--version", "-v"]
        kolibri_conf = os.path.join(CWD, "kolibri.yml")
        kolibri_init = os.path.isfile(kolibri_conf)
        if len(sys_argv) > 1:
            if sys_argv[1] in ['-v', '--version']:
                pass                
            elif not kolibri_init and sys_argv[1] not in exempt_argv:
                error("Kolibri is not initialized yet in this directory: %s" % CWD)
                log("Run 'kolibri init' to initialize Kolibri in the current directory")
                footer()
            else:
                cli()
        else:
            cli()
    except Exception as e:
        
        error("Ohhh noooooo! Something bad happens")
        log(">> %s " % e.__repr__())
        footer()
