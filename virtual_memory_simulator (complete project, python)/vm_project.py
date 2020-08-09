import vm_classes

# ANDRES OWENS // 58449528 // ADOWENS@UCI.EDU // CS143B

def open_file(f = None):
    #done
    #FILE PATH TO INITIALIZE THE VM
    file = open('/Users/andresowens/Documents/CS143B/project2/initFile-7.txt')
#    file = open('/Users/andresowens/Documents/CS143B/project2/01.txt')

    #FILE PATH TO VA'S 2 BE TRANSLATED
    file2 = open('/Users/andresowens/Documents/CS143B/project2/opFile-7.txt')

    a = list(map(lambda x: int(x),  file.readline().split()))
    b = list(map(lambda x: int(x),  file.readline().split()))
    c = list(map(lambda x: int(x), file2.readline().split()))
    return a, b, c

def translate_with_TLB(line1, line2, line3):
    #done
    TLB = vm_classes.TranslationLookAsideBuffer()
    VM = vm_classes.VirtualMemory()
    VM.initialize_vm(line1,line2)
    answer = ''
    
    for seg, va in zip(line3[0::2], line3[1::2]):
        t, va_decomp = seg, "{0:032b}".format(va)
        sp = int(va_decomp[4:23], 2)
        s, p, w = int(va_decomp[4:13],2), int(va_decomp[13:23],2), int(va_decomp[23:],2)
        temp_trans_table = TLB.locate_sp(sp)
                
        if(temp_trans_table <= 0):
            current = VM.translate(t, s, p, w)
            if(current != 'pf' and current != 'err'):
                f = VM.PM[s].page_value(p)
                TLB.add_value(sp, f)
                answer += " " + 'm ' + current 

            else:
                answer += " " + 'm ' + current
        else:
            answer += " " + "h " + str(int(temp_trans_table) + w)
    return answer

def translate_without_TLB(line1, line2, line3):
    #done
    VM = vm_classes.VirtualMemory()
    VM.initialize_vm(line1,line2)
    answer = ''
    
    for seg, va in zip(line3[0::2], line3[1::2]):
        t, va_decomp = seg, "{0:032b}".format(va)
        s, p, w = int(va_decomp[4:13],2), int(va_decomp[13:23],2), int(va_decomp[23:],2)
        answer += " " + VM.translate(t, s, p, w)
    return answer

def write_to_file(result, filepath):
    #done
    f = open(filepath,'w')
    #DOUBLE CHECK [1:] METHOD OF GETTING RID OF INITIAL SPACE!!!
    f.write(result[1:])
    f.close()

line1, line2, line3 = open_file()
#print(translate_without_TLB(line1,line2,line3))
#print(translate_with_TLB(   line1, line2, line3))

write_to_file(translate_without_TLB(line1,line2,line3),'/Users/andresowens/Documents/CS143B/project2/584495281.txt')
write_to_file(translate_with_TLB(line1, line2, line3), '/Users/andresowens/Documents/CS143B/project2/584495282.txt')