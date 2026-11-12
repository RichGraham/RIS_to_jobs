tell application "Finder" to set _dir to insertion location as alias

tell application "Terminal"
	activate
	do script "cd " & (quoted form of (POSIX path of _dir)) & "; conda activate ris; Pass3_Check_Titles.py Project*.xlsx"
end tell