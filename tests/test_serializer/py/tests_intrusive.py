from tests.test_serializer.py.gen.AllTypes import AllTypes
from tests.test_serializer.py.gen.IntrusivePtr import make_intrusive


def test_make_intrusive_with_args():
    assert make_intrusive(AllTypes).int_value0 == 0
    assert make_intrusive(AllTypes, 1).int_value0 == 1
    print('Ok: test_make_intrusive_with_args')


def test_compare_intrusive():
    a = make_intrusive(AllTypes)
    b = make_intrusive(AllTypes)
    assert a == b
    print('Ok: test_compare_intrusive')


def test_intrusive():
    test_make_intrusive_with_args()
    test_compare_intrusive()
