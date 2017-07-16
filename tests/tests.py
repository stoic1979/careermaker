import md5


def test_md5(str):
	return md5.new(str).hexdigest()


def main():
	# checking md5 sum
	print "%s" % test_md5("some-password")

if __name__ == '__main__':
	main()