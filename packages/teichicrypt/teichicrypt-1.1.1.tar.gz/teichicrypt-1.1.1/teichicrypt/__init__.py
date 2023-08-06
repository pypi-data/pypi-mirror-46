"""Custom crypting module for python
This module provides a custom, self created cryting mechanism, which is not (intentionally) based on any other crypting algorithm.
"""
name = "teichicrypt"
from mpmath import *
from secrets import choice
import os
if __name__ == "__main__":
    from tkinter import filedialog
    from tkinter import messagebox as mb
    from tkinter import *
    from tkinter.ttk import Progressbar

key_size=26
cluster_size = 100
mp.dps = cluster_size * 1.5
rotate_list_inside_ = [0,2,4,6,8,9,7,5,3,1]
rotate_list_outside_ = [6,8,9,5,1,3,4,2,0,7]

keys_list=[sqrt(11),sqrt(7),sqrt(5),sqrt(6),sqrt(8),sqrt(3),sqrt(10),sqrt(12),sqrt(2),sqrt(13)]

letters = [b'\xc1', b'\x91', b'\xed', b';', b'\xf2', b'Y', b'\xc8', b'\x16', b'\x8b', b'\xd3', b'\xd4', b'\x92', b'3', b'\x89', b'N', b'\xae', b'\x86', b'R', b'\xa7', b'v', b'\xa3', b'G', b'\x08', b'\xa5', b'\x7f', b'\x9d', b'E', b'<', b'\x98', b'\xc3', b'I', b'\xc7', b'\xac', b'w', b'W', b'\xbf', b'\xa8', b'\x9e', b'\x96', b'e', b'\xb7', b'\xa6', b'\x99', b'k', b'\xfb', b'Z', b'\xf8', b'\x02', b'r', b'L', b'\x9b', b'f', b'U', b'\xc0', b'\xb0', b'\x9c', b'\x0e', b'\xf5', b'?', b'\xc9', b'M', b'\xc5', b'\x8f', b'\xba', b'\x06', b'\xeb', b'\xfd', b"'", b'n', b'\x05', b'`', b'\x0c', b'/', b'\x93', b'\xe1', b'\xcc', b'\x82', b'\x83', b'C', b'\xdd', b'\xde', b'*', b'X', b'"', b'6', b'y', b'm', b'V', b'\xaf', b'\xd2', b'\xf0', b'\x04', b'%', b'\xdb', b'\xb8', b'\xd9', b'\x0b', b'+', b'\xb6', b'#', b'\x01', b'&', b'\xfc', b'\x8a', b'\xd6', b'9', b'\x85', b'\xf3', b'\xa1', b'\x03', b'4', b'7', b'\x11', b'\x9a', b'\xbc', b'\x00', b'\xa0', b'o', b'-', b'j', b'\x1d', b'\xb4', b'\xfa', b'}', b'u', b'\xec', b'\xe0', b'\xad', b'l', b's', b'\xbd', b'@', b'i', b'\xa2', b'\xf9', b'\xe3', b'Q', b'\xd8', b'\xb5', b'b', b'\xef', b'\xea', b'\xfe', b'\x1b', b'\x90', b'\xb3', b'H', b'\x94', b'g', b'\xcd', b'$', b'\xb2', b'P', b'\xca', b'\xbe', b',', b'\xc2', b'\x18', b'T', b'\xe2', b'x', b'\xd0', b'\xe5', b'\xc6', b'\xcf', b' ', b'B', b'z', b'\xa9', b'5', b'c', b'1', b'\x17', b'\xcb', b'\x8e', b'K', b'\x1f', b'\x1c', b'\x80', b'\x84', b'[', b'\xff', b'\\', b'q', b'^', b')', b'\x88', b'p', b'\xab', b'\x12', b'\x0f', b'\xe4', b'\xd7', b'\t', b'\xce', b'\x1a', b'\x8d', b'\x15', b'\xee', b'.', b'\xd1', b'\xe8', b'\xb1', b'\x87', b'!', b'\x07', b'\xc4', b'\xe9', b'\xa4', b'\xdc', b'\n', b'\x95', b'\x10', b'\xd5', b'\xdf', b'O', b't', b'\xda', b'_', b'=', b']', b'\xbb', b'h', b'\xf4', b'\r', b'~', b'0', b'>', b'\x19', b'\x13', b'd', b'\xaa', b'|', b'\xb9', b'(', b'\xf1', b'\xf6', b'a', b'2', b'\x8c', b'{', b'D', b'S', b'\x14', b'A', b'\x81', b'F', b'\x97', b'\xe6', b'J', b'8', b'\x1e', b'\xe7', b':', b'\x9f', b'\xf7']
values = []
for i in range(len(letters)):
    values.append(i)

key_max=""
for i in range(key_size):
    key_max += "9"
key_max=int(key_max)

def _invert(d):
    """internal function"""
    return {v:k for k,v in d.items()}

letters_dict = {letters[i]: values[i] for i in range(len(letters))}
values_dict = _invert(letters_dict)

def _rotate(l, n):
    """internal function"""
    return l[-n:] + l[:-n]

def _sum_d(n):
    """internal function"""
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r

def calc_key(key_list, key_in, count):
    """calculate usable key for the other functions
    
    key_list is a list containing the positions of the key separately. ([1,2,3,4,...])
    key_in is a string or integer, which is the key ("12345...")
    count is the current cluster number for which the key should be calculated
    """
    count_ = count % cluster_size
    if _sum_d(int(key_in)) % 2 == 0:
        p1 = int(str(mpf(mpf(keys_list[0])-int(keys_list[0])))[2:][count_])
        p2 = int(str(mpf(mpf(keys_list[1])-int(keys_list[1])))[2:][count_])
        p3 = int(str(mpf(mpf(keys_list[2])-int(keys_list[2])))[2:][count_])
        p4 = int(str(mpf(mpf(keys_list[3])-int(keys_list[3])))[2:][count_])
    else:
        p1 = int(str(mpf(mpf(keys_list[-4])-int(keys_list[-4])))[2:][count_])
        p2 = int(str(mpf(mpf(keys_list[-3])-int(keys_list[-3])))[2:][count_])
        p3 = int(str(mpf(mpf(keys_list[-2])-int(keys_list[-2])))[2:][count_])
        p4 = int(str(mpf(mpf(keys_list[-1])-int(keys_list[-1])))[2:][count_])
    
    key=mpf(abs(((((key_list[0]+key_list[1])/(p1+1))*((key_list[2]-key_list[3]+key_list[5])/(key_list[4]+p2+1))/((((key_list[8])/(1+key_list[9]))/((2)))+key_list[6])+((p3+((p2)/(p1+1)))/(2+key_list[7]))+1)+((key_list[10]+key_list[11]-key_list[12]-key_list[13])/(p4+key_list[14]+1))-((key_list[11])/(key_list[8]+1))-key_list[15]+((key_list[16])/(p1+1))-((key_list[17])/(key_list[18]+key_list[0]+1))-key_list[19]+((key_list[20]*key_list[21])/(key_list[22]+1))-key_list[23])/((key_list[24]+key_list[25])/(key_list[24]+key_list[25]+1))))
    key_calc_=[]
    key_calc=[]
    for x in str(key):
        key_calc_.append(x)
    for x in key_calc_[key_calc_.index(".")+1:]:
        key_calc.append(int(x))
    return key_calc

def step_1(string_in_before, key_calc, count=0, encrypt=True):
    """Step 1 of the crypting alogrithm.
    
    Has to be called for every cluster separately.
    string_in_before should be the whole list with all clusters included. ([cluster1,cluster2,...])
    key_calc is the return value of calc_key for the curent cluster number
    to decrypt set encrypt to False
    """
    string_in=string_in_before[count]
    string_out=[]
    if encrypt:
        z=0
        for a in string_in:
            x = int.to_bytes(a, 1, 'little')
            zahl = key_calc[z]
            if (0 <= zahl) & (zahl <= 2):
                string_out.append([x])
            elif (2 < zahl) & (zahl <= 6):
                zu = choice(values[:letters.index(x)+1])
                zu1 = values[letters.index(x)]-zu
                string_out.append([letters[zu], letters[zu1]])
            else:
                zu1 = choice(values[:letters.index(x)+1])
                zu2 = choice(values[:letters.index(x)-zu1+1])
                zu3 = values[letters.index(x)]-(zu1+zu2)
                string_out.append([letters[zu1], letters[zu2], letters[zu3]])
            z+=1
            _update_progressbar()
    else:
        try:
            string_out_ = []
            for x in range(len(string_in)):
                wert_current = 0
                for bruchteil in string_in[x]:
                    wert_current += letters_dict[bruchteil]
                string_out.append(values_dict[wert_current])
                _update_progressbar()
        except:
            pass
    return string_out

def step_2(string_in_before, key_calc, count=0, encrypt=True):
    """Step 2 of the crypting algorithm
    
    See step_1
    """
    string_in = string_in_before[count]
    string_out=[]
    if encrypt:
        rotate_list_outside = rotate_list_outside_.copy()
        rotate_list_inside = rotate_list_inside_.copy()
        for zeichen_stelle in range(len(string_in)):
            vf=rotate_list_outside[rotate_list_inside.index(key_calc[zeichen_stelle])]
            for zeichen_teil in string_in[zeichen_stelle]:
                try:
                    string_out.append(values_dict[letters_dict[zeichen_teil]+vf])
                except KeyError:
                    string_out.append(values_dict[letters_dict[zeichen_teil]+vf-len(letters)])
            rotate_list_outside=_rotate(rotate_list_outside, 1)
            _update_progressbar()
    else:
        rotate_list_outside = rotate_list_outside_.copy()
        rotate_list_inside = rotate_list_inside_.copy()
        string_in.reverse()
        rotate_list_outside=_rotate(rotate_list_outside, len(string_in)%10)
        
        for zeichen_stelle in range(len(string_in)):
            rotate_list_outside=_rotate(rotate_list_outside, -1)
            vf=rotate_list_outside[rotate_list_inside.index(key_calc[(len(string_in)-zeichen_stelle)-1])]
            buchstabe_cur = []
            for zeichen_teil in string_in[zeichen_stelle]:
                buchstabe_cur.append(letters[letters_dict[zeichen_teil]-vf])
            string_out.append(buchstabe_cur)
            _update_progressbar()
        
        string_out.reverse()
    
    return string_out

def step_3(string_in):
    """Step 3 of the crypting algorithm
    
    string_in is the complete list [a,b,c,d,...]
    """
    string_out = string_in
    string_out.reverse()
    return string_out

def step_4(string_in):
    """Step 4 of the crypting algorithm
    
    string_in is the complete list [a,b,c,d,...]
    """
    string_out=string_in
    for x in range(len(string_in)):
        if x % 2 == 0:
            try:
                string_out[x], string_out[x+1] = string_out[x+1], string_out[x]
            except IndexError:
                pass
        _update_progressbar()
        return string_out

def step_5(string_in, encrypt=True):
    """Step 5 of the crypting algorithm
    
    string_in is the complete list [a,b,c,d,...]
    to decrypt set encrypt to False
    """
    string_out=[]
    if encrypt:
        for x in range(len(string_in)):
            if (x+1) % 2 == 0:
                try:
                    string_out.append(letters[int(letters.index(string_in[x]))+1])
                except (ValueError, IndexError):
                    string_out.append(letters[int(letters.index(string_in[x]))+1-len(letters)])
            else:
                string_out.append(string_in[x])
            _update_progressbar()
    else:
        for x in range(len(string_in)):
            if (x+1) % 2 == 0:
                string_out.append(letters[int(letters.index(int.to_bytes(string_in[x][0], 1, 'little')))-1])
            else:
                string_out.append(int.to_bytes(string_in[x][0], 1, 'little'))
            _update_progressbar()
    return string_out

def step_6(string_in, encrypt=True):
    """Step 6 of the crypting algorithm
    
    string_in is the complete list [a,b,c,d,...]
    to decrypt set encrypt to False
    """
    if encrypt:
        string_out=string_in
        barrier = choice(letters[2:])
        barrierz=values[letters.index(barrier)]
        for x in range(barrierz):
            string_out.insert(0, choice(letters))
            string_out.append(choice(letters))
        string_out.append(barrier)
    else:
        barrier = values[letters.index(string_in[-1])]
        string_out = string_in[barrier:-(barrier+1)]
    return strin_out

def step_7(string_in, encrypt=True):
    """Step 7 of the crypting algorithm
    
    string_in is the complete list [a,b,c,d,...]
    to decrypt set encrypt to False
    """
    string_out=[]
    if encrypt:
        periode=choice(letters[2:])
        periodez=values[letters.index(periode)]
        for x in range(len(string_in)):
            string_out.append(string_out[x])
            if ((x+1) % (periodez-1)) == 0:
                string_out.append(choice(letters))
        string_out[0] = periode
    else:
        periode = values[letters.index(string_in[0])]
        for x in range(len(string_in)):
            if (x != 0) & ((x+1) % periode == 0):
                pass
            else:
                string_out.append(string_in[x])
    return string_out

def conversion(string_in, input_format, output_format, key=None, key_in=None):
    """Used for the conversion between the different formats for the different steps
    
    currently possible conversions:
    input                                    -> step_1, step_3, step_4, step_5, step_6 or step_7
    step_3, step_4, step_5, step_6 or step_7 -> step_2 or output
    step_2                                   -> step_3, step_4, step_5, step_6 or step_7
    step_1                                   -> output
    """
    
    if input_format == 'input':
        if output_format == 'step_1':
            n=cluster_size
            string_out=[string_in[i:i+n] for i in range(0, len(string_in), n)]
        elif output_format in ['step_3', 'step_4', 'step_5', 'step_6', 'step_7']:
            n=1
            string_out=[string_in[i:i+n] for i in range(0, len(string_in), n)]
    
    elif input_format in ['step_3', 'step_4', 'step_5', 'step_6', 'step_7']:
        string_in_copy = string_in
        if output_format == 'output':
            string_out=string_in
        elif output_format == 'step_2':
            string_out = []
            for count in range(int(len(string_in)/cluster_size)+1):
                try:
                    key_used = _calc_key(key, key_in, count)[:cluster_size]
                except:
                    break
                string_out.append([])
                for buchstabe in range(cluster_size):
                    key_buch = key_used[buchstabe]
                    stelle = count*cluster_size+buchstabe
                    try:
                        if 0 <= key_buch and key_buch <= 2:
                            string_out[count].append([string_in[stelle]])
                        elif 2 < key_buch and key_buch <= 6:
                            string_out[count].append([string_in[stelle],string_in[stelle+1]])
                            string_in.pop(stelle+1)
                        elif 6 < key_buch and key_buch <= 9:
                            string_out[count].append([string_in[stelle],string_in[stelle+1],string_in[stelle+2]])
                            string_in.pop(stelle+1)
                            string_in.pop(stelle+1)
                        else:
                            raise ValueError
                    except IndexError:
                        break
    
    elif input_format == 'step_2':
        if output_format in ['step_3', 'step_4', 'step_5', 'step_6', 'step_7']:
            string_out = []
            for x in range(len(string_in)):
                for y in range(len(string_in[x])):
                    string_out.append(string_in[x][y])
    
    elif input_format == 'step_1':
        if output_format == 'output':
            string_out=[]
            for a in string_in:
                for b in a:
                    string_out.append(b)
    
    else:
        string_out=None
    return string_out

def generate(key=False, key_length=key_size, string=False, length=10):
    """used to generate key and/or input strings for testing purposes
    
    set the boolean variables to whatever should be generated
    also set the desired lengths for string and/or string
    """
    key_in=""
    key_ue=[]
    infile=""
    if key:
        for i in range(key_length):
            key_in += str(choice(range(10)))
            key_ue.append(mpf(keys_list[int(key_in[i])]))
    
    if string:
        for i in range(length):
            infile += choice(letters)
    
    if key and string:
        return key_ue, key_in, infile
    elif key:
        return key_ue, key_in
    elif string:
        return infile

def encrypt_without_6_7(key, key_in, string_begin):
    """wrapper for the encrypting process using step 1 to 5
    
    key is a list containing the positions of the key separately. ([1,2,3,4,...])
    key_in is a string or integer, which is the key ("12345...")
    string_begin can be a string or list containing the input string ("abcd..." or [a,b,c,d,...])
    """
    string_begin_1=conversion(string_begin,'input','step_1')

    string_1=[]
    string_2=[]

    for count in range(len(string_begin_1)):
        key_calc=_calc_key(key, key_in, count)
        string_1.append(step_1(string_begin_1, key_calc, count, encrypt=True))
        string_2.append(step_2(string_1, key_calc, count, encrypt=True))

    string_3_begin=conversion(string_2, 'step_2', 'step_3', key=key, key_in=key_in)
    string_3=step_3(string_3_begin)
    string_4=step_4(string_3)
    string_5=step_5(string_4, encrypt=True)
    output=conversion(string_5, 'step_5', 'output')

    return output

def decrypt_without_6_7(key, key_in, string_begin):
    """wrapper for the decrypting process using step 1 to 5
    
    key is a list containing the positions of the key separately. ([1,2,3,4,...])
    key_in is a string or integer, which is the key ("12345...")
    string_begin can be a string or list containing the input string ("abcd..." or [a,b,c,d,...])
    """
    string_begin_1=conversion(string_begin,'input','step_5')

    string_5 = step_5(string_begin_1, encrypt=False)
    string_4 = step_4(string_5)
    string_3 = step_3(string_4)

    string_2_begin = conversion(string_3, 'step_3', 'step_2', key=key, key_in=key_in)

    string_2=[]
    string_1=[]
    for count in range(len(string_2_begin)):
        key_calc=_calc_key(key, key_in, count)
        string_2.append(step_2(string_2_begin, key_calc, count, encrypt=False))
        string_1.append(step_1(string_2, key_calc, count, encrypt=False))

    output = conversion(string_1, 'step_1', 'output')
    return output

def valid_key(key):
    """function to valided the key
    
    key should be in int or string ("123..." or 1234...)
    """
    try:
        key_list = []
        if int(key) > key_max:
            raise ValueError
        
        for i in range(26):
            key_list.append(mpf(keys_list[int(key[i])]))
        
        return key_list
    
    except (IndexError, ValueError):
        return False

def _crypt():
    """internal function using tkinter
    
    responsible for the crypting process for the tkinter application
    """
    progress.grid(row=9,column=0,columnspan=2)
    progress["value"] = 0
    if input_type.get():
        file_ = input_string_entry.get()
        progress["maximum"] = int(4.5*os.path.getsize(file_))
        f = open(file_, "rb")
        string_in = f.read()
    else:
        string_ = input_string_entry.get()
        progress["maximum"] = int(4.5*len(string_))
        string_in=[]
        for byte in string_:
            string_in.append(bytes(byte, 'utf-8')[0])
    
    key_in = key_string_entry.get()
    key=valid_key(key_in)
    if key == False:
        mb.showerror(title="key length not correct", message="The entered key is too small or too big. It should be "+str(key_size)+" characters long.")
        raise ValueError
    output.config(state="normal")
    output.delete(1.0,END)
    if crypt_type.get():
        temp = encrypt_without_6_7(key, key_in, string_in)
    else:
        temp = decrypt_without_6_7(key, key_in, string_in)
    if input_type.get():
        f = open(output_file.get(), "wb")
        for byte in temp:
            f.write(byte)
        f.close()
    else:
        temp_=""
        for byte in temp:
            temp_+=str(byte)[2:-1]
        output.insert(1.0,temp_)
        output.config(state="disabled")
    root.after(0, _success_label_show)


def _select_file():
    """internal function using tkinter"""
    file_name = filedialog.askopenfilename(title="Select File")#,initialdir="~")
    input_string_entry.delete(0, END)
    input_string_entry.insert(0, file_name)

def _select_save_file():
    """internal function using tkinter"""
    file_name = filedialog.asksaveasfilename(title="Save File")
    output_file.delete(0, END)
    output_file.insert(0, file_name)

def _generate_key():
    """internal function using tkinter"""
    key_gen=""
    for i in range(key_size):
        key_gen+=str(choice(range(10)))
    key_string_entry.delete(0, END)
    key_string_entry.insert(0, key_gen)
    
def _file_type():
    """internal function using tkinter"""
    output.grid_forget()
    output_file_label.grid(row=6,column=0,columnspan=2)
    output_file.grid(row=7,column=0,columnspan=2)
    output_file_button.grid(row=7,column=2)
    
def _string_type():
    """internal function using tkinter"""
    output_file_label.grid_forget()
    output_file.grid_forget()
    output_file_button.grid_forget()
    output.grid(row=6,column=0,columnspan=2)
    
def _copy_key():
    """internal function using tkinter"""
    root.clipboard_clear()
    root.clipboard_append(str(key_string_entry.get()))
    
def _success_label_show():
    """internal function using tkinter"""
    mb.showinfo(title="Successful", message="The crypting process was successful.")

def _update_progressbar():
    """internal function using tkinter"""
    try:
        progress["value"] += 1
        progress.update_idletasks()
    except Exception:
        pass

if __name__ == "__main__":
    root = Tk()
    root.title("Crypt")
    input_type = BooleanVar()
    input_type.set(False)
    Radiobutton(root, variable=input_type, text="String", value=False, command=_string_type).grid(row=0,column=0)
    Radiobutton(root, variable=input_type, text="File", value=True, command=_file_type).grid(row=0,column=1)
    input_string_entry = Entry(root, width=50)
    input_string_entry.grid(row=1,column=0,columnspan=2)
    Button(root,text="Choose",command=_select_file).grid(row=1,column=2)
    Label(root,text="Key:").grid(row=2,column=0)
    key_string_entry = Entry(root,width=27)
    key_string_entry.grid(row=3,column=0,columnspan=2)
    Button(root,text="Random",command=_generate_key).grid(row=3,column=2)
    crypt_type = BooleanVar()
    crypt_type.set(True)
    Radiobutton(root, variable=crypt_type, text="Encrypt", value=True).grid(row=4,column=0)
    Radiobutton(root, variable=crypt_type, text="Decrypt", value=False).grid(row=4,column=1)
    Button(root,text="Crypt",command=_crypt).grid(row=5,column=0)#,columnspan=2)
    Button(root,text="Copy Key",command=_copy_key).grid(row=5,column=1)
    output = Text(root)
    output_file_label = Label(root, text="Save File as")
    output_file = Entry(root, width=50)
    output_file_button = Button(root,text="Choose",command=_select_save_file)
    Button(root, text="Quit", command=root.destroy).grid(row=8,column=0,columnspan=2)
    progress = Progressbar(root, orient="horizontal", length=int(root.winfo_reqwidth()*2), mode="determinate")
    
    _string_type()
    
    root.mainloop()
