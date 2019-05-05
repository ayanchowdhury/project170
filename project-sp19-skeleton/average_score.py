from subprocess import check_output
import statistics as stats

runs = input("Enter number of runs to try: ")
try:
    r = int(runs)
    scores = []
    for i in range(1, r + 1):
        output = check_output(["python3","client.py","--solver","solver"])
        score = float(output[-18:-1])
        print("Attempt " + str(i) + ": " + str(score))
        scores.append(score)

    avg = stats.mean(scores)
    print("Average Score for " + str(r) + " runs: " + str(avg))
    exit()

except ValueError:
   print("Error: Not an int")
   exit()