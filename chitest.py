from scipy.stats import chisquare
fob = [40, 10]
fex = [42.5, 7.5]

# fob =[305, 195]
# fex =[400, 100]

result = chisquare(fob, f_exp=fex)
print(result)