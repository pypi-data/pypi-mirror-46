# Copy of test recipe used on drone.io
#
# Configuration:
#    Language:  Python2.7
#    No Database
#    No Environment Variables
#    Work dir: /home/ubuntu/src/bitbucket.org/Mekk/mercurial-extension_utils
#         (can't change)

pip install Mercurial --use-mirrors
python -m unittest discover tests

pip install tox
tox -e py27-hg27,py27-hg29,py27-hg32,py27-hg33
