import os
import json

root_dir = 'img'
for dir_name, subdir_list, file_list in os.walk(root_dir):
    li = [x for x in file_list]
print(len(li))
i = 0
o = {}
file_no = 1
j = 0
arr = []
for i in range(len(li)):
    if len(arr) < 10:
        arr.append(root_dir + '/' + li[i]);
    else:
        with open(str(file_no) + '.json', 'w') as f:
            f.write(json.dumps(arr))
        file_no += 1
        arr.clear()
with open(str(file_no) + '.json', 'w') as f:
    f.write(json.dumps(arr))
