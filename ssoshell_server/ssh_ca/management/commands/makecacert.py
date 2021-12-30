from django.core.management.base import BaseCommand, CommandError, no_translations
from django.conf import settings
from subprocess import check_output, STDOUT
from os import remove
from os.path import isfile



class Command(BaseCommand):
    help = 'Creates the CA Certificate'
    
    def ask_confirm(self, message):
        confirm = input(message)
        while confirm not in ('y', 'Y', 'yes', 'no', 'n', 'N'):
            print("Please answer yes or no")
            confirm = input(message)
        if confirm in ('y', 'Y', 'yes'):
            return True
        return False
    
    @no_translations
    def handle(self, *args, **options):
        if not settings.SSH_CA_CERT_PATH:
            print("Error: No path set for SSH_CA_CERT_PATH")
            
        if isfile(settings.SSH_CA_CERT_PATH):
            if self.ask_confirm("File already exists. Overwrite? [y/N] "):
                remove(settings.SSH_CA_CERT_PATH)
                remove("%s.pub" % settings.SSH_CA_CERT_PATH)
            else:
                self.stdout.write(self.style.WARNING("File already exists, not overwriting"))
        
        try:
            output = check_output(
                ["ssh-keygen", "-t", "ecdsa", "-f", settings.SSH_CA_CERT_PATH, "-C", "CA", "-N", settings.SSH_CA_CERT_PASSWORD]
            ).decode('utf-8').split('\n')
            
        except Exception as e:
            self.stdout.write(self.style.WARNING("Error creating SSH Certificate"))
            self.stdout.write(self.style.WARNING(e))

        self.stdout.write(self.style.SUCCESS("%s" % output[1]))
        self.stdout.write(self.style.SUCCESS('The key fingerprint is "%s"' % output[4]))