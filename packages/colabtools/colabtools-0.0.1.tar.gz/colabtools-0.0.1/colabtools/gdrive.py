def list_files_for_path(pad=None, silent=True):
  import fnmatch
  head, tail = os.path.split(pad)
  if not silent:
    print(f"head={head}, tail='{tail}'")
  if head == None or head == '/':
    file_list = drive.ListFile({'q': "'root' in parents  and trashed=false"}).GetList()
  else:
    if not silent:
      print(f"Recursing down started {head}")
    file_list = list_files_for_path(head)
    assert len(file_list) == 1
    
    id = file_list[0]["id"]
    
    if not silent:
      print(f"Recursing down using id {id}")
    
    file_list = drive.ListFile({'q': f"'{id}' in parents  and trashed=false"}).GetList()
    if not silent:
    
      print(file_list)
      print(f"Recursing down results finished {head}")
    
  if not silent:
    for file1 in file_list:
      print('title: %s, id: %s, mime: %s' % (file1['title'], file1['id'], file1['mimeType']))  
  
  if tail == None or tail == '':
    tail = '*'
  return [f for f in file_list if fnmatch.fnmatch(f['title'], tail)]
