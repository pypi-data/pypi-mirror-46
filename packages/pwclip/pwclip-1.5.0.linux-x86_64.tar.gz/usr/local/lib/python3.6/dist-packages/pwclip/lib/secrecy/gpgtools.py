#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
gpgtool module
"""
from os import path, environ, remove, name as osname
try:
	from os import uname
except ImportError:
	# windumb faker function
	def uname(): return [0][environ['COMPUTERNAME']]
try:
	from os import chmod
except ImportError:
	# windumb faker function
	def chmod(*_): return

from re import search

from getpass import getpass

from tkinter import TclError

from gnupg import GPG

import wget

try:
	import readline
except ImportError:
	pass

# local imports
from colortext import blu, yel, grn, bgre, tabd, abort, error, fatal

from system import xyesno, xgetpass, xmsgok, xinput, userfind, which

from executor import Command

class DecryptError(Exception):
	pass

class GPGTool(object):
	"""
	gnupg wrapper-wrapper :P
	although the gnupg module is quite handy and the functions are pretty and
	useable i need some modificated easing functions to be able to make the
	main code more easy to understand by wrapping multiple gnupg functions to
	one - also i can prepare some program related stuff in here
	"""
	dbg = None
	gui = None
	iac = None
	__c = 0
	__ppw = None
	homedir = path.join(path.expanduser('~'), '.gnupg')
	if 'GNUPGHOME' in environ.keys():
		homedir = environ['GNUPGHOME'].strip()
	__bin = 'gpg2'
	if osname == 'nt':
		homedir = path.join(
            path.expanduser('~'), 'AppData', 'Roaming', 'gnupg')
		__bin = 'gpg.exe'
	_binary = which(__bin)
	_keyserver = ''
	kginput = {}
	sig = None
	recvs = []
	key = ''
	pwdmsg = 'enter passphrase: '
	def __init__(self, *args, **kwargs):
		"""gpgtool init function"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		args = ['sh_'] + [a for a in args]
		self.cmd = Command(*args)
		if not self.recvs and 'RECIPIENTS' in environ.keys():
			self.recvs = [r.strip() for r in environ['RECIPIENTS'].split(' ')]
		if not self.key and 'GPGKEY' in environ.keys():
			self.key = environ['GPGKEY'].strip()
		if osname == 'nt' and not which('gpg.exe'):
			if not xyesno('mandatory gpg4win not found! Install it?'):
				raise RuntimeError('cannot continue without gpg4win')
			import wget
			src = 'https://files.gpg4win.org/gpg4win-latest.exe'
			trg = path.join(environ['TEMP'], 'gpg4win.exe')
			wget.download(src, out=trg)
			self.cmd.call(trg)
			remove(trg)
		if self.dbg:
			print(bgre(GPGTool.__mro__))
			print(bgre(tabd(GPGTool.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))

	@property                # keyring <str>
	def keyring(self):
		"""pubring getter (read-only)"""
		if self.binary.endswith('.exe'):
			return path.join(self.homedir, 'pubring.gpg')
		return path.join(self.homedir, 'pubring.kbx') \
			if self.binary.endswith('2') else path.join(
                self.homedir, 'pubring.gpg')

	@property                # secring <str>
	def secring(self):
		"""secring getter (read-only)"""
		if self.binary.endswith('.exe'):
			return path.join(self.homedir, 'secring.gpg')
		elif self.binary.endswith('2') and self.keyring.endswith('gpg'):
			return path.join(self.homedir, 'secring.gpg')
		return path.join(self.homedir, 'secring.kbx')

	@property                # binary <str>
	def binary(self):
		"""binary path getter"""
		return self._binary
	@binary.setter
	def binary(self, val):
		"""binary path setter"""
		self._binary = val

	@property                # _gpg_ <GPG>
	def _gpg_(self):
		"""gpg wrapper property"""
		opts = []
		if osname != 'nt':
			opts = ['--pinentry-mode=loopback']
		if self.__c >= 1:
			opts.append('--passphrase="%s"'%self.__ppw)
		__g = GPG(
            keyring=self.keyring, secret_keyring=self.secring,
            gnupghome=self.homedir, gpgbinary=self.binary,
            use_agent=True, options=opts,
            verbose=1 if self.dbg else 0)
		if osname != 'nt':
			__g.encoding = 'utf-8'
		return __g

	@staticmethod
	def passwd(rpt=False, gui=None, msg='enter passphrase: ',
          rptmsg='repeat that passphrase: '):
		"""password questioning method"""
		pas = getpass
		err = error
		if gui:
			pas = xgetpass
			err = xmsgok
		else:
			msg = blu(msg)
			rptmsg = blu(rptmsg)
		while True:
			if not rpt:
				return pas(msg)
			__pwd = pas(msg)
			if __pwd == pas(rptmsg):
				return __pwd
			err('passwords do not match')
		return False

	@staticmethod
	def __find(pattern, *vals):
		"""pattern matching method"""
		if not isinstance(pattern, str):
			raise error('pattern must be type string, got', '%s %s'%(
                type(pattern), pattern))
		for val in vals:
			if isinstance(val, (list, tuple)) and \
                  [v for v in val if pattern in v]:
				return True
			elif isinstance(val, dict) and pattern in val.values():
				return True
			elif pattern in val:
				return True
		return False

	@staticmethod
	def _gendefs(gui=False):
		user = environ['USERNAME'] if osname == 'nt' else environ['USER']
		host = environ['COMPUTERNAME'] if osname == 'nt' else uname()[1]
		kginput = {
                'name_real': user if len(user) >= 5 else '%s key'%user,
                'name_comment': '',
                'name_email': '%s@%s'%(user, host),
                'expire_date': 0,
                'key_type': 'RSA',
                'key_length': 4096,
                'subkey_type': 'RSA',
                'subkey_length': 4096}
		bea = False
		while True:
			echo = print
			ynq = ask = input
			_m = '%s\n%s\n%s [Y/n]\n'
			_g = grn('generating keys using:')
			_d = yel(tabd(kginput, 2))
			_o = grn('Is that OK?')
			if gui:
				echo = xmsgok
				ynq = xyesno
				ask = xinput
				_g = 'generating keys using:'
				_d = tabd(kginput, 2)
				_o = 'Is that OK?'
			msg = _m%(_g, _d, _o)
			try:
				yna = ynq(msg)
			except TclError as err:
				print(err)
				break
			if yna in ('n', False, None):
				msg = '%s [Y/n]'%grn('continue editing?')
				if gui:
					msg = 'abort editing?'
				yna = ynq(msg)
				if yna in ('n', False, None):
					break
			if yna in ('n', False, None):
				while True:
					for (k, v) in sorted(kginput.items()):
						nv = ask(
                            'enter new value for: "%s"\ncurrent value: "%s"\n' \
                            'enter "_" to unset or leave blank to use the ' \
                            ' preset value above\n'%(k, v))
						if nv == '_':
							del kginput[k]
							continue
						nv = v if not nv else nv
						kginput[k] = nv
					msg = _m%(_g, yel(tabd(kginput, 2)), _o)
					bea = ynq(msg)
					if bea is True or bea in ('n', ''):
						break
			elif yna in ('y', '', True):
				break
			if bea is not False:
				break
		return kginput

	def recvlist(self, crypt):
		keys = []
		out = self.cmd.stde('%s --list-only -v -d %s'%(
            self.binary ,crypt)).strip()
		_ks = []
		if out:
			_ks = [l.split(' ')[-1].strip() for l in out.split('\n') if l]
		for k in _ks:
			kv = self.findkey(k, typ='c')
			if not kv: continue
			keys.append('0x%s'%str(list(kv[0].keys())[0])[-16:])
		return keys

	def genkeys(self, **kginput):
		"""key-pair generator method"""
		if self.dbg:
			print(bgre(self.genkeys))
		kginput = kginput if kginput else self._gendefs(self.gui)
		kgmsg = '%s %s%s '%(
            blu('enter new password for'), yel(kginput['name_real']), blu(':'))
		if self.gui:
			echo = xmsgok
			kgmsg = 'enter new password for %s'%kginput['name_real']
		if 'passphrase' not in kginput.keys():
			kginput['passphrase'] = self.passwd(True, self.gui, kgmsg)
		return self._gpg_.gen_key(self._gpg_.gen_key_input(**kginput))

	def findkey(self, pattern='', **kwargs):
		"""key finder method"""
		typ = 'A' if 'typ' not in kwargs.keys() else kwargs['typ']
		sec = False if 'secret' not in kwargs.keys() else kwargs['secret']
		keys = []
		pattern = pattern if not pattern.startswith('0x') else pattern[2:]
		for key in self._gpg_.list_keys(secret=sec):
			if pattern and not self.__find(pattern, *key.values()):
				continue
			finger = key['fingerprint']
			subs = {}
			for (k, _) in key.items():
				if k == 'subkeys':
					#print(k)
					for sub in key[k]:
						#print(sub)
						_, typs, fin = sub
						#print(finger, typs)
						if typ == 'A' or (typ in typs):
							if typs not in subs.keys():
								subs[typs] = []
							subs[typs].append(fin)
			keys.append({finger: subs})
		return keys

	def keyimport(self, key):
		"""key from string import method"""
		if self.dbg:
			print(bgre('%s %s'%(self.keyimport, key)))
		return self._gpg_.import_keys(key)

	def _encryptwithkeystr(self, message, keystr, output):
		"""encrypt using given keystring method"""
		fingers = [
            r['fingerprint'] for r in self._gpg_.import_keys(keystr).results]
		return self._gpg_.encrypt(
            message, fingers, output=output)

	def _fingered(self, keys, typ='e'):
		fingers = []
		if not keys:
			return error('no keys received', keys, 'mode', typ)
		for key in keys:
			for (hsh, tyks) in key.items():
				if typ == 'c':
					fingers.append(hsh)
				else:
					for t in tyks.keys():
						if typ in t:
							fingers = fingers + tyks[t]
		return fingers

	def sign(self, data):
		"""text encrypting method"""
		if self.dbg:
			print(bgre(self.sign))
		if not self.key:
			return error('no default key defined which is needed for signing')
		finger = self._fingered(self.findkey(self.key, typ='s'))
		finger = '' if not finger else finger[0]
		out = '%s.sig'%data
		if path.isfile(data):
			with open(data, 'rb') as cfh:
				self._gpg_.sign_file(
                    cfh, keyid=finger, detach=True, output=out)
		else:
			return self._gpg_.sign(data, keyid=finger)
		if path.isfile(out):
			chmod(out, 0o644)

	def verify(self, sign, data=None):
		try:
			with open(sign, 'rb') as sfh, open(data, 'rb') as dfh:
				return self._gpg_.verify_file(sfh, data)
		except (OSError, FileNotFoundError):
			return self._gpg_.verify(sign)

	def encrypt(self, message, **kwargs):
		"""text encrypting method"""
		if self.dbg:
			print(bgre(self.encrypt))
		out = None if 'output' not in kwargs.keys() else kwargs['output']
		recvs = [] if not self.recvs else self.recvs
		if 'recipients' in kwargs.keys():
			recvs = kwargs['recipients']
		fingers = []
		for rec in recvs:
			fingers = fingers + self._fingered(self.findkey(rec, typ='e'))
		crypt = self._gpg_.encrypt(message, fingers, output=out)
		if path.isfile(out):
			chmod(out, 0o600)
		if self.sig:
			if not out:
				ret = self.sign(crypt)
			ret = self.sign(out)
			if path.isfile('%s.sig'%out):
				chmod('%s.sig'%out, 0o644)

	def decrypt(self, data, **kwargs):
		"""text decrypting method"""
		if self.dbg:
			print(bgre(self.decrypt))
		out = None if not 'output' in kwargs.keys() else kwargs['output']
		sig = self.sig if 'sign' not in kwargs.keys() else kwargs['sign']
		try:
			with open(data, 'r') as cfh:
				message = str(cfh.read())
		except (OSError, FileNotFoundError):
			message = data
		if sig:
			sign = '%s.sig'%data
			signed = self.verify(sign, data)
			if not signed or not signed.valid:
				yesno = 'n'
				if self.gui:
					yesno = xyesno('signature could not be verified\n' \
                                   'continue anyways?')
					yesno = 'y' if yesno else 'n'
				else:
					error('signature could not be verified')
					print(grn('continue anyways?'), '[y/N]')
					yesno = input()
				if yesno.lower() != 'y':
					raise DecryptError('signature verification failed')
		while self.__c < 4:
			__plain = self._gpg_.decrypt(
                str(message), always_trust=True,
                output=out, passphrase=self.__ppw)
			if __plain.ok:
				return __plain
			yesno = 'n'
			if self.__c > 3:
				if self.gui:
					xmsgok('too many wrong attempts')
					exit(1)
				fatal('too many wrong attempts')
			elif self.__c >= 1 and self.__c < 3:
				yesno = 'y'
				if self.gui:
					yesno = xyesno('decryption failed - try again?')
					yesno = 'y' if yesno else 'n'
				else:
					yesno = input('decryption failed - retry? [Y/n]')
			if yesno.lower() == 'n':
				raise DecryptError('%s cannot decrypt %s'%(
                    self.decrypt, message))
			self.__c += 1
			try:
				self.__ppw = self.passwd(False, self.gui, self.pwdmsg)
			except KeyboardInterrupt:
				return False
		return False


class GPGSMTool(GPGTool):
	"""GPGSMTool class for compatibility to SSL keys/certificates"""
	dbg = False
	homedir = path.join(path.expanduser('~'), '.gnupg')
	__gsm = 'gpgsm'
	__ssl = 'openssl'
	if osname == 'nt':
		homedir = path.join(
            path.expanduser('~'), 'AppData', 'Roaming', 'gnupg')
		__gsm = 'gpgsm.exe'
		__ssl = 'openssl.exe'
	_gsmbin = which(__gsm)
	_sslbin = which(__ssl)
	sslcrt = ''
	sslkey = ''
	sslca = ''
	recvs = []
	def __init__(self, *args, **kwargs):
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if not self.recvs:
			if 'GPGKEYS' in environ.keys():
				self.recvs = environ['GPGKEYS'].split(' ')
			elif 'GPGKEY' in environ.keys():
				self.recvs = [environ['GPGKEY']]
		if self.sslcrt and self.sslkey:
			if osname == 'nt':
				raise RuntimeError(
                    'ssl import is currently not available for windows')
			self.sslimport(self.sslkey, self.sslcrt, self.sslca)
		if self.dbg:
			print(bgre(GPGSMTool.__mro__))
			print(bgre(tabd(GPGSMTool.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		GPGTool.__init__(self, *args, **kwargs)
		args = ['sh_'] + [a for a in args]
		self.cmd = Command(*args)

	def sslimport(self, key, crt, ca):
		"""ssl key/cert importing method"""
		if self.dbg:
			print(bgre('%s key=%s crt=%s'%(self.sslimport, key, crt)))
		self.cmd.stdo('%s --import'%self._gsmbin, inputs=self.cmd.stdo(
            '%s pkcs12 -export -chain -CAfile %s -in %s -inkey %s'%(
                self._sslbin, ca, crt, key), b2s=False), b2s=False)

	def keylist(self, secret=False):
		"""key listing function"""
		if self.dbg:
			print(bgre(self.keylist))
		gsc = 'gpgsm -k'
		if secret:
			gsc = 'gpgsm -K'
		kstrs = self.cmd.stdo(gsc)
		keys = []
		if kstrs:
			kstrs = str('\n'.join(kstrs.split('\n')[2:])).split('\n\n')
			for ks in kstrs:
				if not ks: continue
				kid = str(ks.split('\n')[0].strip()).split(': ')[1]
				inf = [i.strip() for i in ks.split('\n')[1:]]
				key = {kid: {}}
				for i in inf:
					key[kid][i.split(': ')[0]] = i.split(': ')[1]
				keys.append(key)
		return keys

	def findkey(self, pattern=''):
		return self.keylist()

	def encrypt(self, message, **kwargs):
		"""text encrypting method"""
		if self.dbg:
			print(bgre(self.encrypt))
		recvs = self.recvs if 'recvs' not in kwargs.keys() else kwargs['recvs']
		if 'recipients' in kwargs.keys():
			recvs = kwargs['recipients']
		recvs = ''.join(['-r %s'%r for r in recvs])
		out = '' if 'output' not in kwargs.keys() else '-o %s'%kwargs['output']
		gsc = '%s -e --armor --disable-policy-checks --disable-crl-checks ' \
            '%s %s'%(self._gsmbin, out, recvs)
		__crypt = self.cmd.stdo(gsc, inputs=message.encode())
		if __crypt:
			return __crypt.decode()
		return False

	def decrypt(self, message, output=None):
		"""text decrypting method"""
		if self.dbg:
			print(bgre(self.decrypt))
		out = '' if not output else '-o %s'%'output'
		gsc = '%s -d %s'%(self._gsmbin, out)
		__plain = self.cmd.stdo(gsc, inputs=message)
		if __plain:
			return __plain
		return False
