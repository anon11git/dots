import os
import sqlite3
from iphone_backup_decrypt import EncryptedBackup

# --- Update these paths! ---
BACKUP_DIR = os.path.expanduser("")
OUTPUT_DIR = os.path.expanduser("~/ios_extracted_decrypted")
PASSPHRASE = ""

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Decrypting keybag and manifest...")
backup = EncryptedBackup(backup_directory=BACKUP_DIR, passphrase=PASSPHRASE)

# 1. Save the decrypted manifest so we can read from it
manifest_path = os.path.join(OUTPUT_DIR, "_Decrypted_Manifest.db")
if not os.path.exists(manifest_path):
    print("Saving decrypted Manifest.db...")
    backup.save_manifest_file(manifest_path)

# 2. Get a list of all unique Domains (e.g., AppDomain-WhatsApp, CameraRollDomain)
conn = sqlite3.connect(manifest_path)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT domain FROM Files WHERE domain IS NOT NULL AND domain != ''")
domains = [row[0] for row in cursor.fetchall()]
conn.close()

print(f"Found {len(domains)} unique domains. Organizing folders...")

# 3. Extract each domain into its own cleanly separated folder
for idx, domain in enumerate(domains, start=1):
    # Create the specific folder for this domain
    domain_dir = os.path.join(OUTPUT_DIR, domain)
    os.makedirs(domain_dir, exist_ok=True)
    
    print(f"[{idx}/{len(domains)}] Extracting: {domain}")
    try:
        # Use the plural method that we know works.
        # Because we point output_folder to the specific domain_dir, 
        # it neatly reconstructs the internal paths (Library, Documents, etc.) inside it!
        backup.extract_files(domain_like=domain, output_folder=domain_dir)
        
    except Exception as e:
        print(f"  -> Skipped {domain} (Error: {e})")

print(f"\nSuccess! All files extracted and cleanly organized by Domain in {OUTPUT_DIR}")
