clear
echo "Installing/Updating Library..."
python3 -m pip install --break-system-packages -r requirements.txt -U
echo "Library Updated... Starting Bot..."
python bootstrap.py