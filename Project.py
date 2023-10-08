import os
import shutil
import time
import hashlib

def sync_folders(source_folder_path, replica_folder_path, log_file_path, sync_interval=60):
  """Synchronizes two folders: source and replica.

  Args:
    source_folder_path: The path to the source folder.
    replica_folder_path: The path to the replica folder.
    log_file_path: The path to the log file.
    sync_interval: The synchronization interval in seconds.
  """

  # Create the log file if it does not exist.
  if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as f:
      f.write("Sync log:\n")

  # Get the list of files and directories in the source folder.
  source_files = os.listdir(source_folder_path)

  # Iterate over the files and directories in the source folder.
  for file in source_files:
    source_file_path = os.path.join(source_folder_path, file)
    replica_file_path = os.path.join(replica_folder_path, file)

    # If the file does not exist in the replica folder, copy it from the
    # source folder.
    if not os.path.exists(replica_file_path):
      shutil.copy(source_file_path, replica_folder_path)
      log_message = f"Copied file '{file}' from source to replica.\n"
      write_log(log_message, log_file_path)
      print(log_message)

    # If the file is a directory, recursively synchronize the directory contents.
    elif os.path.isdir(source_file_path):
      sync_folders(source_file_path, replica_file_path, log_file_path)

    # If the file exists in both folders, compare the file sizes and MD5
    # hashes. If the file sizes or MD5 hashes are different, copy the file
    # from the source folder to the replica folder.
    else:
      source_file_size = os.path.getsize(source_file_path)
      replica_file_size = os.path.getsize(replica_file_path)

      source_file_md5_hash = hashlib.md5(open(source_file_path, "rb").read()).hexdigest()
      replica_file_md5_hash = hashlib.md5(open(replica_file_path, "rb").read()).hexdigest()

      if source_file_size != replica_file_size or source_file_md5_hash != replica_file_md5_hash:
        shutil.copy(source_file_path, replica_folder_path)
        log_message = f"Copied file '{file}' from source to replica because the file sizes or MD5 hashes were different.\n"
        write_log(log_message, log_file_path)
        print(log_message)

  # Schedule the next synchronization.
  time.sleep(sync_interval)
  sync_folders(source_folder_path, replica_folder_path, log_file_path, sync_interval)

def write_log(message, log_file_path):
  """Writes a message to the log file.

  Args:
    message: The message to write to the log file.
    log_file_path: The path to the log file.
  """

  with open(log_file_path, "a") as f:
    f.write(message)

if __name__ == "__main__":
  # Get the folder paths and synchronization interval from the command line
  # arguments.
  source_folder_path = sys.argv[1]
  replica_folder_path = sys.argv[2]
  log_file_path = sys.argv[3]

  # Synchronize the folders.
  sync_folders(source_folder_path, replica_folder_path, log_file_path)
