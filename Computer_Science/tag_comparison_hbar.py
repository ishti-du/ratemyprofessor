import pandas as pd
import matplotlib.pyplot as plt

index = ["RESPECTED", "AMAZING LECTURES", "INSPIRATIONAL", "CARING",
         "GIVES GOOD FEEDBACK", "LOTS OF HOMEWORK", "HILARIOUS",
         "ACCESSIBLE OUTSIDE CLASS", "CLEAR GRADING CRITERIA",
         "SKIP CLASS? YOU WON'T PASS", "TOUGH GRADER",
         "PARTICIPATION MATTERS", "LECTURE HEAVY", "EXTRA CREDIT",
         "GROUP PROJECTS", "GET READY TO READ", "TEST HEAVY",
         "BEWARE OF POP QUIZZES", "GRADED BY FEW THINGS",
         "SO MANY PAPERS",
         ]

columns = ["0%", "1%", "2%", "3%", "4%", "5%", "6%", "7%", "8%", "9%"]

cs = [9.4, 9.12, 8.34, 8.26, 8.14, 7.32, 6.7, 6.5, 6.11, 5.99,
      4.74, 4.31, 3.33, 2.51, 2.35, 2.27, 1.84, 1.33, 1.14, 0.31
      ]

eng = [8.64, 7.37, 8, 9.27, 11.11, 2.23, 5.67, 6.26, 5.16, 5.22,
       5.77, 8.45, 2.01, 0.76, 1.19, 7.94, 0.2, 1.08, 2.09, 1.6
       ]

df = pd.DataFrame({'cs': cs[::-1], 'english': eng[::-1]}, index=index[::-1])
df.plot.barh()
plt.savefig('test.pdf'
