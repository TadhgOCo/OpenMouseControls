def reset_defaults():
	buf = bytearray(65)

	buf[3] = 0x02
	buf[4] = 0x02
	buf[7] = 0xC0
	buf[8] = 0x01

	return bytes(buf)


def reset_profile(profile_id):
	buf = bytearray(65)

	buf[3] = 0x02
	buf[4] = 0x01
	buf[6] = 0x0D
	buf[7] = profile_id

	return bytes(buf)


def get_profile():
	buf = bytearray(65)

	buf[3] = 0x02
	buf[4] = 0x01
	buf[6] = 0x85

	return bytes(buf)


def set_profile(profileID):
	buf = bytearray(65)

	buf[3] = 0x02
	buf[4] = 0x01
	buf[6] = 0x05
	buf[7] = profileID

	return bytes(buf)