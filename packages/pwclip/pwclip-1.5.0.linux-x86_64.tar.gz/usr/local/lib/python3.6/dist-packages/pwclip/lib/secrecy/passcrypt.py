#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""passcrypt module"""

from sys import argv, stdout

from os import path, remove, environ, chmod, stat, makedirs

import socket

from time import time

from yaml import load, dump, Loader

from paramiko.ssh_exception import SSHException

from colortext import blu, yel, bgre, tabd, error

from system import userfind, filerotate, setfiletime, filetime

from net.ssh import SecureSHell

from secrecy.gpgtools import GPGTool, GPGSMTool, DecryptError

class PassCrypt(object):
	"""passcrypt main class"""
	dbg = None
	fen = None
	aal = None
	fsy = None
	sho = None
	rem = None
	gsm = None
	key = None
	sig = True
	gui = None
	chg = None
	syn = None
	try:
		user = userfind()
		home = userfind(user, 'home')
	except FileNotFoundError:
		user = environ['USERNAME']
		home = path.join(environ['HOMEDRIVE'], environ['HOMEPATH'])
	user = user if user else 'root'
	home = home if home else '/root'
	config = path.join(home, '.config', 'pwclip.cfg')
	plain = path.join(home, '.pwd.yaml')
	crypt = path.join(home, '.passcrypt')
	timefile = path.expanduser('~/.cache/PassCrypt.time')
	remote = ''
	reuser = user
	recvs = []
	key = ''
	keys = {}
	sslcrt = ''
	sslkey = ''
	maxage = 3600
	__weaks = {}
	__oldweaks = {}
	def __init__(self, *args, **kwargs):
		"""passcrypt init function"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(PassCrypt.__mro__))
			print(bgre(tabd(PassCrypt.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		self.cpasmsg = '%s %s%s '%(
            blu('enter password for'), yel(self.crypt), blu(':'))
		gargs = list(args) + ['sig'] if self.sig else []
		if self.gui:
			gargs = list(args) + ['gui'] + ['sig'] if self.sig else []
			self.cpasmsg = 'enter password for %s: '%self.crypt
		gsks = GPGSMTool().keylist(True)
		if self.gsm or (
              self.gsm is None and self.recvs and [
                  r for r in self.recvs if r in gsks]):
			self.gpg = GPGSMTool(*gargs, **kwargs)
		else:
			self.gpg = GPGTool(*gargs, **kwargs)
		self.keys = self.gpg.findkey()
		if not self.keys:
			self._mkconfkeys()
		self.ssh = SecureSHell(*args, **kwargs)
		self._cecktimecopynews()
		self.__weaks = self._mergecrypt()

	def __del__(self):
		chgs = []
		crecvs = []
		if path.isfile(self.crypt):
			erecvs = list(set(GPGTool().recvlist(self.crypt)))
			for r in erecvs:
				crecvs.append('0x%s'%r[-16:])
			for r in self.recvs:
				if r not in crecvs:
					chgs.append('+ %s'%r)
			for r in crecvs:
				if r not in self.recvs:
					chgs.append('- %s'%r)
		if self.chg or self.fen or chgs:
			if not self.gui and chgs:
					error(
                    'recipients have changed:\n',
                    '\n'.join(c for c in chgs),
                    '\nfrom:\n', ' '.join(erecvs),
                    '\nto:\n', ' '.join(self.recvs),
                    '\nencryption enforced...', sep='')
			if not self.recvs and not self.gpg.findkey():
				self.gpg.genkeys(self.gpg._gendefs(self.gui))
			if self._writecrypt(self.__weaks):
				if self.rem:
					self._copynews()

	def _mkconfkeys(self):
		self.key = self.gpg.key = '0x%s'%str(self.gpg.genkeys())[-16:]
		cfgs = {'gpg': {}}
		override = False
		if path.isfile(self.config):
			override = True
			with open(self.config, 'r') as cfh:
				cfgs = dict(load(cfh.read(), Loader=Loader))
			if 'gpg' not in cfgs.keys():
				cfgs['gpg'] = {}
		cfgs['gpg']['key'] = self.key
		if 'recipients' not in cfgs['gpg'].keys():
			cfgs['gpg']['recipients'] = self.key
			self.recvs = [self.key]
		with open(self.config, 'w+') as cfh:
			cfh.write(str(dump(cfgs)))

	def _cecktimecopynews(self):
		if self.rem and self.maxage:
			tf = absrelpath(self.timefile)
			if not path.exists(path.dirname(tf)):
				makedirs(path.dirname(tf))
			now = int(time())
			if not path.exists(tf):
				with open(timefile, 'w+') as tfh:
					tfh.write(str(now-self.maxage))
			with open(timefile, 'r') as tfh:
				last = int(tfh.read())
			self.age = int(now-int(last))
			if self.age >= int(self.maxage):
				with open(timefile, 'w+') as tfh:
					tfh.write(str(now))
			return self._copynews()

	def _mergecrypt(self):
		__weaks = {}
		if path.isfile(self.crypt):
			__weaks = self._readcrypt()
		try:
			with open(self.plain, 'r') as pfh:
				__newweaks = load(pfh.read(), Loader=Loader)
			if not self.dbg:
				remove(self.plain)
		except FileNotFoundError:
			__newweaks = {}
			setattr(self, 'chg', True)
		__weaks = __weaks if __weaks else __newweaks
		for (su, ups) in __newweaks.items():
			for (usr, pwdcom) in ups.items():
				if su not in __weaks.keys():
					__weaks[su] = {}
				__weaks[su][usr] = pwdcom
		return __weaks

	def _copynews(self, force=None):
		"""copy new file method"""
		if self.dbg:
			print(bgre(self._copynews))
		for i in (self.crypt, '%s.sig'%self.crypt):
			if SecureSHell().scpcompstats(
                  i, path.basename(i),
                  2, remote=self.remote, reuser=self.reuser):
				print(
                    blu('file'),
                    yel(path.basename(i)), blu('synced successful'))
		return True

	def _readcrypt(self):
		"""read crypt file method"""
		if self.dbg:
			print(bgre(self._readcrypt))
		try:
			return load(str(self.gpg.decrypt(self.crypt)), Loader=Loader)
		except DecryptError as err:
			error(err)
			exit(1)

	def _writecrypt(self, __weaks):
		"""crypt file writing method"""
		if self.dbg:
			print(bgre(self._writecrypt))
		kwargs = {
            'output': self.crypt,
            'recipients': self.recvs}
		isok = None
		for _ in range(0, 2):
			isok = self.gpg.encrypt(message=dump(__weaks), **kwargs)
			chmod(self.crypt, 0o600)
			now = int(time())
			setfiletime(self.crypt, (now, now))
		return True

	@staticmethod
	def __askpwdcom(sysuser, usr, pwd, com, opw, ocom, passwd):
		print(blu('as user '), yel(sysuser), ': ', sep='')
		pwd = pwd if pwd else passwd(msg='%s%s%s%s: '%(
                blu('  enter '), yel('password '),
                blu('for entry '), yel('%s'%usr)))
		pwd = pwd if pwd else opw
		if not pwd:
			error('password is needed if adding password')
			return
		if not com:
			print(
                blu('  enter '), yel('comment '),
                blu('(optional, ___ deletes the comment)')
                , ': ', sep='', end='')
			com = input()
		com = ocom if not com else com
		if com == '___':
			com = None
		return [p for p in [pwd, com] if p is not None]

	def adpw(self, usr, pwd=None, com=None):
		"""password adding method"""
		if self.dbg:
			print(bgre(tabd({
                self.adpw: {'user': self.user, 'entry': usr,
                            'pwd': pwd, 'comment': com}})))
		if not self.aal:
			if self.user in self.__weaks.keys() and \
                  usr in self.__weaks[self.user].keys():
				return error('entry', usr, 'already exists for user', self.user)
			try:
				__opw, __ocom = self.__weaks[self.user][usr]
			except (KeyError, ValueError):
				__opw, __ocom = None, None
			pwdcom = self.__askpwdcom(
                self.user, usr, pwd, com, __opw, __ocom, self.gpg.passwd)
			if pwdcom:
				self.__weaks[self.user][usr] = [p for p in pwdcom if p]
			setattr(self, 'chg', True)
		else:
			for u in self.__weaks.keys():
				if usr in self.__weaks[u].keys():
					error('entry', usr, 'already exists for user', u)
					continue
				try:
					__opw, __ocom = self.__weaks[u][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				pwdcom = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom, self.gpg.passwd)
				if pwdcom:
					self.__weaks[u][usr] = [p for p in pwdcom if p]
				setattr(self, 'chg', True)
		return self.__weaks

	def chpw(self, usr, pwd=None, com=None):
		"""change existing password method"""
		if self.dbg:
			print(bgre(tabd({
                self.chpw: {'user': self.user, 'entry': usr, 'pwd': pwd}})))
		if not self.aal:
			if self.__weaks and self.user in self.__weaks.keys() and \
                  usr in self.__weaks[self.user].keys():
				try:
					__opw, __ocom = self.__weaks[self.user][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				self.__weaks[self.user][usr] = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom, self.gpg.passwd)
				setattr(self, 'chg', True)
			else:
				error('no entry named', usr, 'for user', self.user)
		else:
			for u in self.__weaks.keys():
				if usr not in self.__weaks[u].keys():
					error('entry', usr, 'does not exist for user', u)
					continue
				try:
					__opw, __ocom = self.__weaks[self.user][usr]
				except (KeyError, ValueError):
					__opw, __ocom = None, None
				self.__weaks[u][usr] = self.__askpwdcom(
                    self.user, usr, pwd, com, __opw, __ocom, self.gpg.passwd)
				setattr(self, 'chg', True)
		return self.__weaks

	def rmpw(self, usr):
		"""remove password method"""
		if self.dbg:
			print(bgre(tabd({self.rmpw: {'user': self.user, 'entry': usr}})))
		if self.aal:
			for u in self.__weaks.keys():
				try:
					del self.__weaks[u][usr]
					setattr(self, 'chg', True)
				except KeyError:
					error('entry', usr, 'not found for', u)
		else:
			try:
				del self.__weaks[self.user][usr]
				setattr(self, 'chg', True)
			except KeyError:
				error('entry', usr, 'not found for', self.user)
		return self.__weaks

	def lspw(self, usr=None, aal=None):
		"""password listing method"""
		if self.dbg:
			print(bgre(tabd({self.lspw: {'user': self.user, 'entry': usr}})))
		aal = True if aal else self.aal
		__ents = {}
		if self.__weaks:
			if aal:
				__ents = self.__weaks
				if usr:
					usrs = [self.user] + \
                        [u for u in self.__weaks.keys() if u != self.user]
					for user in usrs:
						if user in self.__weaks.keys() and \
                              usr in self.__weaks[user].keys():
							__ents = {usr: self.__weaks[user][usr]}
							break
			elif self.user in self.__weaks.keys():
				__ents = self.__weaks[self.user]
				if usr in __ents.keys():
					__ents = {usr: self.__weaks[self.user][usr]}
		return __ents

def lscrypt(usr, dbg=None):
	"""passlist wrapper function"""
	if dbg:
		print(bgre(lscrypt))
	__ents = {}
	if usr:
		__ents = PassCrypt().lspw(usr)
	return __ents




if __name__ == '__main__':
	exit(1)
