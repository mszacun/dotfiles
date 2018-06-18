export WORKSPACE=$HOME/aginoodle
export FT=$WORKSPACE/src/backlog/tests/feature_tests/
export MT=$WORKSPACE/src/backlog/tests/module_tests/
export UT=$WORKSPACE/src/backlog/tests/unit_tests/

AGI_SCRIPT_DIR="$HOME/dotfiles/aginoodle/scripts"
export PATH="$PATH:$AGI_SCRIPT_DIR"

alias IWONA_PAVLOVIC="pylint --rcfile=$WORKSPACE/config/pylint.cfg --msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}'"
alias agi="cd $WORKSPACE"
alias atd="cd $WORKSPACE/src/backlog/tests"
alias ft="t src/backlog/tests/feature_tests/"
alias mt="t src/backlog/tests/module_tests/"
alias ut="t src/backlog/tests/unit_tests/"
alias jt='(cd $WORKSPACE/src/backlog/; PATH=$HOME/firefox:$PATH http_proxy= https_proxy= ../../bin/jasmine-ci)'
alias jasmine='(cd $WORKSPACE/src/backlog/; ../../bin/jasmine)'
alias at='runall'
alias backlog="$WORKSPACE/bin/backlog"
alias shell="$WORKSPACE/bin/backlog shell_plus --ipython"
alias runserver="cd $WORKSPACE; backlog runserver"
alias npmdev="cd $WORKSPACE; npm run dev"
alias dbshell="mycli -u root aginoodle"
alias mysql='mycli'
alias stelle='(cd $WORKSPACE; ../AginoodleStelle/stelle_run.py)'
alias cooker='(cd ~/noodlecooker; bin/python bin/requester.py ~/aginoodle feature_tests)'
alias glonull='ssh glonull'
alias durszlak='ssh durszlak'
alias teamcal='(cd $HOME/teamcal; php56 -S localhost:5000 -t .)'

function t() {
    USE_XVFB=0
    other_options=()

    while [[ $1 ]]
    do
    case "$1" in
      --xvfb)
          shift
          USE_XVFB=1
          ;;
      *)
          other_options+=("$1")
          shift
          ;;
    esac
    done

    COMMAND="zsh -ic \"(cd $WORKSPACE; PATH=$HOME/firefox:$PATH http_proxy= https_proxy= bin/py.test --reuse-db ${other_options[@]})\""
    if [ $USE_XVFB -eq 1 ]; then
        COMMAND="xvfb-run $COMMAND"
    fi
    
    eval $COMMAND
}

alias omt='docker-compose exec backend pytest'

function show_tests() {
    grep "def test" $1 | sort | grep "test"
}

function runall() {
    echo "DROP DATABASE test_aginoodle" | \mysql -u root
    cd $WORKSPACE
    bin/fab clean_pyc
    tmux split-window -t:.0
    tmux split-window -h -t:.1
    tmux split-window -h -t:.0

    tmux send-keys -t:.0 ut
    tmux send-keys -t:.0 Enter
    tmux resize-pane -t:.0 -y 15

    tmux send-keys -t:.1 mt
    tmux send-keys -t:.1 Enter

    tmux send-keys -t:.2 cooker
    tmux send-keys -t:.2 Enter

    tmux send-keys -t:.3 jt
    tmux send-keys -t:.3 Enter
}

function agirun() {
    tmux new-window
    tmux send-keys "runserver"
    tmux send-keys Enter

    tmux split-window -h
    tmux send-keys "npmdev"
    tmux send-keys Enter
}

function getagibackup() {
    BACKUP_LOCATION=$1
    GZIPED_BACKUP_FILE=$2
    UNPACKED_BACKUP_FILE=$3

    echo "DROP DATABASE aginoodle" | \mysql -u root
    echo "CREATE DATABASE IF NOT EXISTS aginoodle CHARACTER SET=utf8;" | \mysql -u root
    cd $WORKSPACE/backups
    scp $BACKUP_LOCATION ./
    tar -xzf $GZIPED_BACKUP_FILE
    /usr/bin/mysql -u root aginoodle < $UNPACKED_BACKUP_FILE
    backlog migrate
    echo "from django.contrib.auth.models import User; User.objects.create_superuser(username='jarzyna', password='admin', email='krzysztof.jarzyna@szczecin.pl', id=0xDEAD)" | backlog shell > /dev/null
    echo "from backlog.items.models import PBItem, Tag; PBItem.objects.get(item_id='992.3').tags = Tag.objects.all()" | backlog shell > /dev/null
    echo "from datetime import timedelta; from django.contrib.sessions.models import Session; from django.utils import timezone; Session.objects.create(session_key='0xdeadbeef', session_data='ODNiOTQzMDZlNjNkMGI1NjE0OGJhNzE1MWVmYTVkMjVmOGVkNDZiZjp7ImJhY2tfbG9jYXRpb24iOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvdXNlci9sb2dpbi8/bmV4dD0vaXRlbXMvMTA3MDQvIiwiX2F1dGhfdXNlcl9pZCI6IjU3MDA1IiwiaGFzX3Blcm1fdG9fc2VlX3RlYW1fY2FwYWNpdHkiOlsiRlRLMSIsIkZUSzEwIiwiRlRLMTEiLCJGVEsxMiIsIkZUSzEzIiwiRlRLMTQiLCJGVEsxNSIsIkZUSzE2IiwiRlRLMiIsIkZUSzMiLCJGVEs0IiwiRlRLNSIsIkZUSzYiLCJGVEs3IiwiRlRLOCIsIkZUSzkiLCJGVFcxIiwiRlRXMTAiLCJGVFcxMSIsIkZUVzEyIiwiRlRXMTMiLCJGVFcxNCIsIkZUVzE1IiwiRlRXMTYiLCJGVFcxNyIsIkZUVzE4IiwiRlRXMTkiLCJGVFcyIiwiRlRXMjAiLCJGVFcyMSIsIkZUVzIyIiwiRlRXMyIsIkZUVzQiLCJGVFc1IiwiRlRXNiIsIkZUVzciLCJGVFc4IiwiRlRXOSIsIkZUVzI5IiwiRlRXMzAiLCJGVFczMSIsIkZUVzMyIiwiRlRXMzMiLCJGVFczNCIsIkZUSzU2IiwiRlRXMzciLCJGVEsxOCIsIkZUSzE3IiwiRlRLMTkiLCJGVFczNSIsIkZUU0gxMCIsIkZUSzIzIiwiRlRLMjQiXSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Yzc5ODgwNjA3YmU5NzViZGNkNDY3NjZhYzQ4NmNjMzZlOWNhYTczIn0=', expire_date=timezone.now() + timedelta(days=30))" | backlog shell > /dev/null
    echo "from backlog.aginoodle_shared.models import Attachment; Attachment.objects.all()" | backlog shell
    BACKUP_TIME=$(stat -c %y $UNPACKED_BACKUP_FILE)
    echo "Got backup from: $BACKUP_TIME"
    rm $UNPACKED_BACKUP_FILE
    cd - > /dev/null
}

function getltebackup() {
    getagibackup $LTE_AGINOODLE_BACKUP_LOCATION $LTE_AGINOODLE_GZIPED_BACKUP_FILE $LTE_AGINOODLE_UNPACKED_BACKUP_FILE
}

function getk3backup() {
    getagibackup $K3_AGINOODLE_BACKUP_LOCATION $K3_AGINOODLE_GZIPED_BACKUP_FILE $K3_AGINOODLE_UNPACKED_BACKUP_FILE
}

function getteamcalbackup() {
    DB_NAME=$1
    DB_USER=$2
    DB_PASS=$3

    cd $WORKSPACE/backups
    ssh glonull "mysqldump -u $DB_USER --password=$DB_PASS $DB_NAME > /tmp/teamcal_backup.sql"
    scp glonull:/tmp/teamcal_backup.sql ./
    /usr/bin/mysql -u root $DB_NAME < teamcal_backup.sql
    BACKUP_TIME=$(stat -c %y teamcal_backup.sql)
    echo "Got backup from: $BACKUP_TIME"
    ssh glonull "rm /tmp/teamcal_backup.sql"
    cd - > /dev/null
}

function getwrocteamcalbackup() {
    getteamcalbackup $WROC_TEAMCAL_DB_NAME $WROC_TEAMCAL_USER $WROC_TEAMCAL_PASSWORD
}

function getkrkteamcalbackup() {
    getteamcalbackup $KRK_TEAMCAL_DB_NAME $KRK_TEAMCAL_USER $KRK_TEAMCAL_PASSWORD
}

# completition in bin/backlog - requires Oh-My-ZSH
source $(dirname $0)/aginoodle.plugin.zsh
compdef _managepy backlog
