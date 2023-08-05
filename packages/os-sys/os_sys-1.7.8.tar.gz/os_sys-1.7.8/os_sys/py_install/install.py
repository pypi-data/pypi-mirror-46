import os, sys
#installer
#python3.7
#devlopment
import os, sys
#installer
#python3.7
#devlopment
import os, sys
__all__ = ['install']
import tqdm
import psutil  # nu copy de dict waar files in geplaatst zijn
def process_exists(name):
    i = psutil.pids()
    for a in i:
        try:
            if str(psutil.Process(a).name) == name:
                return True
        except:
            pass
    return False
import shutil
def copytree(src, dst, symlinks=False, ignore=None):
    import tqdm
    items = tqdm.tqdm(os.listdir(src))
    fi = False
    for item in items:
        if fi == False:
            fi == item
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
    items.close()
    return fi

def all_dict(dictory, ex=False, exceptions=None, file_types=['py_install'], maps=False, files=True, print_data=False):
    import os
    data = []
    string_data = ''
    e = exceptions
    if 'list' in str(type(e)) or e == None:
        pass
    else:
        raise TypeError('expected a list but got a %s' % type(e))
    e = file_types
    if 'list' in str(type(e)) or e == None:
        pass
    else:
        raise TypeError('expected a list but got a %s' % type(e))
    
    print_ = True if print_data == 'print' or print or True else False
    
    for dirname, dirnames, filenames in os.walk(dictory):
        # print path to all subdirectories first.
        if maps:
            for subdirname in dirnames:
                dat = os.path.join(dirname, subdirname)
                data.append(dat)
                string_data = string_data + '\n' + dat
                if print_:
                    print(dat)

        # print path to all filenames.
        if files:
            for filename in filenames:
                s = False
                fname_path = filename
                file = fname_path.split('.')
                no = int(len(file) - 1)
                file_type = file[no]
                if not e == None:
                    for b in range(0, len(e)):
                        if e[b] == file_type:
                            s = True
                            
                if e == None:
                    s = True
                if s:
                    s = False   
                            
                    dat = os.path.join(dirname, filename)
                    data.append(dat)
                    string_data = string_data + '\n' + dat
                    if print_:
                        
                        print(dat)
        
        

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if not exceptions == None:
            
            for ip in range(0, int(len(exceptions))):
                exception = exceptions[ip]
                
                if exception in dirnames:
                    # don't go into any .git directories.
                    dirnames.remove(exception)
                elif exception in filename and data:
                    data.remove(exception)
        
    
    return [data, string_data]
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value # Instance of bytes
def install_zip(zip_file, end_dir, rpath):
    print('unzipping...', file=sys.stderr)
    import tqdm 
    from zipfile import ZipFile
    with ZipFile(zip_file, 'r') as zipObj:
        # Get a list of all archived file names from the zip
        files = zipObj.namelist()
        import tqdm
        Bar = tqdm.tqdm(files)
        # Iterate over the file names
        first = None
        for fileName in Bar:
            # Extract a single file from zip
            if first == None:
                first = fileName
            try:
                zipObj.extract(fileName, end_dir)
            except:
                pass
        Bar.close()
        print('installing...')
        return copytree(rpath + '\\' + os.path.dirname(first).replace('/', '\\'), end_dir)

        
        

import tempfile
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value # Instance of str
def stl(s):
    # string naar lijst
    l = []
    for i in range(0,len(s)): l += s[i]
    return l
def install(path):
    global name
    print('searching files...', file=sys.stderr)
    file = all_dict(path)[0][0]
    from distutils.sysconfig import get_python_lib as gpl
    print('building...', file=sys.stderr)
    with open(file, mode='rb') as fh:
        mystr = to_str(str(str(str(to_str(fh.read())).replace('\n', '')).replace('\\r', '\r')).replace('\\n', ''))
    e = mystr.split('\r')
    the = all_dict(path, ex=False, exceptions=None, file_types=['py_install_zip'], maps=False, files=True, print_data=False)[0][0]
    mystr.replace('\n', '')
    with open(all_dict(path, ex=False, exceptions=None, file_types=['info'], maps=False, files=True, print_data=False)[0][0]) as info:
        rpackage_info = str(info.read())
    package_info = rpackage_info.split('\n')
    print('getting info about package...', file=sys.stderr)
    info_dict = {}
    for small in package_info:
        try:
            key, value = small.split('=')
            info_dict[key] = value
            value = value
            
        except:
            pass
        else:
            if 'name' in key:
                from distutils.sysconfig import get_python_lib as gpl
                base_path = os.path.join(gpl(), value)
                name = value
                del key, value
                continue
            elif key == 'version':
                version = value
                del key, value
                continue
            else:
                del key, value
                continue
    from distutils.sysconfig import get_python_lib as gpl
    print('generating info file...', file=sys.stderr)
    lijst = info_dict['maps']
    lijst = str(str(str(str(lijst.replace('[', '')).replace(']', '')).replace("'", '')).replace('\\\\', '\\')).split(", ")
    print(type(lijst))
    
    base = gpl() + '\\' + info_dict['name']
    if os.path.isdir(base):
        print('found older installation')
        print('uninstalling...')
    try:
        shutil.rmtree(base, True)
        print('done')
    except Exception:
        pass
    try:
        os.mkdir(base)
    except:
        pass
    try:
        os.mkdir(base)
        os.mkdir(os.path.abspath('\\lib'))
    except Exception:
        pass
    for inum in range(0, len(lijst)):
        i = lijst[inum]
        print(os.path.join(base, i))
        try:
            os.remove(base + '\\' + i)

        except:
            pass
    try:
        os.makedirs(lijst)
    except:
        pass
    try:
        os.makedirs(base)
    except:
        pass
    with open(os.path.join(gpl(), info_dict['name'], 'data.info'), mode='w+') as done:
        done.write(rpackage_info)
    print('building to temp file...', file=sys.stderr)
    mystr = mystr.split('##########')
    tp = tempfile.mkdtemp()

    import time
    pbar = tqdm.tqdm(mystr)
    if time != None:
        for i in pbar:
            
            try:
                path, data = i.split('>>>>>>>>>>>>>>>')
                a = path
            except Exception:
                pass
            else:
                
                data = str(data)
                from distutils.sysconfig import get_python_lib as gpl
                path2 = tp

                pat = path2 + '\\' + path
                dir_ = os.path.dirname(pat)
                try:
                    os.mkdir(dir_)
                except:
                    pass
                try:
                    with open(pat, mode='wb') as kk:
                        kk.write(to_bytes(str(str(data).replace('\\r', '\r')).replace('\\n', '')))
                except Exception:
                    pass
                
    pbar.close()
    fik = install_zip(the, base, base)
    print('removing temp dict...', file=sys.stderr)
    shutil.rmtree(tp, True)

    print('done!', file=sys.stderr)






