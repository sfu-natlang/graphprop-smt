import sys, cPickle
filename=sys.argv[1]
in_file=open(filename)
def pickle():
    out_file=open(filename+'.pickle', 'wb')
    for line in in_file:
        phr, dp=line.strip().split('\t')
        dp=eval(dp)
        cPickle.dump((phr, dp), out_file, -1)
    out_file.close()

def unPickle():
    while True:
        try:
            phr, dp = cPickle.load(in_file)
            print '%s\t%s'%(phr, dp)
        except:
            print 'EOF'
            break

if __name__=='__main__':
    pickle()    
