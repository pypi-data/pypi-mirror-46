Various ways of pre-release testing:

- manual, current install

      python -m unittest discover tests/

- cross-version

      tox

- automatic

      (active on drone.io, script saved in drone.sh)
