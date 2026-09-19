set -g fish_greeting
alias l='ls -lha --color=always'
fish_add_path "$HOME/.local/bin"
if test (tty) = "/dev/tty1"
	exec start-hyprland && exit 0
end
if status is-interactive
end