from django.conf import settings
from time import sleep
import subprocess, sys, os, pexpect

def sign_key(key_data, user_id, principals, serial):
    """
    Sign a key using the SSH CA.
    """
    # Write cert to file with a random filename
    temp_file = os.path.join('/tmp', 'id_ecdsa%d.pub' % serial)
    
    with open(temp_file, 'w') as f:
        print(key_data)
        f.write(key_data.strip('"'))
            
    ssh_ca_path = settings.SSH_CA_CERT_PATH
    password = ''
    if not settings.SSH_CA_CERT_PASSWORD == '':
        password = settings.SSH_CA_CERT_PASSWORD
        
    args = ['ssh-keygen', '-s', ssh_ca_path, '-I', user_id, '-n', principals, '-z', str(serial), '-V', f'+{str(settings.SSH_CA_CERT_VALIDITY)}h', temp_file]
    print(" ".join(args))
    proc = pexpect.spawn(" ".join(args))
    if not password == "":
        proc.expect('Enter passphrase:')
        proc.sendline(password+'\n')
    
    proc.wait()
    output = proc.read()

    if "Signed user key" not in output.decode():
        print(output.decode())
        return False
        
    with open(os.path.join('/tmp', 'id_ecdsa%s-cert.pub' % serial), 'r') as f:
        cert = f.read()
    os.remove(os.path.join('/tmp', 'id_ecdsa%s-cert.pub' % serial))
    os.remove(os.path.join('/tmp', 'id_ecdsa%s.pub' % serial))
    
    return cert