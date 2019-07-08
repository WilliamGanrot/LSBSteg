from PIL import Image 
import sys

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def char2bi(msg):
    return ' '.join(format(ord(x), '08b') for x in msg)

def decode(img):
    msg = ''
    p = 0

    imgdata = list(img.getdata())
    imgdata = [val for sublist in imgdata for val in sublist]
     
    for i, bit in enumerate(imgdata):
        x = imgdata[p:p+9]
        letter = x[0:8]
        letter = [(value % 2) for value in letter]
        letter = ''.join(str(e) for e in letter)

        msg += text_from_bits(letter)
        if x[8] % 2 == 1:
            break
        p += 9

    print(msg)

def encode(img, msg):
    data = [char2bi(value) for value in msg]
    data = [int(val) for sublist in data for val in sublist]
    data = [data[i:i+8] for i in range(0, len(data), 8)]

    imgdata = list(img.getdata())
    editp = imgdata[:(len(data)*3)]
    editp = [val for sublist in editp for val in sublist]
    editp = [editp[i:i+9] for i in range(0, len(editp), 9)]

    for i in enumerate(data):
        for j in enumerate(data[i[0]]): 
            if editp[i[0]][j[0]] % 2 != data[i[0]][j[0]]:
                editp[i[0]][j[0]] -= 1     
        if editp[i[0]][8] % 2 == 1:
            editp[i[0]][8] -= 1
        
        if i[0] == (len(data) - 1) and editp[i[0]][8] % 2 == 0:
            editp[i[0]][8] -= 1

    editp = [val for sublist in editp for val in sublist]
    editp = list(zip(*[iter(editp)]*3)) 

    for i, pixel in enumerate(editp):
        imgdata[i] = pixel
    
    newimg = Image.new(img.mode, img.size)
    newimg.putdata(imgdata)
    newimg.save(img.filename[:-4] + '_out.png')
    
def main():
    if sys.argv[1] == 'encode':
        try:
            if sys.argv[2][-4:].lower() == '.png':
                img = Image.open(sys.argv[2], 'r')
            else: 
                print("You can only encode and decode PNG's")
        except:
            print('Invalid filename')
        msg = input('Data to hide in image ')
        if len(msg) > 0:
            encode(img, msg)
        else:
            print('You need to supply a message to encode')
        
    elif sys.argv[1] == 'decode':
        try:
            img = Image.open(sys.argv[2], 'r')
        except:
            print('Invalid filename')
        decode(img)
    else:
        print('Invalid option. You either need to encode or decode')

if __name__ == '__main__':
    main()