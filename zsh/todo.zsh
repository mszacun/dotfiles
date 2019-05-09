GLOBAL_TODO_DIR="$HOME/.todo/"

alias t="TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper"
alias ta="TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper -t add"
alias taa="TODOTXT_PRIORITY_ON_ADD=A TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper -t add"
alias tab="TODOTXT_PRIORITY_ON_ADD=B TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper -t add"
alias tac="TODOTXT_PRIORITY_ON_ADD=C TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper -t add"
alias tad="TODOTXT_PRIORITY_ON_ADD=D TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper -t add"
alias tae="TODOTXT_PRIORITY_ON_ADD=E TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper -t add"
alias tl="TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper ls"
alias tdo="TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper do"
alias tp="TODO_DIR=$GLOBAL_TODO_DIR todo-git-wrapper p"


alias lt="TODO_DIR=./todo/ todo.sh -t"
alias lta="TODO_DIR=./todo/ todo.sh -t add"
alias ltl="TODO_DIR=./todo/ todo.sh ls"
alias ltdo="TODO_DIR=./todo/ todo.sh do"
alias ltp="TODO_DIR=./todo/ todo.sh p"
