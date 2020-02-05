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

buildFrontend() {
    pushd frontend &> /dev/null
    rm -rf dist/* &> /dev/null
    npm run build
    popd &> /dev/null

    mkdir -p frontend/dist/help/technical/backend
    cp docs/technical/backend/index.html frontend/dist/help/technical/backend || return 1
}

buildDocsUsermanual() {
    mkdir -p frontend/dist/help &>/dev/null || true
    pushd docs &> /dev/null
    npm run generate -- usermanual
    cp usermanual/usermanual.pdf ../frontend/dist/help/usermanual.pdf
    popd &> /dev/null
}

getVersion() {
    local version

    version="$(git tag -l --points-at HEAD)"

    [[ -z "${version}" ]] && version="$(git log -1 --pretty=%h)"

    echo "${version}"
}

main() {
    local forcedVersion="$1"
    local images=("timescaledb" "sla" "frontend")
    local version

    if [[ -n "${forcedVersion}" ]]; then
        git checkout "${forcedVersion}" 1> /dev/null || { error "Failed to checkout ${forcedVersion}"; return 1; }
    fi


    version="$(getVersion)"

    for image in "${images[@]}"; do
        local tag="bolagsratt-xml/${image}:${version}"
        local name="bolagsratt-xml_${image}_"

        if [[ -e "docker/_build/${name}${version}.tar" ]]; then
            warn "${name}${version}.tar already exist"
            continue
        fi

        info "Building ${image} image"

        case "${image}" in
            "frontend")
                buildFrontend || { error "Failed to build frontend"; return 1; }
                buildDocsUsermanual || { error "Failed to build usermanual.pdf"; return 1; }
                ;;
            *)
                ;;
        esac

        rm -f "docker/_build/${name}"*".tar" &> /dev/null || true

        docker build -f "docker/${image}/Dockerfile" -t "${tag}" . | grep -Ev "^ \-\-\->" || { error "Failed to build ${tag}"; return 1; }
        docker save -o "docker/_build/${name}${version}.tar" "${tag}" || { error "Failed to save ${tag}"; return 1; }
        info "Saved ${tag} to docker/_build/${name}${version}.tar..."
    done

    cat > docker/_build/.env <<EOF
COMPOSE_PROJECT_NAME=bolagsratt_xml
VERSION=${version}
EOF

    rm -rf "build/bolagsratt-xml-${version}.tar.gz"
    tar --transform "s/^docker\/_build/bolagsratt-xml_${version}/" -cf "build/bolagsratt-xml_${version}.tar.gz" docker/_build || { error "Failed to create bundle"; return 1; }

    info "Created deployment bundle build/bolagsratt-xml_${version}.tar.gz"

    if [[ -n "${forcedVersion}" ]]; then
        git checkout develop 1> /dev/null || { error "Failed to checkout develop"; return 1; }
    fi

    return 0
}

main "$@"
exit $?
