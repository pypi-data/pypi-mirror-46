import os
import sys
import urllib.parse
from ctypes import *

so = 'shitf_mac.so'
if sys.platform == 'linux':
  so = 'shitf_linux.so'

if sys.platform != 'win32':
  shitf = CDLL(os.path.dirname(__file__) + os.path.sep + so)

def rotate_left(n,s) :
  t4 = shitf._or(( shitf.left_shitf(n,s )), (shitf.unsigned_right_shitf(n,(32-s))));
  return t4;

def lsb_hex(val) :
  str="";

  for i in range(0, 7, 2) :
    vh = shitf._and((shitf.unsigned_right_shitf(val,(i*4+4))),0x0f)
    vl = shitf._and((shitf.unsigned_right_shitf(val,(i*4))),0x0f)
    str += format(vh,'x') + format(vl,'x')
  return str;

def cvt_hex(val) :
  str="";

  for i in range(7, -1, -1) :
    v = shitf._and((shitf.unsigned_right_shitf(val,(i*4))),0x0f)
    str += format(v,'x')
  return str;

def SHA1(msg) :
	W = [];
	H0 = 0x67452301;
	H1 = 0xEFCDAB89;
	H2 = 0x98BADCFE;
	H3 = 0x10325476;
	H4 = 0xC3D2E1F0;

	msg = utf2bytes(msg);
	msg_len = len(msg);

	word_array = [];
	for i in range(0, (msg_len-3), 4) :
		j = shitf._or(shitf._or(shitf.left_shitf(msg[i],24) , shitf.left_shitf(msg[i+1],16)) , shitf._or(shitf.left_shitf(msg[i+2],8) , msg[i+3]))
		word_array.append( j );

	if msg_len % 4 == 0:
		i = 0x080000000;
	elif msg_len % 4 == 1:
		i = shitf._or(shitf.left_shitf(msg[msg_len-1],24) , 0x0800000)
	elif msg_len % 4 == 2:
		i = shitf._or(shitf._or(shitf.left_shitf(msg[msg_len-2],24) , shitf.left_shitf(msg[msg_len-1],16)) , 0x08000);
	elif msg_len % 4 == 3:
		i = shitf._or(shitf._or(shitf.left_shitf(msg[msg_len-3],24) , shitf.left_shitf(msg[msg_len-2],16)) , shitf._or(shitf.left_shitf(msg[msg_len-1],8)	, 0x80))

	word_array.append( i );

	while ((len(word_array) % 16) != 14):
		word_array.append( 0 );

	word_array.append( shitf.unsigned_right_shitf(msg_len,29 ));
	word_array.append( shitf._and((shitf.left_shitf(msg_len,3)),0x0ffffffff ));

	for blockstart in range(0, len(word_array), 16):
		for i in range(0, 16):
			W.append(word_array[blockstart+i])
		for i in range(16, 80):
			  W.append(rotate_left(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1))
	A = H0;
	B = H1;
	C = H2;
	D = H3;
	E = H4;

	for i in range(0, 20):
		temp = shitf._and((rotate_left(A,5) + (shitf._or((shitf._and(B,C)) , (shitf._and(shitf._not(B),D)))) + E + W[i] + 0x5A827999) , 0x0ffffffff)
		E = D;
		D = C;
		C = rotate_left(B,30);
		B = A;
		A = temp;

	for i in range(20, 40):
		temp = shitf._and((rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) , 0x0ffffffff)
		E = D;
		D = C;
		C = rotate_left(B,30);
		B = A;
		A = temp;

	for i in range(40, 60):
		temp = shitf._and((rotate_left(A,5) + (shitf._or(shitf._or((shitf._and(B,C)) , (shitf._and(B,D))) , (shitf._and(C,D)))) + E + W[i] + 0x8F1BBCDC) , 0x0ffffffff)
		E = D;
		D = C;
		C = rotate_left(B,30);
		B = A;
		A = temp;

	for i in range(60, 80):
		temp = shitf._and((rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) , 0x0ffffffff)
		E = D;
		D = C;
		C = rotate_left(B,30);
		B = A;
		A = temp;

	H0 = shitf._and((H0 + A) , 0x0ffffffff)
	H1 = shitf._and((H1 + B) , 0x0ffffffff)
	H2 = shitf._and((H2 + C) , 0x0ffffffff)
	H3 = shitf._and((H3 + D) , 0x0ffffffff)
	H4 = shitf._and((H4 + E) , 0x0ffffffff)

	return (cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4)).lower()

def utf2bytes(s) :
	s = urllib.parse.quote(s)
	l = len(s)
	q = [];
	i = 0
	while (i<l):
		p = s[i:i+1];
		if p=='%' :
			q.append(int(s[i+1:i+3], 16));
			i+= 3;
		else:
			q.append(ord(p[0]));
			i+= 1;
	return q;

def bytes2hex(arr) :
	l = len(arr)
	q = [];
	for i in range(l):
		t = format(arr[i],'x')
		q.append('0'+t if len(t)==1 else t);
	return ''.join(q)

def hex2bytes(s) :
	l = len(s)
	q = [];
	for i in range(0, l, 2):
		result = int(s[i:i+2],16)
		q.append(int(s[i:i+2],16));
	return q;

def bytes2utf(arr) :
	for i in range(len(arr)):
		arr[i] = chr(arr[i]);
	return ''.join(arr);

def rc4_arr(key, arr) :
	s = [];
	for i in range(256):
		s.append(i)
	j = 0
	x = 0
	for i in range(256):
		j = (j + s[i] + ord(key[i % len(key)])) % 256;
		x = s[i];
		s[i] = s[j];
		s[j] = x;
	i = 0; j = 0;
	ct = [];
	al = len(arr)
	for y in range(al):
		i = (i + 1) % 256;
		j = (j + s[i]) % 256;
		x = s[i];
		s[i] = s[j];
		s[j] = x;
		ct.append(arr[y] ^ s[(s[i] + s[j]) % 256])
	return ct;