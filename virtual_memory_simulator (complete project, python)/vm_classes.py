from bitarray import bitarray

# ANDRES OWENS // 58449528 // ADOWENS@UCI.EDU // CS143B

class VirtualMemory:
    def __init__(self):
        #done
        self.bitmap = bitarray(1024)
        self.bitmap.setall(0)
        self.bitmap[0] =  1
        self.frames = 1024
        self.size   = 512
        self.PM = [0 for i in range(1024 * 512)]

    def read(self, s, p, w):
        #done
        if(self.PM[s] == 0):
            return "err"
        elif(self.PM[s] == -1):
            return "pf"
        elif(self.PM[s].page_value(p) == -1):
            return "pf"
        elif(self.PM[s].page_value(p) == 0):
            return "err"
        else:
            return self.PM[s].page_value(p) + w                                        

    def write(self, s, p, w):
        #done
        if(self.PM[s] == 0):
            new_frame = None
            for i in range(1, self.frames - 1):
                if (self.bitmap[i] == 0 and self.bitmap[i+1] == 0):
                    self.bitmap[i] = 1
                    new_frame = i * 512
                    self.bitmap[i+1] = 1
                    break
            if(new_frame):   
                self.PM[s] = PageTable(new_frame)
                return self.PM[s].page_value(p) + w
            
        elif(self.PM[s] == -1 or self.PM[s].page_value(p) == -1):
            return "pf"
        
        elif(self.PM[s].page_value(p) == 0):
            new_frame = None
            for i in range(1, self.frames - 1):
                if (self.bitmap[i] == 0):
                    new_frame = i * 512
                    self.bitmap[i] = 1
                    #self.bitmap[i+1] = 1
                    break
            if(new_frame):    
                self.PM[s].add_page(p, new_frame)
                return self.PM[s].page_value(p) + w
            
        #POSSIBLE ELIF CASE @ END OF FILe
        
        else:
            return self.PM[s].page_value(p) + w
        
    def translate(self, t, s, p, w):
        #done
        if(not t):
            return str(self.read(s,p,w))
        else:
            return str(self.write(s,p,w))
    
    def initialize_vm(self, line1,line2):
        #done
        for seg, va in zip(line1[0::2], line1[1::2]):
            if(va == -1):
                self.PM[seg] = -1
            elif(va not in range(512)):
                self.PM[seg] = PageTable(va)
                self.bitmap[int(va/512)] = 1
                self.bitmap[int(va/512)+1] = 1
                
        for si, seg, va in zip(line2[0::3], line2[1::3],line2[2::3]):
            if(va > 0):
                self.bitmap[int(va/512)] = 1
            if(isinstance(self.PM[seg], PageTable)):
                self.PM[seg].add_page(si, va)

class TranslationLookAsideBuffer:
    def __init__(self):
        #done
        self.TLB = [{'LRU': 0, 'sp': None, 'f':0},
                    {'LRU': 0, 'sp': None, 'f':0},
                    {'LRU': 0, 'sp': None, 'f':0},
                    {'LRU': 0, 'sp': None, 'f':0}]      
    
    def locate_sp(self, sp):
        #done
        for x in range(4):
            if (self.TLB[x]['sp'] == sp):
                for y in range(4):
                    if(self.TLB[x]['LRU'] < self.TLB[y]['LRU']):
                        self.TLB[y]['LRU'] -= 1
                
                self.TLB[x]['LRU'] = 3
                return self.TLB[x]['f']
        return False
    
    def add_value(self, sp, f):
        #done
        for x in range(4):
            if (self.TLB[x]['LRU'] == 0):
                self.TLB[x]['LRU']  = 3
                self.TLB[x]['f']    = f
                self.TLB[x]['sp']   = sp
                
                for y in range(4):
                    if(x != y and self.TLB[y]['LRU'] != 0):
                        self.TLB[y]['LRU'] -= 1 
                return 1     
        return 0
    
class PageTable:
    def __init__(self, start = None):
        #done
        self.pm_index = start
        self.pages = [0 for x in range(2048)]
#        self.bm1 = int(start/512) 
#        self.bm2 = int(start/512) + 1
    
    def add_page(self, page, value):
        #done
        self.pages[page] = value
        
    def page_value(self, page):
        #done
        return self.pages[page]