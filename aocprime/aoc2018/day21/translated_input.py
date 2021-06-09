def code():
    def and_test():
        if not (123 & 456 == 72):
            while not (0 & 456 == 72):
                pass
    r0, r1, r2, r3, r4, r5 = (0,) * 6
    def six():
        r5 = 65536
        r2 =  5234604
        while True:
            r3 = r5 & 255
            r2 += r3
            r2 &= 16777215
            r2 *=  65899
            r2 &= 16777215
            if 256 > r5:
                break
            r3 = 0
            r1 = r3 + 1
            r1 *= 256
            while not (r1 > r5):
                r3 += 1
                r1 = r3 + 1
                r1 *= 256
            r5 = r3
        while r2 != r0:
            yield r2
            r5 = r2 | 65536
            r2 =  5234604
            while True:
                r3 = r5 & 255
                r2 += r3
                r2 &= 16777215
                r2 *=  65899
                r2 &= 16777215
                if 256 > r5:
                    break
                r3 = 0
                r1 = r3 + 1
                r1 *= 256
                while not (r1 > r5):
                    r3 += 1
                    r1 = r3 + 1
                    r1 *= 256
                r5 = r3
        return 
    and_test()
    for val in six():
        yield val
def solver():
    vals = set()
    i = 1
    last_val = None
    for r in code():
        if r not in vals:
            print(i, ":", r, " "*20, end="\r")
            vals.add(r)
            i += 1
            last_val = r
        else:
            break
    return last_val
if __name__ == "__main__":
    print("Solution:", solver())
    


