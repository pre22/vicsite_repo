#!/bin/bash

declare -A ARRAY_OF_ENV_FILES

PROJECT_NAME='SIMPLE DJANGO PROJECT'
BACKEND_SERVICE_NAME='backend'
CONFIG_DIR='configs'
ENV_FILES_DIR="${CONFIG_DIR}/envs/"
# SUBDOMAINS=("api" "cpanel" "pages" "www")
SUBDOMAINS=("www")
ROOT_DOMAIN_NAME="avaloqsassets.com"
PGADMIN4_SUBDOMAIN_NAME="pgadmin4"
ARRAY_OF_ENV_FILES=(
  [nginxproxy]="nginxproxy.env"
  [nginxproxy_letsencrypt]="nginxproxy_acme.env"
  [pgadmin]="pgadmin4.env"
  [postgres]="postgres.env"
  [redis]="redis.env"
  [backend]="backend.env"
)

close_color="\e[0m"
color_close="${close_color}"
color_reset="${color_close}"
color_invert="\e[7m"
invert_color="${color_invert}"
default_color="\e[39m"
default_bg="\e[49m"
reset_color="${color_close}"

blink="\e[5m"
bold="\e[1m"
dim_color="\e[2m"
hide_color="\e[8m"
italic="\e[3m"
underline="\e[4m"

close_blink="\e[25m"
close_bold="\e[21m"
close_dim="\e[22m"
close_hidden="\e[28m"
close_invert="\e[27m"
close_underline="\e[24m"

black_color="\e[30m"
blue_color="\e[34m"
cyan_color="\e[36m"
green_color="\e[32m"
light_green_color="\e[92m"
majenta_color="\e[35m"
red_color="\e[31m"
white_color="\e[97m"

black_bg="\e[40m"
blue_bg="\e[44m"
cyan_bg="\e[46m"
dark_gray_bg="\e[100m"
green_bg="\e[42m"
light_red_bg="e[101m"
light_gray_bg="\e[47m"
majenta_bg="\e[45m"
red_bg="\e[41m"
white_bg="\e[107m"
yellow_bg="\e[43m"

generate_env_files() {
  local config_env_dir="${ENV_FILES_DIR%/}"
  mkdir -p "${config_env_dir}"
  for env_file in "${!ARRAY_OF_ENV_FILES[@]}"; do
    local env_file_with_path
    env_file_with_path="${config_env_dir%/}/${ARRAY_OF_ENV_FILES[${env_file}]}"
    if [[ -f "${env_file_with_path}" ]]; then
      rm -r "${env_file_with_path}"
    fi
    touch "${env_file_with_path}"
  done
}

create_env_files() {
  generate_env_files
}

base_docker_command_for_backend() {
  echo "docker-compose exec ${BACKEND_SERVICE_NAME} python manage.py"
}

cleaned_domain_name() {
  if [[ ${#*} -ne 1 ]]; then
    echo "You must supply a URL to validate"
    exit 1
  fi
  local domain_name=$1
  case ${domain_name} in
  https://)
    domain_name=${domain_name#https://}
    ;;
  http://)
    domain_name=${domain_name#http://}
    ;;
  www.)
    domain_name=${domain_name#www.}
    ;;
  https://www.)
    domain_name=${domain_name#https://www.}
    ;;
  http://www.)
    domain_name=${domain_name#http://www.}
    ;;
  esac

  echo "${domain_name}" | grep -q '/'
  if [[ ${?} -eq 0 ]]; then
    domain_name=${domain_name%/}
  fi
  echo "${domain_name#https://}"
}

generate_random() {
  echo "Generating random"
}

grep_match_domain_name() {
  local domain_name_regex="(https://|https://)?(w{3}\.)?([a-zA-Z0-9]+[-\._]?)*[a-zA-Z0-9]+(\.[a-zA-Z0-9]+){1,2}/?$"
  echo "${domain_name_regex}"
}

generate_secret_code() {
  local random_code secret_code
  random_code=$(tr -cd "'[[:alnum:][:punct:]]'" </dev/urandom | tr -d "'[\"\'\\]'" | head -c 50)
  secret_code="django-secure-${random_code}"
  echo "${secret_code}"
}

trim_whitespaces() {
  { test $# -ne 1 && echo "Argument must just be one" || test -z "${1}" && echo "First argument cannot be blank"; } && exit 1
  echo "${1}" | grep -Eq "^[[:space:]]+$"
  test $? -eq 0 && echo "Argument cannot start and end with ${#1} whitespaces" && exit 1
  echo "${1}" | tr -d "[:space:]"
}

validate_domain_name() {
  local domain_name=${1}
  local domain_name_regex="^(https://|https://)?(w{3}\.)?([a-zA-Z0-9]+[-\._]?)*[a-zA-Z0-9]+(\.[a-zA-Z0-9]+){1,2}/?$"
  if [[ $domain_name =~ $domain_name_regex ]]; then
    return 0
  fi
  return 1
}

validate_email() {
  local email
  email=$1
  echo "${email}" | grep -E -iqw '^[[:alnum:]]+(\.?[[:alnum:]])+@[[:alnum:]]+(\.[[:alnum:]]+){1,2}$'
  return $?
}

setup_allowed_hosts() {
  local hosts=${1}
  local current_dir production_settings_file
  current_dir=$(dirname "${0}")
  production_settings_file="${current_dir}/src/config/settings/production.py"
  sed -i "/ALLOWED_HOSTS/d" "$production_settings_file"
  echo -e "\nALLOWED_HOSTS = [${hosts}]\n" >>"$production_settings_file"
}

setup_postgres() {
  local postgres_db_name postgres_db_user postgres_db_password
  local postgres_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[postgres]}"
  local backend_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[backend]}"
  echo "Setting up postgres"
  read -p "Enter your postgres DB name: " postgres_db_name
  read -p "Enter your postgres DB username: " postgres_db_user
  echo "Enter your postgres DB password: "
  read -s
  postgres_db_password=${REPLY}

  echo -e \
    "POSTGRES_DB=${postgres_db_name}\nPOSTGRES_USER=${postgres_db_user}\nPOSTGRES_PASSWORD=${postgres_db_password}" \
    >"${postgres_env_file}"
  echo -e \
    "BACKEND_DB_NAME=${postgres_db_name}\nBACKEND_DB_USER=${postgres_db_user}\nBACKEND_DB_PASSWORD=${postgres_db_password}" \
    >>"${backend_env_file}"
}

setup_pgadmin4() {
  echo "Setting up pgadmin4"

  local pgadmin4_email_address pgadmin4_password is_valid=false
  local pgadmin4_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[pgadmin]}"
  until $is_valid; do
    read -p "Enter PGADMIN4 login e-mail address: " pgadmin4_email_address
    validate_email "${pgadmin4_email_address}"
    if [[ $? -eq 0 ]]; then
      echo "${pgadmin4_email_address}"
      is_valid=true
    fi
  done
  until [[ -n ${pgadmin4_password} ]]; do
    echo "Please enter your PGADMIN4 login password: "
    read -rs
    pgadmin4_password=${REPLY}
  done
  echo -e "PGADMIN_DEFAULT_EMAIL=${pgadmin4_email_address}" >>"${pgadmin4_env_file}"
  echo -e "PGADMIN_DEFAULT_PASSWORD=${pgadmin4_password}" >>"${pgadmin4_env_file}"

}

make_migrations() {
  $(base_docker_command_for_backend) makemigrations
}

migrate() {
  $(base_docker_command_for_backend) migrate
}

collect_static_files() {
  $(base_docker_command_for_backend) collectstatic --no-input
}

load_dummy_data() {
  $(base_docker_command_for_backend) loaddata db.json
}

post_installation_setup() {
  make_migrations
  migrate
  load_dummy_data
  collect_static_files
}

setup_domain_name() {
  local clean_domain is_valid=false
  until $is_valid; do
    read -p "Please enter your domain name: " domain_name
    validate_domain_name "${domain_name}"
    if [[ $? -eq 0 ]]; then
      clean_domain=$(cleaned_domain_name "${domain_name}")
      echo "${clean_domain}"
      is_valid=true
    fi
  done
}

setup_email() {
  local email_address is_valid=false
  until $is_valid; do
    read -p "Enter e-mail address: " email_address
    validate_email "${email_address}"
    if [[ $? -eq 0 ]]; then
      echo "${email_address}"
      is_valid=true
    fi
  done
}

setup_backend() {
  local secret_key domain_name subdomains ALLOWED_DOMAINS
  local backend_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[backend]}"
  echo "Backend configuration setup"
  secret_key=$(generate_secret_code)
  domain_name="$(setup_domain_name)"
  subdomains="${domain_name},"
  ALLOWED_DOMAINS="'${domain_name}', "
  for subdomain in ${SUBDOMAINS[*]}; do
    subdomains+="${subdomain}.${domain_name},"
    ALLOWED_DOMAINS+="'${subdomain}.${domain_name}', "
  done
  ALLOWED_DOMAINS=${ALLOWED_DOMAINS%, } # trail out ending comma and whitespace
  echo -e "BACKEND_SECRET_KEY=${secret_key}" >>"$backend_env_file"
  echo -e "VIRTUAL_HOST=${subdomains%,}\nLETSENCRYPT_HOST=${subdomains%,}" >>"$backend_env_file"

  local pgadmin4_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[pgadmin]}"
  local pgadmin4_domain="${PGADMIN4_SUBDOMAIN_NAME}.${domain_name}"
  local pgadmin4_domain="${pgadmin4_domain}"
  echo -e "VIRTUAL_HOST=${pgadmin4_domain}\nLETSENCRYPT_HOST=${pgadmin4_domain}" >>"${pgadmin4_env_file}"

  setup_allowed_hosts "$ALLOWED_DOMAINS"
}

global_configuration_setup() {
  local email_address
  local nginxproxy_acme_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[nginxproxy_letsencrypt]}"
  local backend_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[backend]}"
  local pgadmin4_env_file="${ENV_FILES_DIR}/${ARRAY_OF_ENV_FILES[pgadmin]}"

  echo -e "GENERAL CONFIGURATION"
  echo "This is a one time configuration setup that will be shared across all other subsequent installation"
  email_address=$(setup_email)
  echo "DEFAULT_EMAIL=${email_address}" >"$nginxproxy_acme_env_file"
  echo -e "LETSENCRYPT_EMAIL=${email_address}" >>"$backend_env_file"
  echo -e "LETSENCRYPT_EMAIL=${email_address}" >>"$pgadmin4_env_file"

}

start() {
  echo -e "${bold}WELCOME TO ${PROJECT_NAME}${close_color}"
  echo ""
  echo ""
  create_env_files
  global_configuration_setup
  echo ""
  echo ""
  setup_postgres
  echo ""
  echo ""
  setup_backend
  echo ""
  echo ""
  setup_pgadmin4
  echo ""
  echo ""
  docker-compose up -d
  echo ""
  post_installation_setup
}

start