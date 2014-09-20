import sys,os, shutil

PROJECT_PATH = os.path.abspath(__file__ + "/../../")
PROJECT_NAME = "soulightrd"

CATALOGUE = "CATALOGUE"
COMMENT_CHARACTER = "<!--"

YUI_COMPRESSOR = PROJECT_NAME + "/vendor/compressor/yuicompressor-2.4.2.jar"
HTML_COMPRESSOR = PROJECT_NAME  + "/vendor/compressor/htmlcompressor-1.5.3.jar"
COMPRESSOR = {"html": HTML_COMPRESSOR, "css": YUI_COMPRESSOR, "js": YUI_COMPRESSOR}

def compress(in_files, out_file, in_type='js', verbose=False,
             temp_file='.temp'):
    temp = open(temp_file, 'w')
    for f in in_files:
        fh = open(f)
        data = fh.read() + '\n'
        fh.close()

        temp.write(data)

        print ' + %s' % f
    temp.close()

    options = ['-o "%s"' % out_file,
               '--type %s' % in_type]

    if in_type == "html":
        options.append("--compress-js")
        options.append("--compress-css")

    if verbose:
        options.append('-v')

    cmd = 'java -jar "%s" %s "%s"' % (COMPRESSOR[in_type],' '.join(options),temp_file)
    os.system(cmd)

    org_size = os.path.getsize(temp_file)
    new_size = os.path.getsize(out_file)

    print '=> %s' % out_file
    print 'Original: %.2f kB' % (org_size / 1024.0)
    print 'Compressed: %.2f kB' % (new_size / 1024.0)
    print 'Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100)
    print ''


def listFiles(rootdir,fileList):
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            f = os.path.join(root,file)
            fileList.append(f)


def copyRecursive(src,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src,dest)
 

def readCatalogue(list_file,path):
    f = open(path + CATALOGUE,"r")
    for filename in f:
        if len(filename.replace("\n","")) != 0 and filename.startswith(COMMENT_CHARACTER) == False:
            list_file.append(path + filename.replace("\n",""))


def setupFiles(list_file,path):
    if os.path.exists(path + CATALOGUE):
        readCatalogue(list_file,path)
    else:
        new_list_file = []
        files = os.listdir(path)
        for filename in files:
            new_list_file.append(path + filename)
        new_list_file.sort()
        list_file += new_list_file


def setupStatic():
    dajaxice_script_src = PROJECT_PATH + "/assets/static/js/dajaxice.core.js"
    dajaxice_scripts_out = PROJECT_PATH + "/assets/static/js/prod/dajaxice.core.min.js"
    compress([dajaxice_script_src], dajaxice_scripts_out, 'js', False)

    # Minify the global javascript
    global_scripts_src = PROJECT_PATH + "/assets/static/js/global/"
    scripts = []
    setupFiles(scripts,global_scripts_src)
    scripts_out = PROJECT_PATH + "/assets/static/js/prod/" + PROJECT_NAME + ".script.global.min.js"
    compress(scripts, scripts_out, 'js', False)

    # Minify the global plugin javascript
    plugin_src = PROJECT_PATH + "/assets/static/js/plugins/"
    plugin_scripts = []
    setupFiles(plugin_scripts,plugin_src)
    plugin_scripts_out = PROJECT_PATH + "/assets/static/js/prod/" + PROJECT_NAME + ".script.plugins.global.min.js"
    compress(plugin_scripts,plugin_scripts_out,"js",False)

    # # Minify the javascript of each app
    js_src = PROJECT_PATH + "/assets/static/js/apps/"
    files = os.listdir(js_src)
    files.sort()
    for filename in files:
        if ".js" not in filename:

            dir_app = js_src + filename + "/"
            if not os.path.exists(dir_app + "prod"):
                os.makedirs(dir_app + "prod")

            subapp_plugin_scripts_out = None
            if os.path.exists(dir_app + "plugins"):
                subapp_plugin_files = os.listdir(dir_app + "plugins")
                if len(subapp_plugin_files) > 0:
                    subapp_plugin_scripts = []
                    subapp_plugin_files.sort()
                    for plugin_file in subapp_plugin_files:
                        subapp_plugin_scripts.append(dir_app + "plugins/" + plugin_file)
                    subapp_plugin_scripts_out = dir_app + "prod" + "/" + PROJECT_NAME + ".script.plugins.app.min.js"
                    compress(subapp_plugin_scripts,subapp_plugin_scripts_out,"js",False)

            
            subapp_scripts = [
                    plugin_scripts_out,
                    scripts_out,
                    dir_app + "function.js",
                    dir_app + "ajax.js",
                    dir_app + "main.js",
                ]
            
            if subapp_plugin_scripts_out != None:
                subapp_scripts.insert(2,subapp_plugin_scripts_out)

            subapp_scripts_out = dir_app + "prod" + "/" + PROJECT_NAME + ".script.app.min.js"
            compress(subapp_scripts, subapp_scripts_out, 'js', False)

    # Clear all the already minified css
    css_dest = PROJECT_PATH + "/assets/static/css/prod/"
    for filename in os.listdir(css_dest):
        if "css" in filename:
            os.remove(css_dest + filename)

    
    # Minify the plugin and global css and output to one final file
    css_global_src = PROJECT_PATH + "/assets/static/css/global/"
    css_plugins_src = PROJECT_PATH + "/assets/static/css/plugins/global/stylesheets/"
    css_plugins_resources_src = PROJECT_PATH + "/assets/static/css/plugins/global/resources/"
    
    plugins_resources_files = os.listdir(css_plugins_resources_src)
    
    for filename in plugins_resources_files:
        copyRecursive(css_plugins_resources_src + filename,css_dest + filename)

    style_css = []

    setupFiles(style_css,css_plugins_src)
    setupFiles(style_css,css_global_src)

    style_css_out = css_dest + "stylesheets/styles.min.css"
    compress(style_css, style_css_out, 'css')

    # List all processing css file
    css_subapp_src = PROJECT_PATH + "/assets/static/css/apps/"
    subapp_files = os.listdir(css_subapp_src)
  
    # Minify the css for each sub app combine with the global stylesheet
    for filename in subapp_files:
        subapp_css = [style_css_out,css_subapp_src + filename]
        subapp_css_out = css_dest + "stylesheets/" + filename[0:filename.rfind(".")] + ".min.css"
        compress(subapp_css, subapp_css_out, "css")


def main():
    print "...RUNNING SETUP ASSETS SCRIPT..."
    try:
        stage = sys.argv[1]
        if stage == "prod" or stage == "beta":
            setupStatic()
            print "Setup assests successfully"
        else:
            print "No need to compress asset in the development mode"
    except Exception:
        print "Setup assets error"
        raise

if __name__ == "__main__":
    main() 
