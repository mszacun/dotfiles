#PROMPT="%{$fg_bold[yellow]%}%n@%m:%{$fg_bold[blue]%}%~ %{$fg_bold[red]%}[ %* ]%{$reset_color%} $(git_prompt_info) $ "
#PROMPT='%{$fg_bold[yellow]%}%n@%m:%{$fg_bold[blue]%}%~ %{$fg[red]%}[ %* ] %{$fg_bold[blue]%}$(git_prompt_info)%{$fg_bold[blue]%} % %{$reset_color%}'
PROMPT='%{$fg_bold[yellow]%}%n@%m:%{$fg_bold[blue]%}%~ %{$fg[red]%}[ %* ]%{$reset_color%}$(git_prompt_info) $ '

ZSH_THEME_GIT_PROMPT_PREFIX=" ("
ZSH_THEME_GIT_PROMPT_SUFFIX=")%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[red]%}*%{$fg[green]%}"
ZSH_THEME_GIT_PROMPT_CLEAN=""
