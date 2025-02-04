#senkron işlerin sırasıyla yapılması demektir.
import time


def my_func_1():
    print("1. fonksiyon başlıyor")
    time.sleep(5)
    print("1.fonksiyon bitti")
    return 5

def my_func_2():
    print("2. fonksiyon başlıyor")
    time.sleep(5)
    print("2.fonksiyon bitti")
    return 10

if __name__ == "__main__":
    x= my_func_1()
    y=my_func_2()

    print(f" my func 1'in çalışması sonucu x 'in dğeri{x}")
    print(f" my func 2'in çalışması sonucu y 'in dğeri{y}")



