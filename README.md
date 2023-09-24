# ROCK Pi Penta SATA

## Install
A systemd service file is provided to easily install and run the script. And to
easily install the service a script is also provided!
```shell
sudo ./install.sh
# You can configure your installation with (see default values in install.sh):
sudo \
  INSTALL_TARGET_USER="${USER}" \
  DEST_PATH="${HOME}/bin/hat/" \
  LOG_PATH="${HOME}/bin/hat/logs/" \
  ./install.sh
```
