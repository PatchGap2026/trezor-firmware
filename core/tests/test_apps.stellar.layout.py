# flake8: noqa: F403,F405
from common import *  # isort:skip

if not utils.BITCOIN_ONLY:
    from trezor.messages import (
        StellarInt128Parts,
        StellarInt256Parts,
        StellarUInt128Parts,
        StellarUInt256Parts,
    )

    from apps.stellar.operations.layout import (
        _format_i128,
        _format_i256,
        _format_u128,
        _format_u256,
    )


@unittest.skipUnless(not utils.BITCOIN_ONLY, "altcoin")
class TestStellarFormatIntegers(unittest.TestCase):
    def test_format_u128(self):
        TESTS = [
            ((0, 0), "0"),
            ((0, 1), "1"),
            ((1, 0), str(2**64)),
            ((0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF), str(2**128 - 1)),
        ]
        for (hi, lo), expected in TESTS:
            self.assertEqual(_format_u128(StellarUInt128Parts(hi=hi, lo=lo)), expected)

    def test_format_i128(self):
        TESTS = [
            ((0, 0), "0"),
            ((0, 1), "1"),
            ((-1, 0xFFFFFFFFFFFFFFFF), "-1"),
            ((1, 0), str(2**64)),
            ((-1, 0), str(-(2**64))),
            ((0x7FFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF), str(2**127 - 1)),
            ((-0x8000000000000000, 0), str(-(2**127))),
        ]
        for (hi, lo), expected in TESTS:
            self.assertEqual(_format_i128(StellarInt128Parts(hi=hi, lo=lo)), expected)

    def test_format_u256(self):
        TESTS = [
            ((0, 0, 0, 0), "0"),
            ((0, 0, 0, 1), "1"),
            ((0, 0, 1, 0), str(2**64)),
            ((0, 1, 0, 0), str(2**128)),
            ((1, 0, 0, 0), str(2**192)),
            (
                (
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                ),
                str(2**256 - 1),
            ),
        ]
        for (hi_hi, hi_lo, lo_hi, lo_lo), expected in TESTS:
            parts = StellarUInt256Parts(
                hi_hi=hi_hi, hi_lo=hi_lo, lo_hi=lo_hi, lo_lo=lo_lo
            )
            self.assertEqual(_format_u256(parts), expected)

    def test_format_i256(self):
        TESTS = [
            ((0, 0, 0, 0), "0"),
            ((0, 0, 0, 1), "1"),
            (
                (
                    -1,
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                ),
                "-1",
            ),
            ((0, 0, 1, 0), str(2**64)),
            ((-1, 0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0), str(-(2**64))),
            ((0, 1, 0, 0), str(2**128)),
            ((-1, 0xFFFFFFFFFFFFFFFF, 0, 0), str(-(2**128))),
            ((1, 0, 0, 0), str(2**192)),
            ((-1, 0, 0, 0), str(-(2**192))),
            (
                (
                    0x7FFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                    0xFFFFFFFFFFFFFFFF,
                ),
                str(2**255 - 1),
            ),
            ((-0x8000000000000000, 0, 0, 0), str(-(2**255))),
        ]
        for (hi_hi, hi_lo, lo_hi, lo_lo), expected in TESTS:
            parts = StellarInt256Parts(
                hi_hi=hi_hi, hi_lo=hi_lo, lo_hi=lo_hi, lo_lo=lo_lo
            )
            self.assertEqual(_format_i256(parts), expected)


if __name__ == "__main__":
    unittest.main()
