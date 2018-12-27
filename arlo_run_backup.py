from ArloGooglePhotos import ArloGooglePhotos
from Arlo import Arlo
# Arlo auth
USER = 'arlo username'
PASS = 'arlo password'
arlo = Arlo(USER, PASS)
arlo_backup = ArloGooglePhotos(arlo)
arlo_backup.run()