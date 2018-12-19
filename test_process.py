import multiprocessing
import os
import time


def run_task(name):
	while True:
		print('Task {0} pid {1} is running, parent id is {2}'.format(
				name, os.getpid(), os.getppid()))
		time.sleep(1)


class T():
	def ser_(self):
		while True:
			print('server reserve')
			time.sleep(1)

	def cli_(self):
		while True:
			print('client send')
			time.sleep(2)

	def feed_dog(self):
		while True:
			print('feed dog!')
			time.sleep(5)

	def run(self):
		p = multiprocessing.Pool(processes=3)
		p.apply_async(self.ser_)
		p.apply_async(self.cli_)
		p.apply_async(self.feed_dog)
		p.close()
		p.join()


if __name__ == '__main__':
	# print('current process {0}'.format(os.getpid()))
	# p = multiprocessing.Pool(processes=6)
	# for i in range(6):
	# 	p.apply_async(run_task, args=(i,))
	# print('Waiting for all subprocesses done...')
	test = T()
	test.run()
	print('All processes done!')
