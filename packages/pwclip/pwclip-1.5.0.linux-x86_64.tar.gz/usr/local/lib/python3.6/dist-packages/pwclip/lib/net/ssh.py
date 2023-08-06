#!/usr/bin/env python3
"""ssh connection and remote command """

#global imports"""
import os
from os.path import basename
import sys
import stat
from shutil import copy2, copyfile
from socket import \
    gaierror as NameResolveError, timeout as sockettimeout
from psutil import Process

from paramiko import AutoAddPolicy, SSHException, ssh_exception
from paramiko.client import SSHClient
from paramiko.agent import AgentRequestHandler

from colortext import bgre, tabd, abort, error
from executor import Command
from system import which, whoami, userfind, filetime, setfiletime, filerotate
from net import askdns

# default vars
__version__ = '0.1'

class SecureSHell(Command):
	"""paramiko wrapper class"""
	dbg = None
	reuser = whoami()
	remote = ''
	ssh = None
	def __init__(self, *args, **kwargs):
		"""ssh init function"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(SecureSHell.__mro__))
			print(bgre(tabd(self.__dict__, 2)))
		Command.__init__(self, *args, **kwargs)

	def _ssh(self, remote=None, reuser=None, port=22):
		"""ssh connector method"""
		if self.ssh: return self.ssh
		remote = remote if remote else self.remote
		reuser = reuser if reuser else self.reuser
		if '@' in remote:
			reuser, remote = remote.split('@')
		reuser = whoami() if not reuser else reuser
		#prc = Process(os.getppid()).name()
		#if prc == 'sudo':
		#uuid = userfind(userfind(), 'uid')
		#sshsock = '/run/user/%s/gnupg/S.gpg-agent.ssh'%uuid
		#os.environ['GNUPGHOME'] = os.path.dirname(sshsock)
		os.environ['GPG_AGENT_INFO'] = '/tmp/ssh-gmAiq6Vy73/agent.17632'
		#print(os.getenv('GNUPGHOME'))
		#print(os.getenv('GPG_AGENT_INFO'))
		if self.dbg:
			print(bgre('%s\n  %s@%s:%s '%(
                self._ssh, reuser, remote, port)))
		__ssh = SSHClient()
		__ssh.set_missing_host_key_policy(AutoAddPolicy())
		#__ssh.load_system_host_keys()
		__ssh.connect(
                askdns(remote), int(port),
                username=reuser, allow_agent=True, look_for_keys=True)
		ses = __ssh.get_transport().open_session()
		agent = AgentRequestHandler(ses)
		self.ssh = __ssh
		return self.ssh

	def rrun(self, cmd, remote=None, reuser=None):
		"""remote run method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.rrun, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		try:
			ssh.exec_command(cmd)
		except (AttributeError, ssh_exception.SSHException) as err:
			error(self.rrun, err)

	def rcall(self, cmd, remote=None, reuser=None):
		"""remote call method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.rcall, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		try:
			chn = ssh.get_transport().open_session()
			chn.settimeout(10800)
			chn.exec_command(cmd)
			while not chn.exit_status_ready():
				if chn.recv_ready():
					och = chn.recv(1024)
					while och:
						sys.stdout.write(och.decode())
						och = chn.recv(1024)
				if chn.recv_stderr_ready():
					ech = chn.recv_stderr(1024)
					while ech:
						sys.stderr.write(ech.decode())
						ech = chn.recv_stderr(1024)
			return int(chn.recv_exit_status())
		except (
               AttributeError, ssh_exception.SSHException, sockettimeout
               ) as err:
			error(self.rcall, err)
			raise err
		except KeyboardInterrupt:
			abort()

	def rstdx(self, cmd, remote=None, reuser=None):
		"""remote stout/error method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.rstdx, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		try:
			_, out, err = ssh.exec_command(cmd)
		except (AttributeError, ssh_exception.SSHException) as err:
			error(self.rstdx, err)
		return ''.join(out.readlines()), ''.join(err.readlines())

	def rstdo(self, cmd, remote=None, reuser=None):
		"""remote stdout method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.rstdo, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		try:
			_, out, _ = ssh.exec_command(cmd)
		except (AttributeError, ssh_exception.SSHException) as err:
			error(self.rstdo, err)
		return ''.join(out.readlines())

	def rstde(self, cmd, remote=None, reuser=None):
		"""remote stderr method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.rstde, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		ssh = self._ssh(remote, reuser)
		try:
			_, _, err = ssh.exec_command(cmd)
		except (AttributeError, ssh_exception.SSHException) as err:
			error(self.rstde, err)
		return ''.join(err.readlines())

	def rerno(self, cmd, remote=None, reuser=None):
		"""remote error code  method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.rerno, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		ssh = self._ssh(remote, reuser)
		try:
			_, out, _ = ssh.exec_command(cmd)
		except (AttributeError, ssh_exception.SSHException) as err:
			error(self.rerno, err)
		return int(out.channel.recv_exit_status())

	def roerc(self, cmd, remote=None, reuser=None):
		"""remote stdout/stderr/errorcode method"""
		if self.dbg:
			print(bgre('%s\n  cmd = %s'%(self.roerc, cmd)))
		ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		ssh = self._ssh(remote, reuser)
		try:
			_, out, err = ssh.exec_command(cmd)
		except (AttributeError, ssh_exception.SSHException) as err:
			error(self.roerc, err)
		return ''.join(out.readlines()), ''.join(err.readlines()), \
            out.channel.recv_exit_status()

	def get(self, src, trg, remote=None, reuser=None):
		"""sftp get method"""
		if not (os.path.isfile(src) or os.path.isfile(trg)):
			raise FileNotFoundError('connot find either %s nor %s'%(src, trg))
		remote = remote if remote else self.remote
		reuser = reuser if reuser else self.reuser
		cmd = '%s %s@%s:%s %s'%(which('scp'), reuser, remote, src, trg)
		if self.dbg:
			print(bgre('%s\n  src = %s\n  trg = %s\n  cmd = %s\n'%(
                self.get, src, trg, cmd)))
		eno = self.call(cmd)
		if eno != 0:
			error('command', cmd, 'returned non-zero value')
		#ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		#ssh = self._ssh(remote, reuser)
		#scp = ssh.open_sftp()
		#ret = scp.get(src, trg)
		#scp.close()
		return eno

	def put(self, src, trg, remote=None, reuser=None):
		"""sftp put method"""
		if not (os.path.isfile(src) or os.path.isfile(trg)):
			raise FileNotFoundError('connot find either %s nor %s'%(src, trg))
		remote = remote if remote else self.remote
		reuser = reuser if reuser else self.reuser
		#ssh = self.ssh if self.ssh else self._ssh(remote, reuser)
		#ssh = self._ssh(remote, reuser)
		#scp = ssh.open_sftp()
		#ret = scp.put(src, trg)
		#scp.close()
		cmd = '%s %s %s@%s:%s'%(
            which('scp'), src, reuser, remote, basename(trg))
		if self.dbg:
			print(bgre('%s\n  src = %s\n  trg = %s\n  cmd = %s\n'%(
                self.put, src, trg, cmd)))
		o, e, n = self.oerc(cmd)
		if n != 0:
			error('command', cmd, 'returned non-zero value', n)

	def rcompstats(self, src, trg, remote=None, reuser=None):
		"""remote file-stats compare """
		smt = int(os.stat(src).st_mtime)
		if self.dbg:
			print(bgre('%s\n  src = %s\n  trg = %s'%(self.rcompstats, src, trg)))
		rmt = self.rstdo(
            'stat -c %%Y %s'%trg, remote=remote, reuser=reuser)
		if rmt:
			rmt = int(str(rmt))
		srctrg = src, '%s@%s:%s'%(reuser, remote, trg)
		if rmt == smt:
			return
		elif rmt and int(rmt) > int(smt):
			srctrg = '%s@%s:%s'%(reuser, remote, trg), src
		return srctrg

	def rfiletime(self, trg, remote=None, reuser=None):
		"""remote file-timestamp method"""
		if self.dbg:
			print(bgre('%s\n trg = %s'%(self.rfiletime, trg)))
		tamt = str(self.rstdo(
            'stat -c "%%X %%Y" %s'%trg, remote, reuser).strip())
		tat = 0
		tmt = 0
		if tamt:
			tat, tmt = tamt.split(' ')
		return int(tmt), int(tat)

	def rsetfiletime(self, trg, mtime, atime, remote=None, reuser=None):
		"""remote file-timestamp set method"""
		if self.dbg:
			print(bgre('%s\n trg = %s\n  mtime = %s\n  atime = %d'%(
			    self.rsetfiletime, trg, mtime, atime)))
		self.rstdo(
            'touch -m --date=@%s %s'%(mtime, trg), remote, reuser)
		self.rstdo(
            'touch -a --date=@%s %s'%(atime, trg), remote, reuser)

	def scpcompstats(self, lfile, rfile, rotate=0, remote=None, reuser=None):
		"""
		remote/local file compare method copying and
		setting the file/timestamp of the neweer one
		"""
		if self.dbg:
			print(bgre(self.scpcompstats))
			print(bgre('  %s@%s:%s %s'%(remote, reuser, rfile, lfile)))
		lmt, lat = filetime(lfile)
		rmt, rat = self.rfiletime(rfile, remote, reuser)
		if rmt == lmt:
			return True
		if rotate > 0:
			filerotate(lfile, rotate)
		if rmt and rmt > lmt:
			self.get(rfile, lfile, remote, reuser)
			setfiletime(lfile, rmt, rat)
			os.chmod(lfile, oct('0o%s'%self.rstdo('stat -c %%a %s'%rfile)))
		else:
			omode = str(oct(stat.S_IMODE(os.stat(lfile).st_mode)))
			self.put(lfile, rfile, remote, reuser)
			self.rsetfiletime(rfile, lmt, lat, remote, reuser)
			self.rcall('chmod %s%s %s'%(
                omode[:1], omode[-3:], rfile))
		return True



if __name__ == '__main__':
	"""module debugging area"""
	#ssh = SecureSHell(**{'remote':'bigbox.janeiskla.de'})
	#print(ssh.command('cat /etc/debian_version'))
