#!/bin/bash

WORKSPACE=$(pwd)
SYSTEMCTL_DIR=/etc/systemd/system/

CONFIG_FILE="${WORKSPACE}/config.cfg"
PKMN_TCG_SERVICE=card_collector.service
PKMN_TCG_SERVICE_SRC="${WORKSPACE}/${PKMN_TCG_SERVICE}"
PYTHON_VENV="${WORKSPACE}/.venv"

EXIT_CODE=0

if [[ $EUID -ne 0 ]]; then
    echo "RUN AS ROOT"
    exit 1
fi

install_packages() {
    echo "Install system packages"
    apt update -y && apt install -y sqlite3 python3-venv
}

create_venv() {
    echo "Creating Python venv"
    # Create virtual environment
    python3 -m venv "${PYTHON_VENV}"
    source "${PYTHON_VENV}/bin/activate"
    # Install requirements
    echo "Installing requirements"
    python3 -m ensurepip --upgrade
    pip install -r "${WORKSPACE}/requirements.txt"
    chown -R "${SUDO_USER}:${SUDO_USER}" "${PYTHON_VENV}"
}

install_service() {
    sed -i "s,INSTALL_USER,${SUDO_USER},g" "${2}"
    sed -i "s,INSTALL_DIR,${1},g" "${2}"
    cp "${2}" "${SYSTEMCTL_DIR}"
}

run_service() {
    systemctl start "${1}"
    systemctl enable "${1}"
}

install_system_services() {
    echo "Installing services"
    install_service "${WORKSPACE}" "${PKMN_TCG_SERVICE_SRC}"
    systemctl daemon-reload
    run_service "${PKMN_TCG_SERVICE}"
}

if [ $EXIT_CODE -eq 0 ]; then
    install_packages
    EXIT_CODE=$?
fi
if [ $EXIT_CODE -eq 0 ]; then
    create_venv
    EXIT_CODE=$?
fi
if [ $EXIT_CODE -eq 0 ]; then
    install_system_services
    EXIT_CODE=$?
fi
if [ $EXIT_CODE -ne 0 ]; then
    echo "INSTALL FAILED"
fi

