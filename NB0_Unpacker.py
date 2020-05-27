import struct
import sys
import os

CHUNK_SIZE = 1024 * 1024

def files_information(nb0_file_object, files_count):
    file_info = []
    for i in range(0, files_count):
        file_info.append(struct.unpack("IIII48s", nb0_file_object.read(0x40)))

    real_offset = nb0_file_object.tell()
    return file_info, real_offset

def unpack_file(file_detail, output_path, nb0_file_object, real_offset):
    new_file = open(os.path.join(output_path, file_detail[4].replace("\x00", "")), "wb")
    counter = 0
    
    nb0_file_object.seek(real_offset + file_detail[0])

    while counter != file_detail[1]:
        if file_detail[1] - counter > CHUNK_SIZE:
            new_file.write(nb0_file_object.read(CHUNK_SIZE))
            counter += CHUNK_SIZE
        else:
            new_file.write(nb0_file_object.read(file_detail[1] - counter))
            counter += file_detail[1] - counter
    
    new_file.close()

if len(sys.argv) >= 3:
    try:
        nb0_file = open(sys.argv[2], "rb")
    except:
        print "File not found, can't do anything :("
        exit()

    files_count = struct.unpack("I", nb0_file.read(4))[0]
    files_info, real_offset = files_information(nb0_file, files_count)

    if sys.argv[1] == "-l":
        print "Files Count : %i" % (files_count)
        for f in files_info:
            print "Offset : 0x%08X\tSize : 0x%08X\tFilename : %s" % (f[0] + real_offset, f[1], f[4])
    elif sys.argv[1] == "-u":
        print "Unpacking to %s" % (sys.argv[3])
        if not os.path.exists(sys.argv[3]):
            os.mkdir(sys.argv[3])

        for f in files_info:
            print "Unpacking %s" % f[4]
            unpack_file(f, sys.argv[3], nb0_file, real_offset)
    nb0_file.close()
else:
    print "Uses : %s -l <Filename>" % sys.argv[0]
    print "Uses : %s -u <Filename> <OutputDir>" % sys.argv[0]
