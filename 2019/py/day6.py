from collections import defaultdict

class Node:
    def __init__(self):
        self.name = ''
        self.parent = None
        self.children = []

    def count_children(self):
        count = len(self.children)
        for child in self.children:
            count += child.count_children()
        return count

    def get_parents(self):
        parents = []
        node = self.parent
        while node:
            parents.append(node)
            node = node.parent
        return parents

    def count_parent_links(self, ancestor):
        node = self.parent
        count = 1
        while node != ancestor:
            count += 1
            node = node.parent
        return count

def construct_map(orbits):
    orbit_map = defaultdict(Node)
    for orbit in orbits:
        parent, child = orbit.split(')')
        parent_node = orbit_map[parent]
        child_node = orbit_map[child]

        child_node.parent = parent_node
        child_node.name = child
        parent_node.children.append(child_node)
        parent_node.name = parent
    return orbit_map

def count_orbits(orbit_map):
    return sum(o.count_children() for o in orbit_map.values())

orbits = [
    "PJK)X3G", "ZM3)JGN", "YYF)614", "K5T)X18", "2PT)2BR", "4RF)VL2", "QQN)7S4",
    "X9S)HM9", "NMG)DH5", "TQD)SJD", "2JD)SM4", "5SD)4NG", "W1R)XYJ", "DXF)72L",
    "CGN)T85", "ZF4)ZZ1", "91Q)Y69", "SMB)QSZ", "PVN)PP3", "C4S)1VL", "3BK)ZNZ",
    "LYZ)92X", "TPP)XPP", "NTK)R7B", "XMH)GBQ", "LZW)49Y", "28R)R1G", "5SX)F2K",
    "X21)WC7", "JL7)ZKL", "F1G)XF8", "XJG)N8L", "227)HBK", "FG8)RMS", "S5B)RXD",
    "T71)LDZ", "TYQ)2LW", "1W2)BFQ", "2X1)NCQ", "SJL)TG5", "64W)RKB", "DRH)W45",
    "ZTK)YC5", "L1Y)VXS", "SGD)F66", "ZBG)YJ7", "NC6)544", "XKQ)8Z5", "B5K)XFW",
    "V3F)SF9", "DC7)737", "ZCJ)ZCB", "JPX)FZS", "PFB)TYQ", "C22)HGM", "C67)MDM",
    "4W1)X87", "TQX)7YM", "2Y4)CLQ", "R1G)M5V", "HK5)56W", "Y7B)8RN", "LFR)FN6",
    "RVW)7G3", "SXH)97Y", "H25)WHC", "X8Y)3H8", "97Y)77T", "6VB)91Q", "V7S)595",
    "JFH)2JD", "ZSL)HHS", "3D6)T71", "1BP)MCR", "FBQ)2PB", "7Q9)K1X", "C81)6JF",
    "YYQ)9FR", "FBR)GZS", "VXK)4BR", "Z9L)DYJ", "PRL)K2Y", "Q68)R8F", "WJC)WZ5",
    "H3K)3NG", "K9N)BG4", "VXS)RLT", "K1Q)R29", "C76)TNL", "RLV)PCY", "Z4J)2GC",
    "4F2)SC2", "Y82)JKM", "GZS)Q1Q", "VB3)WRW", "XW6)FK8", "YG1)73H", "KZQ)9FQ",
    "R25)C13", "FFZ)DTC", "H99)Y82", "N12)TRX", "F5G)RLV", "7VN)D7V", "CRJ)GY4",
    "C7S)YD3", "V6S)CNH", "82G)ZBV", "KMM)YOU", "27R)S8P", "ZTK)2PT", "8R4)HC5",
    "V9D)ZSV", "L25)N12", "544)ZT7", "62H)SBL", "ZMG)M4P", "Y77)SB7", "G6R)2RZ",
    "YPB)6ZG", "WKT)FVM", "126)ZPY", "8KQ)KSF", "G3Q)W3D", "56F)RZX", "KFC)LHG",
    "75Y)BHL", "921)95L", "QRQ)SG4", "8BW)KGK", "5D5)YH2", "4PK)9LQ", "7J4)QQN",
    "F8Q)SBM", "14K)5NV", "6NP)91L", "JKM)HR1", "9G9)Q7P", "P74)BCK", "DBC)K1H",
    "CH7)Z9W", "GBK)YFR", "LLX)YG1", "KFB)C53", "7XJ)8Q8", "54L)JMG", "2PB)P2C",
    "ZPY)V3S", "NG6)WNM", "R29)LN8", "1DT)LTD", "XLM)X12", "3HQ)G3Q", "95L)VM4",
    "8RN)Q28", "2GC)CVB", "BHL)N5T", "X9T)GBK", "J27)G8G", "LHG)RR3", "FS5)XSF",
    "6HN)WC8", "WQR)G1C", "X5M)SXQ", "MCR)Q6W", "F57)7W8", "QKG)X4T", "PL8)BZM",
    "JM3)3KS", "GYP)6S2", "8V3)4TV", "GSV)Y9V", "JKM)5WX", "VSM)3Q5", "L7Q)L1C",
    "MFX)T1R", "GQ2)22M", "4L4)W3W", "TRX)45N", "GLG)WKT", "92T)KTL", "1PB)TFX",
    "C9N)88W", "Z19)PTB", "95K)NGQ", "8H6)CHW", "DC8)7NY", "R8F)HHP", "TFX)S9L",
    "P61)4JD", "KDW)GMS", "961)J5R", "C4H)35Y", "BJQ)FDN", "R79)P6J", "QTH)B6J",
    "K2Y)3RY", "K47)NC6", "GQR)C5W", "6HN)LLX", "Q7P)921", "WPV)VLF", "329)YPB",
    "3XV)RR1", "DTC)2CF", "C9K)X43", "5SB)X9T", "9ZL)8V3", "F5G)XMH", "VD5)XG2",
    "97R)SC9", "NCQ)F2D", "BML)2JY", "N8G)DMN", "6Y7)JXB", "M4P)Z4J", "PL1)M52",
    "57Z)HSB", "LP8)WXJ", "X49)ZHJ", "YQ4)LBF", "TZN)26G", "3NG)PLN", "XLC)TBR",
    "8ZV)77G", "3SR)QR2", "91B)J7Y", "PWH)LJS", "GG3)91S", "2NJ)C23", "MRG)V2D",
    "77G)NBP", "DBC)3N2", "Q1Q)Z34", "BH4)B5K", "V5P)8Q7", "35Y)39W", "DMN)DKJ",
    "GY4)HPQ", "66L)S4M", "FK8)W9R", "W3W)X5M", "YBW)X41", "WPG)XQN", "BKC)NBD",
    "82C)8ZV", "8LR)P74", "XL9)F17", "DKJ)V6X", "836)FFB", "RS8)K1Q", "CY5)4PC",
    "YFR)GTQ", "QF6)ZLD", "35K)5YW", "P6J)Z8W", "Z39)NJK", "J8X)T8P", "15H)YXX",
    "K5M)3B4", "FVY)L93", "DS2)QP5", "39W)WTS", "NFM)LFR", "4ZR)N8K", "JGW)4XY",
    "XSP)9YR", "5WB)286", "292)637", "KTL)3CT", "TQR)GPW", "ZT7)7H2", "6YX)VCC",
    "G2X)HLX", "7QT)33M", "SXQ)6VY", "1WQ)ZMG", "G1C)35K", "D7V)PZG", "73H)NG6",
    "TQD)6M6", "GPW)YQ4", "C67)C4H", "G6F)9YS", "YLZ)YBW", "4XZ)KSG", "11N)V9D",
    "56W)8R4", "S8P)PVN", "XG2)Z7K", "LBF)6KM", "ZSV)VF3", "QV6)JJN", "2D9)VM8",
    "TYB)NTG", "Q94)QNF", "4JD)J8X", "5WB)MVZ", "X12)KV2", "79V)VP8", "8VV)B6R",
    "T42)8BW", "C13)Z9L", "WFY)HC7", "3LK)RV9", "6LP)W98", "6LD)XLM", "YBQ)GQ2",
    "VF3)MLX", "DQ7)66L", "C53)5F1", "5F1)YZY", "3GQ)C67", "M52)VWY", "M89)9L5",
    "HPQ)4W1", "8Z5)7FX", "F8Q)1TY", "4FC)VN3", "2DG)PL1", "KT2)7QT", "X3G)GH2",
    "VFH)5ZL", "3SN)ZW3", "RTP)1KS", "KGK)2NJ", "8Z5)F57", "91S)DC7", "SLY)QBX",
    "BKH)M89", "637)6FC", "V7K)L25", "QCF)Q3X", "4L1)X58", "B2S)J5L", "JJK)6PN",
    "F4V)MHH", "SC4)34G", "5XC)GPJ", "PTB)579", "C3D)XCK", "HDY)PCH", "KTM)8XY",
    "3KS)GYP", "HHS)RD2", "68B)YBQ", "L1C)7C7", "TKK)NWD", "YD3)JKC", "VM8)38W",
    "S9X)H3K", "VN3)WPG", "2RZ)56F", "PG2)Z3G", "SJD)SKH", "JKC)XJG", "KTK)V6B",
    "Z7L)64W", "6KS)GR6", "BZM)6NP", "HSB)2T3", "YC5)5WB", "6RL)PFB", "TL2)XSP",
    "8NL)VV7", "KZH)3BK", "FN6)FG8", "NQ6)YWV", "4K3)WFZ", "4VT)SZH", "7C7)JKB",
    "FJJ)WP9", "FBZ)QRQ", "88W)RD6", "GPH)5VZ", "F17)7FJ", "VWY)TWJ", "BRN)95K",
    "R55)LP8", "9K3)M4B", "NWD)JSX", "4NS)783", "6VH)D6T", "XYQ)BHN", "3RY)MFX",
    "KGR)QGX", "1XH)MNS", "1TY)15L", "XWV)WJC", "JJN)8B3", "Y8L)Y7B", "FFQ)3SG",
    "F77)Z5Z", "783)Q9R", "HF2)RMK", "WRW)JT4", "6MS)FBQ", "44G)BRN", "FDN)289",
    "4NJ)ZF6", "WN8)Y77", "66G)FMH", "773)7HJ", "M4B)Z7L", "V88)52G", "2HR)24V",
    "3KH)VYY", "77T)PG2", "S8N)G6F", "QY2)54G", "F66)9KL", "FLB)SFB", "HLX)32D",
    "S4M)VXK", "XPP)DQ7", "3SG)BH4", "Z5S)XW6", "92X)XLC", "LQ4)3GQ", "729)PRL",
    "S3N)Z5S", "29B)K47", "WBQ)TKK", "BJR)GC5", "Y82)ZM3", "GK1)62H", "8Q7)ZR3",
    "7YM)7Q9", "4R4)FQ7", "B6V)2HR", "T95)LQ4", "T99)6SL", "COM)ZB8", "4SC)SMZ",
    "X87)GX6", "ZKL)M72", "7W8)WN8", "64G)15F", "34G)K9J", "BSK)2MM", "1ZV)4FC",
    "Z5Z)CZC", "LKS)N8G", "XDC)P5D", "RXD)B9R", "2BR)BKC", "HHP)85J", "QX7)FWL",
    "WTS)WBQ", "ZLY)6T5", "LP9)G65", "9ZL)GG2", "4JY)2FH", "QJZ)384", "6S2)ZLY",
    "2W1)XL9", "X4T)LKB", "38W)2YD", "RZX)NL6", "2BW)ZF4", "K6L)24D", "TZM)SGD",
    "2JY)K5T", "MP9)GLG", "8VV)TQX", "MQJ)G2B", "W9R)Y8L", "6Y8)8NR", "CNH)2X1",
    "5Y4)QKG", "TWJ)V7S", "CNJ)9K3", "5VZ)YYF", "48Q)4L1", "1VL)2W1", "HSB)VC9",
    "HKT)45Z", "CP6)XY1", "JKC)GM1", "B1H)D6Q", "4B9)8XW", "DLX)15H", "45Z)HNQ",
    "289)75Y", "2MM)GCH", "NBD)FFZ", "QGX)Q3V", "N1F)9G9", "P54)P9L", "GC5)62Z",
    "15L)11N", "TK1)CCW", "35W)8S3", "4NG)4FZ", "1P9)MND", "5ZL)FVY", "L5P)79V",
    "VCC)WPV", "8BG)9M4", "24V)T95", "YFR)F1G", "FS5)H1M", "JKB)YVS", "N1K)7NP",
    "LKR)S82", "SLY)7R3", "GTQ)L2N", "L2N)4DJ", "CGN)7S9", "NJ7)7QH", "WXB)KT2",
    "R3T)78Q", "XSF)QCF", "T85)1W2", "11N)29B", "6SL)BQ2", "1Y2)C81", "B6J)5XC",
    "GV4)LW1", "FFB)1WQ", "GPP)6LP", "FYL)4R4", "K9N)KZQ", "ZB8)RRS", "YP6)Q68",
    "9FQ)1PB", "7G3)2L3", "KJK)NYV", "WNM)9ZL", "JMZ)QF6", "38S)44G", "JG6)LYZ",
    "286)WXS", "B4B)Y8Y", "ZML)VRJ", "Z2X)FVK", "TNS)8BG", "8S3)QLD", "NBP)DRH",
    "TKL)429", "CC7)9DN", "FYL)14D", "LLX)3SZ", "QQX)WF9", "LJS)GMZ", "7R3)2WR",
    "4GT)4F2", "9LQ)DBC", "YPZ)4GT", "9BK)SMB", "QB9)P4L", "3N2)ZQ9", "7N8)F7L",
    "BLG)B2S", "1SF)W53", "ZZ1)4B9", "H4Q)KJK", "ZXN)4SC", "82C)8D8", "15F)KGR",
    "54G)XXH", "J7Y)QJZ", "SNM)SXH", "BKH)8VV", "SMB)KTK", "ZS2)2KV", "L2N)C76",
    "Q1T)BJQ", "GQR)SK6", "QQK)TGL", "LW1)FLB", "3B4)J6L", "V6B)57Z", "Y1R)2DG",
    "QQH)Z2Q", "G8G)8KQ", "8NR)K9N", "6M6)3KH", "J27)28R", "85J)48Q", "RLT)LKR",
    "XY1)CGN", "ZW3)N1K", "QR2)6LD", "88G)G6R", "QGY)126", "5XC)X9S", "X5N)7VN",
    "8D8)97R", "PYX)KMM", "N8K)7B8", "MF9)PXY", "8WW)4NS", "JZ8)RVW", "H1M)78C",
    "QZV)3XV", "YZY)66Z", "WFZ)44F", "3Q5)PPH", "NTG)SNM", "HBK)CM6", "6JF)CH7",
    "CVB)Y9X", "F5G)TZN", "95K)Y1R", "614)54L", "TPP)66G", "4BR)8WW", "YJ7)W1R",
    "Q9R)773", "YH2)SY4", "2CF)3Q6", "GK1)NPV", "6PL)TL2", "6RQ)X5N", "TGK)52W",
    "7HJ)SC4", "7B8)L8S", "MKR)88G", "SC2)DLX", "SF9)KFC", "QSZ)KBD", "VL2)S9X",
    "LV6)HK5", "FMJ)8R2", "9YR)YLZ", "N23)V3F", "B6R)DXF", "M5V)KZH", "6VY)CRW",
    "T3Z)MQJ", "JVM)WFJ", "33M)9G7", "W45)VFH", "YZY)1LY", "HR1)QF5", "JGN)QB9",
    "991)F5G", "78C)J27", "8XW)5SB", "BHN)4SY", "LKB)BSK", "3DL)GQR", "9XC)B6V",
    "L4C)PD6", "LN8)82C", "P2C)Z19", "SNM)C3D", "4SY)8NL", "8Q8)4RF", "QLD)NS6",
    "C7M)6HN", "PZG)TBV", "D6T)KFB", "DYJ)TLH", "PQJ)729", "Z7K)QQK", "ZLD)Q49",
    "JT4)6PL", "49Y)WZ9", "X43)VNS", "3SZ)H25", "ZF6)QGY", "SCD)FMJ", "6FC)RTP",
    "RMS)GZC", "VNS)961", "Z2Q)NJ7", "H3K)9XC", "9J3)6VB", "BRN)3HQ", "NQY)GTK",
    "D8W)F6F", "GMS)LXG", "L5Y)B1H", "HC5)KTM", "QVC)292", "MCN)G2X", "HC7)TNW",
    "QBX)1XH", "X1H)X5D", "NPV)SLY", "DYN)VD5", "CCW)7CP", "TG5)6Y7", "6PL)CYJ",
    "2LW)8H9", "77T)ZXN", "X5D)HJ2", "S82)2BW", "729)PL8", "Y9V)8MW", "PCH)LZW",
    "XQN)3SN", "WC7)ZML", "V3S)JJK", "T46)XG7", "XF4)TPP", "SH8)2Y4", "WXT)892",
    "P9L)V6S", "PXY)JG4", "CY5)MF9", "X41)NQ6", "B9R)9HH", "M4P)91B", "RD6)QQ4",
    "SMZ)X49", "4DJ)BKH", "D6Q)F8Q", "ZHJ)4ZZ", "MDM)QXG", "RMK)B5Z", "27F)1Y2",
    "J87)Z39", "G65)5Y4", "NGQ)LP9", "Z34)MP9", "VLN)YPZ", "MHH)K6L", "F7L)JZ8",
    "9KL)8LZ", "5XS)TK1", "MNS)Z2X", "2KZ)K5M", "CZC)8LR", "RS8)7XJ", "M72)VHV",
    "6PN)TKL", "SG4)FBR", "SC9)5WZ", "N8L)ZTK", "XG7)MKK", "KB9)JL7", "1GQ)82G",
    "N4X)91W", "F6F)NR4", "44F)1SF", "SZH)CNJ", "V2D)F7M", "Y77)RS8", "VD3)7P7",
    "LXG)S5B", "QXG)KDW", "2KV)T46", "XXJ)1BP", "ZNZ)MBB", "BG4)Q94", "B5Z)CVD",
    "5WZ)T8K", "2MM)FLH", "CHW)V88", "FZS)DS2", "WZ5)LDJ", "BFQ)MKR", "Y1R)YLV",
    "QLD)34L", "737)GPH", "QQX)1ZV", "CRW)T42", "73H)L9K", "G2B)VJV", "9G7)SH8",
    "Z3G)T3Z", "9YS)TGK", "7NY)27R", "8R2)WXT", "GPH)FS5", "KBD)7N8", "HM9)68B",
    "2YD)PD5", "9YS)38S", "Z8W)W8Z", "3KH)X4V", "6ZG)935", "36T)QX7", "9L5)SPK",
    "VLF)4L4", "XCK)GPP", "66Z)FFQ", "XXH)H4Q", "FWL)TQD", "9DN)YYQ", "F7M)4XZ",
    "7S4)BML", "L58)FCC", "739)XWV", "YQ4)FJJ", "3CT)JM3", "KSG)NMG", "6T5)JG6",
    "T8K)X8Y", "K6L)QQH", "P74)9HY", "JG4)9BK", "9FR)836", "TNW)6RL", "RR3)HD6",
    "26G)SCD", "HC5)B98", "72L)6G9", "6G9)1DT", "32D)FBZ", "1TY)C7S", "QQ4)43D",
    "RV9)5D5", "7P7)MCN", "5YW)6YX", "S99)6RQ", "RR1)YBD", "V6X)227", "SBL)6Y8",
    "6KM)X21", "66Y)4VT", "91L)4PK", "PD5)4K3", "Y8Y)L1Y", "LHS)L4C", "1LY)SAN",
    "W8Z)L5Y", "V6X)KS8", "7FX)J87", "YXX)B4B", "CLQ)S8N", "JGW)H99", "WHC)SJL",
    "XMH)V5P", "VP8)BLG", "BCK)R55", "4PC)Q1T", "TBV)N23", "B66)JMZ", "YLV)TNS",
    "88G)4C6", "RLT)Q76", "RRS)WXZ", "43D)WQR", "ZR3)HDY", "S2D)QQX", "DTC)BJR",
    "Q3X)YP6", "7QH)PWH", "WXJ)329", "SCK)1GQ", "QKG)GSV", "ZHJ)HKT", "BML)CY5",
    "WFJ)46L", "TLH)36T", "VC9)QY2", "2CF)NFM", "Z4B)VYK", "46L)5KV", "GCH)X1H",
    "14D)3DL", "PD6)QZV", "34L)LHS", "X8Y)9HW", "QF5)KB9", "24D)WXB", "GVR)D8W",
    "PCY)PJK", "1QW)L48", "J5L)LKS", "ZQ9)JPX", "L9K)V7K", "X4V)4ZR", "SB7)8H6",
    "VF3)HHD", "2WR)QTH", "PPH)W66", "C23)ZKT", "HGM)XDC", "NS6)8GQ", "X58)991",
    "MLX)S3N", "ZCB)14K", "29Q)5SD", "BH4)7D3", "FVK)NPP", "Y9X)N2Q", "GH2)R79",
    "HJ2)739", "WXS)B66", "SY4)59D", "F2K)NTK", "HHD)35W", "935)4NJ", "ZKT)C7M",
    "V2D)C9K", "HD6)2D9", "B98)SCK", "ZF6)7J4", "PVN)L7Q", "SBM)F77", "3H8)29Q",
    "F2D)W41", "FLH)QV6", "YT8)S99", "GBQ)YT8", "WXZ)6MS", "C5W)WFB", "KV2)66Y",
    "TBR)L5P", "NL6)3SR", "SK6)ZCJ", "VYY)P54", "2L3)GV4", "K1X)ZS2", "7D3)Z4B",
    "384)457", "8R2)TGF", "ZB8)CC7", "KS8)TYB", "RKB)2YT", "K1H)XXJ", "52W)S2D",
    "WF9)P61", "WP9)GG3", "95M)8BB", "W53)CP6", "CM6)R25", "GTK)TZM", "Q28)D68",
    "WC8)VD3", "JMG)KCW", "9HW)JFH", "9HY)92T", "8GQ)6KS", "62Z)9WY", "VRJ)81G",
    "TGL)VLN", "TGF)ZSL", "XW6)XJS", "TNL)XYQ", "9G9)PQJ", "VYK)4JY", "GMZ)PQ1",
    "NJK)L58", "XF8)JVM", "GQ2)GVR", "N2Q)XKQ", "SM4)TQR", "C4S)QVC", "Q76)LV6",
    "FMH)3D6", "7B8)C4S", "VYY)2KZ", "9L5)27F", "7FJ)T99", "GY4)JGW", "YYQ)WFY",
    "GV4)CRJ", "457)VSM", "7G3)1P9", "SKH)DYN", "4PK)9J3", "7S9)C22", "1KS)V6H",
    "YVS)N4X", "2YT)F4V", "4ZZ)ZBG", "FVM)PYX", "8BB)1QW", "PQ1)TCV", "NR4)5SX",
    "9WY)95M", "SPK)DC8", "W3D)VB3", "L93)3LK", "K9J)C9N", "4C6)MRG", "P5D)5XS",
    "4XY)HF2", "MFS)64G", "T33)R3T", "SFB)TV7", "78Q)FYL", "892)GK1", "GG2)N1F",
    "LTD)XF4", "5WX)NQY", "QNF)T33", "CYJ)6VH", "NTG)MFS",
]

# orbits = [
#     "COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K",
#     "K)L"
# ]

orbit_map = construct_map(orbits)
num_orbits = count_orbits(orbit_map)
print("part 1: {}".format(num_orbits))
assert num_orbits == 106065


# orbits = [
#     "COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K",
#     "K)L", "K)YOU", "I)SAN",
# ]

n1 = orbit_map['YOU'].parent
n2 = orbit_map['SAN'].parent
common_parents = set(n1.get_parents()) & set(n2.get_parents())
hops = [n1.count_parent_links(o) + n2.count_parent_links(o) for o in common_parents]
min_hops = min(hops)
print("part 2: {}".format(min_hops))
assert min_hops == 253

