#!/bin/bash
install_folder=$(dirname $(realpath $0))
scripts_folder=$(dirname $(dirname $(realpath $0)))
user_services=~/".config/systemd/user"

service_name="media_node.service"
script_name="run_media_node.sh"

if test $EUID == 0; then
    echo "run as non-root user"
    exit
fi

# apply the correct path
sed -i "s|^ExecStart=.*|ExecStart=$scripts_folder/$script_name|" $install_folder/$service_name

# make the script executable
chmod +x $scripts_folder/$script_name

# create a folder for current user services
loginctl enable-linger $(logname)
mkdir -p $user_services

# copy systemd service unit file
cp "$install_folder/$service_name" "$user_services"

# enable service
systemctl --user enable $service_name
echo "service enabled"
