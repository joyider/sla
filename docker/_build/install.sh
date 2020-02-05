#!/usr/bin/env bash

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m' # No Color

info() {
    _log "$*"
}

error() {
    _log "$*"
}

warn() {
    _log "$*"
}

_log() {
    local color
    local level="${FUNCNAME[1]}"

    case "${level}" in
        "info")
            color="${GREEN}"
            ;;
        "error")
            color="${RED}"
            ;;
        "warn")
            color="${YELLOW}"
            ;;
        *)
            color="${RESET}"
            ;;
    esac

    echo -e "${color}${level^^}${RESET}: $*"
}

install() {
    docker load -i "$1"
}

main() {
    # shellcheck disable=SC1091
    . .env

    local new_version
    local old_version
    new_version="$(basename "${PWD}")"

    pushd ../ &>/dev/null
    if [[ -L "bolagsratt-xml" ]]; then
        old_version="$(basename "$(realpath bolagsratt-xml)")"
        [[ "${new_version}" == "${old_version}" ]] && { error "You are trying to install ${new_version} which is already deployed"; return 1; }
        info "Replacing ${old_version} with ${new_version}"
    else
        info "Installing ${new_version}"
    fi
    popd &>/dev/null

    # copy production configuration, if it exist
    if [[ -e ../bolagsratt-xml/docker-compose.yaml ]]; then
        cp ../bolagsratt-xml/docker-compose.yaml . &>/dev/null || true
    else
        warn "Did not find docker-compose.yaml from a previous version, review the current one to make sure it will work"
    fi

    for image in *.tar; do
        install "${image}" || { error "Failed to install ${image}"; return 1; }
        info "Imported ${image}"
    done

    docker-compose up -d || { error "Failed to bring up bolagsratt_xml"; return 1; }

    rm -- *.tar &> /dev/null || true

    pushd ../ &>/dev/null
    ln -sfn "${new_version}" bolagsratt-xml
    popd &>/dev/null

}

main "$@"
exit $?
