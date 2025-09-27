x = 0
y = 2 ** 3
print(x)
print(y)

print("While")
while x < 20: {
    if x > 10: {
        print(x)
        break
    }
    x = x + 1
}
print("While terminou")

print("Do-While")
x = 0
do: {
    if x >= 19: {
        print(x)
    }
    x = x + 1
} while x < 20

print("For")
for i in range(10): {
    if i % 2 == 0: {
        print(i)
    } else: {
        continue
    }
}
print("For terminou")

print("For com 3 parâmetros")
for j in range(1, 10, 2): {
    print(j)
}
print("For com 3 parâmetros terminou")

print("For dentro de for")
for k in range(1, 10, 2): {
    for l in range(1, 10, 2): {
        print(k,l,k * l)
    }
}
print("For dentro de for terminou")

def teste(): {
    print("Função teste chamada")
}
    
    