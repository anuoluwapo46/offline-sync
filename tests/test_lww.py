import unittest
from sync.lww import LWWStore

class TestLWWStore(unittest.TestCase):
    def test_later_time_wins(self):
        store = LWWStore()
        store.write("plot7", 45, 100, "ada")
        store.write("plot7", 42, 200, "bayo")
        self.assertEqual(store.entries["plot7"].value, 42)

    def test_merge_order_does_not_matter(self):
        ada_phone = LWWStore()
        ada_phone.write("plot7", 45, 100, "ada")
        bayo_phone = LWWStore()
        bayo_phone.write("plot7", 42, 200, "bayo")

        server1 = LWWStore()
        server1.merge(ada_phone)
        server1.merge(bayo_phone)

        server2 = LWWStore()
        server2.merge(bayo_phone)
        server2.merge(ada_phone)

        self.assertEqual(server1.entries, server2.entries)

    def test_wrong_clock_picks_the_wrong_winner(self):
            ada_phone = LWWStore()
            ada_phone.write("plot7", 45, 36000, "ada")

            bayo_phone = LWWStore()
            bayo_phone.write("plot7", 42, 36300 - 1200, "bayo")

            server = LWWStore()
            server.merge(ada_phone)
            server.merge(bayo_phone)

            self.assertEqual(server.entries["plot7"].value, 45)
if __name__ == "__main__":
     unittest.main()