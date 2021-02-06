import argparse
import sys
import subprocess

# Process arguments
parser = argparse.ArgumentParser(description='Setup a new apache virtual host on an Ubuntu system. Only tested on versions 18.04 and 20.04')
parser.add_argument('domain_name', metavar='D', type=str, nargs='+', help='domain name to give to virtual host. multiple domains can be specified at once')
args = parser.parse_args()

# Confirm action with user
print("The following virtual host(s) will be created under their respective names.")
fa_flag = False
for arg in vars(args):
    print(getattr(args, arg))

while True:
    ans = input("Proceed? [Y/n] ")
    if ans == 'n' or ans == 'N':
        print("Exiting")
        quit()
    elif ans == 'Y' or ans == 'y':
        print("Proceeding")
        break
    else:
        print("Invald input")

# Install apache2 if not yet installed
install_sts = subprocess.call(['test', '-e', '/etc/apache2'])
if install_sts != 0:
    print("Installing Apache")
    subprocess.call(['sudo', 'apt', 'install', 'apache2'])
    subprocess.call(['ufw', 'allow', "'Apache'"])

# Iterate though each virtual host to be created
for vh in sys.argv:
    if vh == 'create_apache_vhost.py':
        continue
    
    print("Creating virtual host: " + vh)

    src_path = '/var/www/' + vh
    subprocess.call(['sudo', 'mkdir', src_path])
    subprocess.call(['sudo', 'chown', '-R', '$LOGNAME:$LOGNAME', src_path])
    subprocess.call(['sudo', 'chmod', '755', src_path])
    subprocess.call(['sudo', 'touch', src_path + 'index.html'])

    with open(src_path + '/index.html', 'a') as out:
        out.write("""<html>
    <head>
        <title>Welcome to """ + vh + """</title>
    </head>
    <body>
        <h1>""" + vh + """ virtual host is working!</h1>
    </body>
</html>""")
    
    conf_path = '/etc/apache2/sites-available/' + vh + '.conf'
    subprocess.call(['sudo', 'touch', conf_path])

    with open(conf_path, 'w') as out:
        out.write("""<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName """ + vh + """
    ServerAlias www.""" + vh + """
    DocumentRoot /var/www/""" + vh + """
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>""")

    print("\n   [" + vh + "] virtual host was successfully created")
    print("    - Source is located at " + src_path)
    print("    - Config file is located at " + conf_path + "\n")


    


    


    
