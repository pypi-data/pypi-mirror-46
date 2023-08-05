import karantools as kt
import pytest

def test_average_simple():
	assert(kt.average([1, 2, 3]) == 2)
	assert(kt.average([1]) == 1)
	assert(kt.average([1, 2, 3, 4]) == 2.5)

	with pytest.raises(ZeroDivisionError):
		kt.average([])

def test_average_or_0():
	assert(kt.average_or_0([1, 2, 3]) == 2)
	assert(kt.average_or_0([1]) == 1)
	assert(kt.average_or_0([1, 2, 3, 4]) == 2.5)

	assert(kt.average_or_0([]) == 0)

def test_average_streamer():
	streamer = kt.AverageStreamer()

	0, 1, 3, 6, 10, 15, 21
	averages = [0, 0.5, 1, 1.5, 2, 2.5, 3]

	with pytest.raises(ZeroDivisionError):
		streamer.query()

	for i in range(7):
		streamer.add(i)
		assert(streamer.query() == averages[i])

def test_max_streamer():
	streamer = kt.MaxStreamer()

	with pytest.raises(RuntimeError):
		streamer.query()

	for i in range(0, 10):
		streamer.add(i)
		assert(streamer.query() == i)

	for i in range(9, -1, -1):
		streamer.add(i)
		assert(streamer.query() == 9)

def test_min_streamer():
	streamer = kt.MinStreamer()

	with pytest.raises(RuntimeError):
		streamer.query()

	for i in range(0, 10):
		streamer.add(i)
		assert(streamer.query() == 0)

	for i in range(9, -1, -1):
		streamer.add(i)
		assert(streamer.query() == 0)

	for i in range(-1, -10, -1):
		streamer.add(i)
		assert(streamer.query() == i)

def test_max_score_streamer():
	streamer = kt.MaxScoreStreamer(lambda x: x)

	with pytest.raises(RuntimeError):
		streamer.query()

	with pytest.raises(RuntimeError):
		streamer.query_score()

	for i in range(0, 10):
		streamer.add(i)
		assert(streamer.query() == i)
		assert(streamer.query_score() == i)

	for i in range(9, -1, -1):
		streamer.add(i)
		assert(streamer.query() == 9)
		assert(streamer.query_score() == 9)

	streamer = kt.MaxScoreStreamer(lambda x: -x)

	with pytest.raises(RuntimeError):
		streamer.query()

	with pytest.raises(RuntimeError):
		streamer.query_score()

	for i in range(0, 10):
		streamer.add(i)
		assert(streamer.query() == 0)
		assert(streamer.query_score() == 0)

	for i in range(9, -1, -1):
		streamer.add(i)
		assert(streamer.query() == 0)
		assert(streamer.query_score() == 0)

	for i in range(-1, -10, -1):
		streamer.add(i)
		assert(streamer.query() == i)
		assert(streamer.query_score() == -i)

	streamer = kt.MaxScoreStreamer(lambda x: -1 * abs(x - 5.5))

	with pytest.raises(RuntimeError):
		streamer.query()

	with pytest.raises(RuntimeError):
		streamer.query_score()

	for i in range(0, 6):
		streamer.add(i)
		assert(streamer.query() == i)
		assert(streamer.query_score() == i - 5.5)

	for i in range(6, 10):
		streamer.add(i)
		assert(streamer.query() == 5)
		assert(streamer.query_score() == -0.5)

def test_assert_and_print():
	kt.assert_and_print(1, 1 > 0)
	kt.assert_and_print(1, 1 >= 0)
	kt.assert_and_print(1, 1 >= 1)
	test_list = [1, 2, 3]
	kt.assert_and_print(test_list, kt.average(test_list) == 2)

	with pytest.raises(AssertionError):
		test_list = [1, 2, 3]
		kt.assert_and_print(test_list, kt.average(test_list) == 3)

def test_assert_eq():
	with pytest.raises(AssertionError):
		kt.assert_eq(1, 2)

	with pytest.raises(AssertionError):
		kt.assert_eq(1, [])

	with pytest.raises(AssertionError):
		kt.assert_eq(0, [])

	kt.assert_eq(1, 1)

def test_assert_float_eq():
	with pytest.raises(AssertionError):
		kt.assert_float_eq(1, 2)

	with pytest.raises(AssertionError):
		kt.assert_float_eq(1, 1 + 1e-3)

	kt.assert_float_eq(1, 1 + 1e-10)

def test_assert_neq():
	kt.assert_neq(1, 2)

	kt.assert_neq(1, [])

	kt.assert_neq(0, [])

	with pytest.raises(AssertionError):
		kt.assert_neq(1, 1)

def test_assert_float_neq():
	kt.assert_float_neq(1, 2)

	kt.assert_float_neq(1, 1 + 1e-3)

	with pytest.raises(AssertionError):
		kt.assert_float_neq(1, 1 + 1e-10)
