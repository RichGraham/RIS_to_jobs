tell application "Finder" to set _dir to insertion location as alias

tell application "Terminal"
	activate
	do script "cd " & (quoted form of (POSIX path of _dir)) & "; conda activate ris; Pass2_Check_Roles.py Pro*.xlsx"
end tell