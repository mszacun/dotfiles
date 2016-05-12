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
alias jt='(cd $WORKSPACE/src/backlog/; ../../bin/jasmine-ci)'
alias jasmine='(cd $WORKSPACE/src/backlog/; ../../bin/jasmine)'
alias at='runall'
alias backlog="$WORKSPACE/bin/backlog"
alias shell="$WORKSPACE/bin/backlog shell_plus --bpython"
alias mysql='mycli'
alias stelle='(cd $WORKSPACE; ../AginoodleStelle/stelle_run.py)'
alias glonull='ssh glonull'
alias teamcal='(cd $HOME/teamcal; php -S localhost:5000 -t .)'

function t() {
    (cd $WORKSPACE; script -c "bin/py.test --reuse-db $1" /tmp/tests.log)
}

function show_tests() {
    grep "def test" $1 | sort | grep "test"
}

function runall() {
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

    tmux send-keys -t:.2 stelle
    tmux send-keys -t:.2 Enter

    tmux send-keys -t:.3 jt
    tmux send-keys -t:.3 Enter
}

# completition in bin/backlog - requires Oh-My-ZSH
compdef _managepy backlog
