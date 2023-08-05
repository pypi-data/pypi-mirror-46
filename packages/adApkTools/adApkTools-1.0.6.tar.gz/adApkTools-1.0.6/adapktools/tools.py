# -*- coding:utf-8 -*-
import os
import platform as pt
import re
import shutil
import zipfile

if pt.system() == 'Windows':
    platform = 'windows'
else:
    platform = 'linux'

module_path = os.path.dirname(__file__)
TEMP_DIR = os.path.join(module_path, 'tmp')
apksigner_path = os.path.join(module_path, 'lib',platform, 'apksigner.jar')
java_path = 'java'
appt_path = os.path.join(module_path, 'lib', platform, 'aapt')
zipalign_path = os.path.join(module_path, 'lib', platform, 'zipalign')


if not os.path.isdir(TEMP_DIR):
    os.mkdir(TEMP_DIR)


def align(input_path, output_path):
    cmd = ' '.join([zipalign_path, '-v', '4', input_path, output_path])
    rt = os.system(cmd)
    if rt != 0:
        raise Exception('align {} got error'.format(input_path))


def sign(input_path, output_path, keysotre=None, kspass=None, keypass=None, keyalias=None):
    if len(keysotre) > 100:
        tmp_file_name = 'keystore_{}'.format(os.path.basename(input_path))
        key_store = os.path.join(TEMP_DIR, tmp_file_name)
        with open(key_store, 'wb') as f:
            f.write( keysotre )
    else:
        key_store = keysotre

    cmd = ' '.join(
        [java_path, '-jar', apksigner_path,'sign', '--ks', key_store, '--ks-pass', 'pass:{}'.format(kspass), '--key-pass',
         'pass:{}'.format(keypass), '--ks-key-alias', keyalias, '--out', output_path, input_path])
    rt = os.system(cmd)
    # remove tmp file
    if os.path.isfile(tmp_file_name):
        os.remove(tmp_file_name)
    if rt != 0:
        raise Exception('sign {} got error'.format(input_path))


def alignSign(input_path, output_path, keysotre=None, kspass=None, keypass=None, keyalias=None):
    file_name = 'aligned_{}'.format(os.path.basename(input_path))
    tmp_aligned = os.path.join(TEMP_DIR, file_name)
    try:
        align(input_path, tmp_aligned)
        sign(tmp_aligned, output_path, keysotre, kspass, keypass, keyalias)
    finally:
    # remove tmp file
        os.remove(tmp_aligned)
    return True


def makeAdApk(signed_apk, output_path, channel_info):
    shutil.copy(signed_apk, output_path)
    zipped = zipfile.ZipFile(output_path, 'a', zipfile.ZIP_DEFLATED)
    empty_channel_file = "assets/dap.properties"
    writein_file_path = getTmpPropertiesFile(channel_info)
    zipped.write(writein_file_path, empty_channel_file)
    # remove tmp file
    os.remove(writein_file_path)
    zipped.close()


def getTmpPropertiesFile(channel_info):
    import hashlib
    md5 = hashlib.md5()
    md5.update(str(channel_info).encode('utf-8'))
    file_name = md5.hexdigest()
    if not isinstance(channel_info, dict):
        raise Exception('Channel_info must be dict.')
    tmp_path = os.path.join(TEMP_DIR, file_name)
    strings = ['='.join([k, str(v)]) for k, v in channel_info.items()]
    with open(tmp_path, 'w') as f:
        f.write("\n".join(strings))
    return tmp_path


def getApkInfo(apk_path):
    p = re.compile(r".*?\s(\w+)\='(.*?)'")
    cmd = ' '.join([appt_path, 'dump', 'badging', apk_path])
    f = os.popen(cmd)
    row = f.readline()
    rt = dict(p.findall(row))
    return rt
