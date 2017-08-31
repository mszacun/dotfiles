export WORKSPACE=$HOME/aginoodle
export FT=$WORKSPACE/src/backlog/tests/feature_tests/
export MT=$WORKSPACE/src/backlog/tests/module_tests/
export UT=$WORKSPACE/src/backlog/tests/unit_tests/

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
alias shell="$WORKSPACE/bin/backlog shell_plus --bpython"
alias mysql='mycli'
alias stelle='(cd $WORKSPACE; ../AginoodleStelle/stelle_run.py)'
alias cooker='(cd ~/noodlecooker; bin/python bin/requester.py ~/aginoodle feature_tests)'
alias glonull='ssh glonull'
alias teamcal='(cd $HOME/teamcal; php56 -S localhost:5000 -t .)'

function t() {
    if [ $# -eq 1 ]; then
        (cd $WORKSPACE; PATH=$HOME/firefox:$PATH http_proxy= https_proxy= script -c "bin/py.test --reuse-db $1" /tmp/tests.log)
    else
        (cd $WORKSPACE; PATH=$HOME/firefox:$PATH http_proxy= https_proxy= script -c "bin/py.test --create-db $1" /tmp/tests.log)
    fi
}

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
    echo "from datetime import timedelta; from django.contrib.sessions.models import Session; from django.utils import timezone; Session.objects.create(session_key='0xdeadbeef', session_data='MmMxZjdkZDI3ZDBhYmRkN2E4YTI2ZmNhMDZiNTUyMzdkY2U3ZTVmMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjNiMzg3ZDkzM2NmNmQ1MjJlYzllN2Y1ZTJmMzg3ZmQ0MGExOGZmODIiLCJfYXV0aF91c2VyX2lkIjoiNTcwMDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImhhc19wZXJtX3RvX3NlZV90ZWFtX2NhcGFjaXR5IjpbIkZUSzEiLCJGVEsxMCIsIkZUSzExIiwiRlRLMTIiLCJGVEsxMyIsIkZUSzE0IiwiRlRLMTUiLCJGVEsxNiIsIkZUSzIiLCJGVEszIiwiRlRLNCIsIkZUSzUiLCJGVEs2IiwiRlRLNyIsIkZUSzgiLCJGVEs5IiwiRlRXMSIsIkZUVzEwIiwiRlRXMTEiLCJGVFcxMiIsIkZUVzEzIiwiRlRXMTQiLCJGVFcxNSIsIkZUVzE2IiwiRlRXMTciLCJGVFcxOCIsIkZUVzE5IiwiRlRXMiIsIkZUVzIwIiwiRlRXMjEiLCJGVFcyMiIsIkZUVzI5IiwiRlRXMyIsIkZUVzMwIiwiRlRXMzEiLCJGVFczMiIsIkZUVzQiLCJGVFc1IiwiRlRXNiIsIkZUVzciLCJGVFc4IiwiRlRXOSJdfQ==', expire_date=timezone.now() + timedelta(days=30))" | backlog shell > /dev/null
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
compdef _managepy backlog
